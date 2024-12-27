from flask import Blueprint, render_template, request, redirect, flash, url_for, abort
from database import db

user = Blueprint("user", __name__)

@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_acc = request.form['user_acc']
        user_password = request.form['user_password']

        cursor = db.connection.cursor()
        try:
            # Check if the account already exists
            cursor.execute(f"""
                SELECT COUNT(*)
                FROM Users
                WHERE UAccount = '{user_acc}';
            """)
            result = cursor.fetchone()
            if result[0] > 0:  # If the account already exists
                flash("Account already exists. Please choose a different account.")
                return redirect(url_for('user.register'))

            # Insert the new user into the database
            cursor.execute(f"""
                INSERT INTO Users (UName, UAccount, UPassword)
                VALUES ('{user_name}', '{user_acc}', '{user_password}');
            """)
            db.connection.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for('user.login'))  # Redirect to login after registration
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK")
            cursor.close()
            abort(500, "An error occurred during registration.")
    return render_template('register.html')

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_acc = request.form['user_acc']
        user_password = request.form['user_password']

        cursor = db.connection.cursor()
        try:
            # Query to check if the account and password match
            cursor.execute(f"""
                SELECT UID
                FROM Users
                WHERE UAccount = '{user_acc}' AND UPassword = '{user_password}';
            """)
            result = cursor.fetchone()  # Fetch one result
            cursor.close()

            if result:  # If a matching user is found
                user_id = result[0]
                return redirect(url_for('user.profile', user_id=user_id))
            else:  # If no matching user is found
                flash("Invalid account or password. Please try again.")
                return redirect(url_for('user.login'))
        except Exception as e:
            print(e)
            cursor.execute("ROLLBACK")
            cursor.close()
            abort(500, "An error occurred during login.")
    return render_template('login.html')

@user.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    # Fetch user data from database
    return render_template('profile.html', user_id=user_id)
