from flask import (
    Blueprint,
    render_template,
    request,
    abort,
    url_for,
    redirect,
    flash,
    jsonify,
    Flask
)
from database import db

goal = Blueprint("goal",__name__)

# for a given user_id, get all goals including gid and gname
@goal.route('/get_all_goals',methods=['GET', 'POST'])
def get_all_goals():

    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT GID, GName
                FROM Goals
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchall()
        goals = []
        for item in result:
            gid, gname = item
            goals.append({
                "Gid": gid,
                "GName": gname
            })
        cursor.close()
        return jsonify(goals),200
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

# for a given data_id, get the owner goal of this data
@goal.route("/get_my_partner_goal", methods=["GET"])
def get_my_partner_goal():
    try:
        data_id= request.args.get("data_id")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                SELECT GID
                FROM DataToGoal
                WHERE DID = {data_id}
            """
        )
        gid = cursor.fetchall()
        return jsonify(gid), 200
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")
