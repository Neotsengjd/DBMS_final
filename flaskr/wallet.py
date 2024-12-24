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

wallet = Blueprint("wallet",__name__)

# for a given user_id, get all wallets including wid and wname
@wallet.route('/get_all_wallets',methods=['GET', 'POST'])
def get_all_wallets():

    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT WID, WName
                FROM Wallets
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchall()
        wallets = []
        for item in result:
            wid, wname = item
            wallets.append({
                "wid": wid,
                "wname": wname
            })
        cursor.close()
        return jsonify(wallets),200
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

# for a given user id and wallet name, insert a new wallet
@wallet.route('/insert_wallet',methods=['GET', 'POST', 'PUT'])
def insert_wallet():

    user_id = request.args.get('user_id')
    wallet_name = request.args.get('wallet_name')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                INSERT INTO Wallets (UID, WName)
                VALUES ({user_id}, '{wallet_name}');
            """
        )
        cursor.execute("COMMIT")
        cursor.close()
        return jsonify({"message": "success"}), 201
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

# for a given wallet_id, delete a wallet
@wallet.route('/delete_wallet',methods=['GET', 'POST', 'DELETE'])
def delete_wallet():

    wallet_id = request.args.get('wallet_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                DELETE FROM Wallets
                WHERE WID = {wallet_id};
            """
        )
        cursor.execute("COMMIT")
        cursor.close()
        return jsonify({"message": "success"}), 201
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

# for a given wallet_id, update wallet name
@wallet.route('/update_wallet',methods=['GET', 'POST', 'PUT'])
def update_wallet():

    wallet_id = request.args.get('wallet_id')
    new_wallet_name = request.args.get('new_wallet_name')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                UPDATE Wallets
                SET WName = '{new_wallet_name}'
                WHERE WID = {wallet_id};
            """
        )
        cursor.execute("COMMIT")
        cursor.close()
        return jsonify({"message": "success"}), 201
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

