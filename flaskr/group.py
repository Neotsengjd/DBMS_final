from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from database import db

group = Blueprint("group", __name__)

@group.route("/<int:user_id>", methods=["GET", "POST"])
def group_home(user_id):

    cursor = db.connection.cursor()
    
    # 預設 (GET) 先載入所有群組名稱，給 "Join Group" 那段用 (下拉選單)
    all_groups = []
    try:
        cursor.execute("SELECT GName FROM GROUP_LEADER;")
        all_groups = cursor.fetchall()  # 回傳 [(群組名稱,), (群組名稱,), ...]
    except Exception as e:
        print(f"Error fetching all group names: {e}")
        db.connection.rollback()
        abort(500, "Error loading group list.")
    
    # my_groups 用來儲存「我的群組」查詢結果；初次 GET 時可為 None
    my_groups = None
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # ---------------------------
        # 1) 查詢 "My Group"
        # ---------------------------
        if action == "my_group":
            try:
                # 根據你提供的 MY GROUP SQL 寫法
                sql_my_group = """
                SELECT GL.GroupID, GL.GName, 'Leader' AS Role
                FROM `GROUP_LEADER` GL
                WHERE GL.Leader = %s
                UNION
                SELECT GL.GroupID, GL.GName, 'Member' AS Role
                FROM `GROUP_MEMBER` GM
                JOIN `GROUP_LEADER` GL ON GM.M_GroupID = GL.GroupID
                WHERE GM.Members = %s
                """
                cursor.execute(sql_my_group, (user_id, user_id))
                my_groups = cursor.fetchall()  # [(GroupID, GName, Role), (...), ...]
                
                if not my_groups:
                    flash("目前沒有任何群組紀錄。", "info")
                
            except Exception as e:
                print(f"Error fetching my groups: {e}")
                db.connection.rollback()
                abort(500, "Error fetching my group data.")
        
        # ---------------------------
        # 2) 加入 "Join Group"
        # ---------------------------
        elif action == "join_group":
            group_name = request.form.get("group_name")  # 下拉式選單的值
            if not group_name:
                flash("請選擇欲加入的群組！", "warning")
            else:
                try:
                    # 依照你提供的 Join Group SQL 邏輯
                    sql_join = """
                    INSERT INTO `GROUP_MEMBER` (M_GroupID, Members)
                    SELECT GL.GroupID, %s
                    FROM `GROUP_LEADER` GL
                    WHERE GL.GName = %s
                      -- (1) 檢查使用者是否存在
                      AND EXISTS (
                          SELECT 1
                          FROM `USERS` U
                          WHERE U.ID = %s
                      )
                      -- (2) 確認該用戶尚未在此群組
                      AND NOT EXISTS (
                          SELECT 1
                          FROM `GROUP_MEMBER` GM
                          WHERE GM.Members   = %s
                            AND GM.M_GroupID = GL.GroupID
                      );
                    """
                    cursor.execute(sql_join, (user_id, group_name, user_id, user_id))
                    db.connection.commit()
                    
                    # rowcount > 0 表示成功插入一筆
                    if cursor.rowcount > 0:
                        flash(f"成功加入群組「{group_name}」!", "success")
                    else:
                        flash(f"加入群組「{group_name}」失敗：可能已加入過或群組不存在。", "danger")
                
                except Exception as e:
                    print(f"Error joining group: {e}")
                    db.connection.rollback()
                    abort(500, "Error joining group.")
        
        # ---------------------------
        # 3) 建立 "Create Group"
        # ---------------------------
        elif action == "create_group":
            group_name = request.form.get("group_name")
            if not group_name:
                flash("請輸入想建立的群組名稱！", "warning")
            else:
                try:
                    # 依照 Create Group SQL 邏輯
                    sql_create = """
                    INSERT INTO `GROUP_LEADER` (Leader, GName)
                    SELECT %s, %s
                    WHERE 
                        -- 1) 先確認隊長是否存在
                        EXISTS (
                            SELECT 1
                            FROM `USERS` U
                            WHERE U.ID = %s
                        )
                        -- 2) 再確認此群組名稱尚未被使用
                        AND NOT EXISTS (
                            SELECT 1
                            FROM `GROUP_LEADER` GL
                            WHERE GL.GName = %s
                        );
                    """
                    cursor.execute(sql_create, (user_id, group_name, user_id, group_name))
                    db.connection.commit()
                    
                    # rowcount > 0 表示成功插入
                    if cursor.rowcount > 0:
                        flash(f"成功建立群組「{group_name}」!", "success")
                    else:
                        flash(f"群組「{group_name}」已存在，或使用者ID有誤。", "danger")
                
                except Exception as e:
                    print(f"Error creating group: {e}")
                    db.connection.rollback()
                    abort(500, "Error creating group.")
    
    cursor.close()
    # 回到 group.html，並把 my_groups, all_groups 帶進模板
    return render_template(
        "group_home.html",
        user_id=user_id,
        my_groups=my_groups,     # 可能是 None 或 查詢結果
        all_groups=all_groups    # 供下拉式選單使用
    )
