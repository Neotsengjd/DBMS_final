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

user = Blueprint("user",__name__)

@user.route('/get_user_id',methods=['GET', 'POST'])
def get_user_id():
    user_acc = request.args.get('user_acc')
    user_password = request.args.get('user_password')

    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT UID
                FROM Users 
                WHERE UAccount = '{user_acc}' AND UPassword = '{user_password}';
            """
        )
        result = cursor.fetchone()
        cursor.close()
        return jsonify(result)
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/get_name',methods=['GET', 'POST'])
def get_user_name():
    
    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT UName
                FROM Users 
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchone()
        cursor.close()
        return jsonify(result)
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")
        

@user.route('/get_isright',methods=['GET', 'POST'])
def get_is_right():
    
    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT isrightHander
                FROM Users 
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchone()
        cursor.close()
        return jsonify(result)
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/get_isdark',methods=['GET', 'POST'])
def get_is_dark():
    
    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT isDarkMode
                FROM Users 
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchone()
        cursor.close()
        return jsonify(result)
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/get_ntime',methods=['GET', 'POST'])
def get_ntime():
    
    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT NoticeTime
                FROM Users 
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchone()
        notice_time = result[0]
        notice_time_str = str(notice_time)
        return jsonify(notice_time_str)
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/get_acc',methods=['GET', 'POST'])
def get_user_acc():
    
    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT UAccount
                FROM Users 
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchone()
        cursor.close()
        return jsonify(result)
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/get_password',methods=['GET', 'POST'])
def get_user_password():
    
    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT UPassword
                FROM Users 
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchone()
        cursor.close()
        return jsonify(result)
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/get_budget',methods=['GET', 'POST'])
def get_budget():
    
    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT BUDGET
                FROM Users 
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchone()
        cursor.close()
        return jsonify(result)
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/get_nname',methods=['GET', 'POST'])
def get_user_nname():
    
    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT UNickname
                FROM Users 
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchone()
        cursor.close()
        return jsonify(result)
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")


@user.route('/update_name',methods=['PUT', 'GET'])
def update_user_name():
    
    user_id = request.args.get('user_id')
    new_name = request.args.get('new_name')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Users
                SET UName = '{new_name}'
                WHERE UID = {user_id};
            """
        )
        db.connection.commit()
        cursor.close()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/update_password',methods=['PUT', 'GET'])
def update_user_password():
    
    user_id = request.args.get('user_id')
    new_password = request.args.get('new_password')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Users
                SET UPassword = {new_password}
                WHERE UID = {user_id};
            """
        )
        db.connection.commit()
        cursor.close()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/update_acc',methods=['PUT', 'GET'])
def update_user_acc():
    
    user_id = request.args.get('user_id')
    new_acc = request.args.get('new_acc')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Users
                SET UAccount = {new_acc}
                WHERE UID = {user_id};
            """
        )
        db.connection.commit()
        cursor.close()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/update_nname',methods=['PUT', 'GET'])
def update_user_nname():
    
    user_id = request.args.get('user_id')
    new_nname = request.args.get('new_nname')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Users
                SET UNickname = '{new_nname}'
                WHERE UID = {user_id};
            """
        )
        db.connection.commit()
        cursor.close()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")


@user.route('/update_ntime',methods=['PUT', 'GET'])
def update_user_ntime():
    
    user_id = request.args.get('user_id')
    new_ntime = request.args.get('new_ntime')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Users
                SET NoticeTime = {new_ntime}
                WHERE UID = {user_id};
            """
        )
        db.connection.commit()
        cursor.close()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")


@user.route('/update_isright',methods=['PUT', 'GET'])
def update_user_isright():
    
    user_id = request.args.get('user_id')
    new_isright = request.args.get('new_isright')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Users
                SET isrightHander = {new_isright}
                WHERE UID = {user_id};
            """
        )
        db.connection.commit()
        cursor.close()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

@user.route('/update_isdark',methods=['PUT', 'GET'])
def update_user_isdark():
    
    user_id = request.args.get('user_id')
    new_isdark = request.args.get('new_isdark')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Users
                SET isDarkMode = {new_isdark}
                WHERE UID = {user_id};
            """
        )
        db.connection.commit()
        cursor.close()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")


@user.route('/update_budget',methods=['PUT', 'GET'])
def update_user_budget():
    
    user_id = request.args.get('user_id')
    new_budget = request.args.get('new_budget')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Users
                SET BUDGET = {new_budget}
                WHERE UID = {user_id};
            """
        )
        db.connection.commit()
        cursor.close()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")


def check_account(user_acc):

    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT COUNT(*)
                FROM Users 
                WHERE UAccount = '{user_acc}';
            """
        )
        result = cursor.fetchone()
        cursor.close()
        if result[0] == 0: #if != 0 means account already exist return true
            return False
        else: return True
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500") 


@user.route('/insert_acc_password',methods=['GET','POST'])
def insert_user_acc_password():
    
    user_name = request.args.get('user_name')
    user_acc = request.args.get('user_acc')
    user_password = request.args.get('user_password')
    #user_nickname = request.args.get('user_nickname')
    print(user_name)
    if check_account(user_acc):
        return 'account already exist!'
    #print("{}, {}, {}".format(user_name, user_acc, user_password))
    cursor = db.connection.cursor()
    try:
        #print("YESY")
        cursor.execute(
            f"""
                INSERT INTO Users (UName, UAccount, UPassword) VALUES ('{user_name}', '{user_acc}', '{user_password}');
            """
        )
        #print("NO")
        db.connection.commit()
        return 'success!'
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")