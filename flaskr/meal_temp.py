from flask import Blueprint, request, abort, jsonify
from flask import Blueprint, request, abort, jsonify, render_template, redirect, url_for, flash
from datetime import datetime, timedelta
from database import db  # 確保 `db` 已正確實現連線池
from flask import render_template
import datetime

meal = Blueprint("meal", __name__)

@meal.route('/add_meal/<int:user_id>', methods=['GET', 'POST'])
def add_meal(user_id):
    cursor = db.connection.cursor()
    if request.method == 'POST':
        try:
            # 從表單取得使用者輸入
            meal_date = request.form['meal_date']  # 日期
            meal_time = request.form['meal_time']  # 時間
            meal_category = request.form['meal_category']  # 類型 (如 Breakfast, Lunch)

            # 獲取新的 MealID (假設 MealID 自增)
            cursor.execute("""
                SELECT COALESCE(MAX(MealID), 0) + 1
                FROM MEAL
                WHERE UID = %s;
            """, (user_id,))
            new_meal_id = cursor.fetchone()[0]

            # 插入新餐點資料到 MEAL 表
            cursor.execute("""
                INSERT INTO MEAL (MealID, UID, Dates, Times, Category)
                VALUES (%s, %s, %s, %s, %s);
            """, (new_meal_id, user_id, meal_date, meal_time, meal_category))
            db.connection.commit()

            # flash("Meal added successfully!")
            return redirect(url_for('meal.query', user_id=user_id))
        except Exception as e:
            print(f"Error adding meal: {e}")
            db.connection.rollback()
            abort(500, "An error occurred while adding the meal.")
        finally:
            cursor.close()

    # return render_template('meal.query', user_id=user_id)
    return render_template('add_meal.html', user_id=user_id) 
@meal.route('/query/<int:user_id>', methods=['GET'])
def query(user_id):
    cursor = db.connection.cursor()
    try:
        # Query for 'Meal' data within the last 7 days
        cursor.execute(
            """
            SELECT 
                Dates AS Date,
                Times AS Time,
                Category AS MealCategory
            FROM 
                MEAL
            WHERE 
                UID = %s AND Dates >= DATE_SUB(CURDATE(), INTERVAL 100 DAY)
            ORDER BY 
                Dates DESC, Times DESC;
            """, (user_id,)
        )
        result = cursor.fetchall()
        # 格式化數據為字典列表
        meals = [
            {
                "Date": row[0].strftime('%Y-%m-%d'),  # 格式化日期
                "Time": (datetime.datetime.min + row[1]).time().strftime('%H:%M:%S'),  # 格式化時間
                "MealCategory": row[2]  # 餐點類型
            }
            for row in result
        ]
        cursor.close()
        
        # Pass the query result to the template
        return render_template('meal_info.html', user_id=user_id, meals=meals)
    except Exception as e:
        db.connection.rollback()
        cursor.close()
        return jsonify({"status": "error", "message": str(e)})
