from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)

tasks = {
    "to_do": ["Task 1", "Task 2", "Task 3"],
    "doing": ["Task 4"],
    "done": ["Task 5", "Task 6"]
}

@app.route("/")
def login():
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract the user's input from the request form
        username = request.form['username']
        password = request.form['password']
        # Validate the user's input
        if username and password:
            # TO DO -> Create a new user account in your database
            # Redirect the user to the login page
            return redirect(url_for('login'))
        else:
            # Display an error message and render the sign-up page again
            error = 'Please fill out all fields.'
            return render_template('signup.html', error=error)
    else:
        # Render the sign-up page
        return render_template('signup.html')

# @app.route("/add_task", methods=["POST"])
# def add_task():
#     task = request.form.get("task")
#     tasks["to_do"].append(task)
#     return redirect(request.referrer)

# @app.route("/move_task", methods=["POST"])
# def move_task():
#     task = request.form.get("task")
#     target_state = request.form.get("column")
#     for task_state in tasks:
#         if task in tasks[task_state]:
#             tasks[task_state].remove(task)
#             break
#     tasks[target_state].append(task)
#     return redirect(request.referrer)

# @app.route("/delete_task", methods=["POST"])
# def delete_task():
#     task = request.form.get("task")
#     for state in tasks:
#         if task in tasks[state]:
#             tasks[state].remove(task)
#     return redirect(request.referrer)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         conn = sqlite3.connect('users.db')
#         c = conn.cursor()

#         c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
#         user = c.fetchone()

#         conn.close()

#         if user:
#             session['username'] = username
#             return redirect(url_for('home'))
#         else:
#             error = 'Invalid username or password'
#             return render_template('login.html', error=error)
#     else:
#         return render_template('login.html')


# @app.route('/home')
# def home():
#     username = session.get('username')

#     if username:
#         conn = sqlite3.connect('users.db')
#         c = conn.cursor()

#         c.execute('SELECT * FROM users WHERE username = ?', (username,))
#         user = c.fetchone()

#         conn.close()

#         return render_template('home.html', username=user[1])
#     else:
#         return redirect(url_for('login'))
