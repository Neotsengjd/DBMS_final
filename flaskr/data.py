from flask import Blueprint, render_template, request, jsonify, abort
from database import db

data = Blueprint("data", __name__, template_folder="flaskr")

# input user_id, insert data information, including price, dname, dtype, ddate, lid, gid
@data.route("/insert_data", methods=["GET", "POST"])
def insert_data():
    try:
        # Get user id
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({'error': 'User id not defined'}), 404
        # Avoid insert data to non-exist user
        cursor = db.connection.cursor()
        cursor.execute(f"SELECT * FROM Datas WHERE UID = {user_id}")
        user_test = cursor.fetchone()
        if not user_test:
            return jsonify({'error': 'User not found'}), 404
        
        # Get necessary data information
        price = request.args.get("price")
        dname = request.args.get("dname")
        dtype = request.args.get("dtype")
        ddate = request.args.get("ddate")
    
        # Get optional data information
        lid = request.args.get("lid")
        gid = request.args.get("gid")
    
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                INSERT INTO Datas (UID, Price, DName, DType, DDate)
                VALUES ({user_id}, {price}, '{dname}', '{dtype}', {ddate});
            """
        )
        cursor.execute('COMMIT')
    
        if lid is not None:
            cursor.execute(
                f"""
                    INSERT INTO DataToLedger (DID, LID)
                    VALUES ((SELECT MAX(DID) FROM Datas), {lid});
                """
            )
            cursor.execute('COMMIT')
        if gid is not None:
            cursor.execute(
                f"""
                    UPDATE Goals
                    SET GCurrentAmount = GCurrentAmount + {price}
                    WHERE GID = {gid}
                """
                )
            cursor.execute('COMMIT')
            cursor.execute(
                f"""
                    INSERT INTO DataToGoal (DID, GID)
                    VALUES ((SELECT MAX(DID) FROM Datas), {gid});
                """
            )
            cursor.execute('COMMIT')
        cursor.close()
        return jsonify({'success':'Insert data successfully'}), 201
    except:
        cursor.execute('ROLLBACK')
        abort(500, 'ERROR 500')

# for a given data_id update price, dname, dtype, ddate, lid, gid
@data.route("update_data", methods=["GET", "POST"])
def update_data():
    try: 
        data_id = request.args.get("data_id")
        # Get necessary data information
        new_data = {
            'price':request.args.get("price"),
            'dname':request.args.get("dname"),
            'dtype':request.args.get("dtype"),
            'ddate':request.args.get("ddate")
        }
        # In update, these are necessary, can be either None or not None
        lid = request.args.get("lid")
        gid = request.args.get("gid")
    
        # Avoid update non-exist data
        cursor = db.connection.cursor()
        cursor.execute(f"SELECT * FROM Datas WHERE DID = {data_id}")
        original_data = cursor.fetchone()
        if not original_data:
            return jsonify({'error': 'Data not found'}), 404
       
       # Get current price
        cursor.execute(
            f"""
                SELECT Price
                FROM Datas
                WHERE DID = {data_id}
            """
        )
        original_price = cursor.fetchone()[0]

       # Update Datas
        update_fields = []
        update_values = []
        for key, value in new_data.items():
            if value is not None:
                update_fields.append(f"{key} = %s")
                update_values.append(value) 
            
        if update_fields:
            update_values.append(data_id)
            update_query = f"UPDATE datas SET {', '.join(update_fields)} WHERE DID = %s"
            cursor.execute(update_query, tuple(update_values))
            cursor.execute('COMMIT')
        
        # Update DataToLedger
        if lid is not None:
            cursor.execute(
                f"""
                    DELETE FROM DataToLedger
                    WHERE DID = {data_id};
                """
            )
            cursor.execute(
                f"""
                    INSERT INTO DataToLedger (DID, LID)
                    VALUES ({data_id}, {lid});
                """
            )   
            cursor.execute('COMMIT')
        else:
            cursor.execute(
                f"""
                    DELETE FROM DataToLedger
                    WHERE DID = {data_id};
                """
            )
            cursor.execute('COMMIT')
            
        # Update DataToGoal table, GCurrentAmount of Goal    
        if gid is not None:
            # Minus original price from GCurrentAmount
            cursor.execute(
                f"""
                    UPDATE Goals
                    SET GCurrentAmount = GCurrentAmount - {original_price}
                    WHERE GID = (SELECT GID FROM DataToGoal WHERE DID = {data_id});
                """
            )
            # Add new price to new Goal's GCurrentAmount
            cursor.execute(
                f"""
                    UPDATE Goals
                    SET GCurrentAmount = GCurrentAmount + (SELECT Price FROM Datas WHERE DID = {data_id})
                    WHERE GID = {gid};
                """
            )
            # Update DataToGoal
            cursor.execute(
                f"""
                    DELETE FROM DataToGoal
                    WHERE DID = {data_id};
                """
            )
            cursor.execute(
                f"""
                    INSERT INTO DataToGoal (DID, GID)
                    VALUES ({data_id}, {gid});
                """
            )   
            cursor.execute('COMMIT')
        # Delete bounding of Data and Goal
        else: 
            cursor.execute(
                f"""
                    UPDATE Goals
                    SET GCurrentAmount = GCurrentAmount - {original_price}
                    WHERE GID = (SELECT GID FROM DataToGoal WHERE DID = {data_id});
                """
            )
            cursor.execute(
                f"""
                    DELETE FROM DataToGoal
                    WHERE DID = {data_id};
                """
            )
            cursor.execute('COMMIT')
        
        cursor.close()
        return jsonify({"Success":"Update data successfully"}), 201
    except:
        cursor.execute('ROLLBACK')
        abort(500, 'ERROR 500')
        
# Get all data information for a given user_id        
@data.route("/get_all_datas", methods=["GET"])
def get_all_datas():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({'error': 'User id not defined'}), 404
        # Avoid show non-exist user's data
        cursor = db.connection.cursor()
        cursor.execute(f"SELECT * FROM Datas WHERE UID = {user_id}")
        user_test = cursor.fetchone()
        if not user_test:
            return jsonify({'error': 'User not found'}), 404
        
        cursor = db.connection.cursor()
        cursor.execute(
            f"""
                SELECT * FROM Datas
            """
        )
        datas = cursor.fetchall()
        result = []
        for data in datas:
            result.append({
                'UID': data[0],
                'DID': data[1],
                'Price': data[2],
                'DName': data[3],
                'DType': data[4],
                'DDate': data[5]
            })
        return jsonify(result), 200
    except:
        cursor.execute("ROLLBACK")
        abort(500, "ERROR 500")

# for a given data_id, delete data 
@data.route('/delete_data',methods=['DELETE', 'GET'])
def delete_data():

    data_id = request.args.get('data_id')
    cursor = db.connection.cursor()
    try:
        cursor.execute(f"""
                       SELECT GID
                       FROM DataToGoal
                       WHERE DID = {data_id};
                       """)
        corresponding_goal = cursor.fetchone()
        if not corresponding_goal:
            cursor.execute(
                f"""
                    DELETE FROM Datas
                    WHERE DID = {data_id};
                """
            )
            cursor.execute("COMMIT")
            cursor.close()
            return "success"
        else:
            gid = corresponding_goal[0]
            cursor.execute(f"""
                           UPDATE Goals
                           SET GCurrentAmount = GCurrentAmount - (SELECT Price FROM Datas WHERE DID = {data_id})
                           WHERE GID = {gid};""")
            cursor.execute(
                f"""
                    DELETE FROM Datas
                    WHERE DID = {data_id};
                """
            )
            cursor.execute("COMMIT")
        # If there exists any data-ledger relation, delete it
        cursor.execute(f"""
                       SELECT LID
                       FROM DataToLedger
                       WHERE DID = {data_id};
                       """)
        corresponding_ledger = cursor.fetchone()
        if corresponding_ledger:
            cursor.execute(f"""
                           DELETE FROM DataToLedger
                           WHERE DID = {data_id};
                           """)
            cursor.execute("COMMIT")
        cursor.close()
        return jsonify({"success":"data deleted successfully"}), 201

    except:
        cursor.execute("ROLLBACK")
        cursor.close()
        abort(500, "ERROR 500")