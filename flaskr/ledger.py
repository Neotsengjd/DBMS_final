from flask import Blueprint, render_template, request, abort, jsonify
from database import db

ledger = Blueprint("ledger", __name__)

# input wallet_id, get all ledgers of this wallet including lid and lname
# notice : if you want get all ledger for a user not a wallet, you can use get_all_ledgers(last one in this file)
@ledger.route("/get_ledgers", methods=["GET"])
def get_ledgers():
    wallet_id = request.args.get("wallet_id")
    if not wallet_id:
        return jsonify({"error":"wallet_id not defined"}), 404
    cursor = db.connection.cursor()
    cursor.execute(f"""SELECT * FROM Wallets WHERE WID = {wallet_id};""")
    # Avoid non-exist wallet
    if not cursor.fetchall():
        return jsonify({"error":"wallet not exists"}), 404
    
    cursor.execute(f"""
                   SELECT *
                   FROM Ledgers
                   WHERE WID = {wallet_id};
                   """)
    ledgers = cursor.fetchall()
    result = []
    for ledger in ledgers:
        result.append(
            {
                "WID": ledger[0],
                "LID": ledger[1],
                "LName": ledger[2],
            }
        )
    return jsonify(result), 200

# for a given wallet_id, insert a new ledger of it 
@ledger.route("/insert_ledger", methods=["GET", "POST"])
def insert_ledger():
    wallet_id = request.args.get("wallet_id")
    ledger_name = request.args.get("ledger_name")
    
    if not wallet_id or not ledger_name:
        return jsonify({"error":"wallet_id or ledger_name not defined"}), 404
    cursor = db.connection.cursor()
    cursor.execute(f"""SELECT * FROM Wallets WHERE WID = {wallet_id};""")
    # Avoid non-exist wallet
    if not cursor.fetchall():
        return jsonify({"error":"wallet not exists"}), 404
    
    try:
        cursor.execute(
            f"""
                INSERT INTO Ledgers (WID, LName)
                VALUES ({wallet_id}, '{ledger_name}');
            """
        )
        cursor.execute("COMMIT")
        cursor.close()
        return jsonify({"success":"ledger inserted"}), 201
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

# for a given ledger_id, delete ledger
@ledger.route("/delete_ledger", methods=["DELETE", "GET"])
def delete_ledger():
    ledger_id = request.args.get("ledger_id")
    cursor = db.connection.cursor()
    if not ledger_id:
        return jsonify({"error":"ledger_id not defined"}), 404
    cursor.execute(f"""SELECT * FROM Ledgers WHERE LID = {ledger_id};""")
    if not cursor.fetchall():
        return jsonify({"error":"ledger not exists, pass"}), 404
    
    try:
        cursor.execute(
            f"""
                DELETE FROM Ledgers
                WHERE LID = {ledger_id};
            """
        )
        cursor.execute("COMMIT")
        cursor.execute(f"""
                        SELECT * 
                        FROM DataToLedger
                        WHERE LID = {ledger_id};""")
        if cursor.fetchall():
            cursor.execute(f"""DELETE FROM DataToLedger WHERE LID = {ledger_id};""")
            cursor.execute("COMMIT")
        
        cursor.close()
        return jsonify({"success":"ledger deleted successfully"}), 200
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

# for a given ledger_id, update WID and LName of this ledger
@ledger.route("/update_ledger", methods=["PUT", "GET"])
def update_ledger():
    ledger_id = request.args.get("ledger_id")
    cursor = db.connection.cursor()
    if not ledger_id:
        return jsonify({"error":"ledger_id not defined"}), 404
    cursor.execute(f"""
                    SELECT * 
                    FROM Ledgers 
                    WHERE LID = {ledger_id};""")
    if not cursor.fetchall():
        return jsonify({"error":"ledger not exists, pass"}), 404
    
    try:
        new_data = {
            'WID':request.args.get("wallet_id"),
            'LName':request.args.get("ledger_name")
        }
        if not new_data['WID'] or not new_data['LName']:
            return jsonify({"error":"wallet_id or ledger_name not defined"}), 404
        cursor.execute(f"""SELECT * FROM Wallets WHERE WID = {new_data['WID']};""")
        if not cursor.fetchall():
            return jsonify({"error":"wallet not exists"}), 404
        # Update Datas
        update_fields = []
        update_values = []
        for key, value in new_data.items():
            if value is not None:
                update_fields.append(f"{key} = %s")
                update_values.append(value) 
            
        if update_fields:
            update_values.append(ledger_id)
            update_query = f"UPDATE Ledgers SET {', '.join(update_fields)} WHERE LID = %s"
            cursor.execute(update_query, tuple(update_values))
            cursor.execute('COMMIT')
        cursor.close()
        return jsonify({"success":"ledger updated successfully"}), 201
        
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

# for a given ledger_id, get all datas of this ledger
@ledger.route("/get_ledger_all_datas", methods=["GET"])
def get_ledger_all_datas():
    ledger_id = request.args.get("ledger_id")
    cursor = db.connection.cursor()
    if not ledger_id:
        return jsonify({"error":"ledger_id not defined"}), 404
    cursor.execute(f"""SELECT * FROM Ledgers WHERE LID = {ledger_id};""")
    if not cursor.fetchall():
        return jsonify({"error":"ledger not exists, pass"}), 404
    
    cursor.execute(f"""
                   SELECT DID
                   FROM DataToLedger
                   WHERE LID = {ledger_id};
                   """)
    datas = cursor.fetchall()
    result = []
    for data in datas:
        result.append(
            {
                "DID": data[0]
            }
        )
    return jsonify(result), 200

# for a given data_id, get the owner ledger of this data
@ledger.route("/get_my_partner_ledger", methods=["GET"])
def get_my_partner_ledger():
    try:
        data_id= request.args.get("data_id")
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                SELECT LID
                FROM DataToLedger
                WHERE DID = {data_id}
            """
        )
        lid = cursor.fetchall()
        return jsonify(lid), 200
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")

# for a given wallet_id, get all ledgers of this wallet including lid and lname
@ledger.route("/get_wallet_all_ledger", methods=["GET"])
def get_wallet_all_ledger():

    wallet_id = request.args.get("wallet_id")
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT LID, LName
                FROM Ledgers
                WHERE WID = {wallet_id};
            """
        )
        result = cursor.fetchall()
        ledgers = []
        for item in result:
            lid, lname = item
            ledgers.append({
                "LID": lid,
                "LNAME": lname
            })
        cursor.close()
        return jsonify(ledgers),200
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")

# for a given user_id, get all ledgers of this user including lid and lname
@ledger.route('/get_all_ledgers',methods=['GET', 'POST'])
def get_all_ledgers():

    user_id = request.args.get('user_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            f"""
                SELECT WID
                FROM Wallets
                WHERE UID = {user_id};
            """
        )
        result = cursor.fetchall()
        for item in result:
            wid = item[0]
            cursor.execute(
                f"""
                    SELECT LID, LName
                    FROM Ledgers
                    WHERE WID = {wid};
                """
            )
            result = cursor.fetchall()
            ledgers = []
            for item in result:
                lid, lname = item
                ledgers.append({
                    "LID": lid,
                    "LName": lname
                })
            cursor.close()
            return jsonify(ledgers),200
    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")