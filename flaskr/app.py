import os
from database import db
from dotenv import load_dotenv
from flask import Flask, jsonify, abort
from data import data
from user import user
from ledger import ledger
from wallet import wallet
from goal import goal
app = Flask(__name__)

def initialize_app():
    # Initialize the app with the current amount of each goal
    with app.app_context():
        try:
            print(db.connection.cursor())
            cursor = db.connection.cursor()
            cursor.execute(
                f"""
                    UPDATE Goals
                    SET GCurrentAmount = (
                        SELECT COALESCE(SUM(Price), 0)
                        FROM Datas, DataToGoal
                        WHERE Datas.DID = DataToGoal.DID
                        AND DataToGoal.GID = Goals.GID
                    )
                """
            )
            cursor.execute('COMMIT')
    
        except:
            cursor.execute("ROLLBACK")
            cursor.close()
            abort(500, "ERROR 500")
    
load_dotenv()

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

db.init_app(app)
initialize_app() # Initialize the app with the current amount of each goal
app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(ledger, url_prefix="/ledger")
app.register_blueprint(data, url_prefix="/data")
app.register_blueprint(wallet, url_prefix="/wallet")
app.register_blueprint(goal, url_prefix="/goal")


@app.route('/')
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000, debug=True)
    
