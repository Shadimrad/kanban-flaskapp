from app import db, app
from flask import request, render_template, redirect, url_for, session, flash, g
from .models import User, Task
from app  import login
from flask_login import current_user, login_required, login_user

# The user_loader decorator tells Flask-Login how to load a user from the database
@login.user_loader
def load_user(user_id):
    """
    This function is called by Flask-Login to load a user from the database.
    It takes the user's ID as a string and returns the corresponding user object.
    If the user ID is invalid, or if the user is not found, it returns None.
    """
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """
    Redirect the user to the Kanban board if they are logged in.
    Otherwise, redirect them to the login page.
    """
    if current_user.is_authenticated:
        tasks = Task.query.filter_by(user_id=current_user.id).all() # Get all tasks for the current user
        return render_template('board.html', title='Kanban Board', tasks=tasks) # Render the Kanban board
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log in the user if they provide valid credentials.
    Otherwise, display an error message.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first() # Get the user from the database
        if user: # If the user exists and the password is correct
            login_user(user) # Log in the user
            return redirect('/kanban') # Redirect the user to the Kanban board
            
        else:
            error_msg = 'Invalid login credentials. Please try again.'
            return render_template('login.html', error=error_msg) # Display the error message
    else:
        return render_template('login.html') # Render the login page

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    Log out the current user and redirect them to the login page.
    """
    session.pop('logged_in', None) # Remove the user from the session
    session.clear() # remove the cookie from the browser
    return redirect('/') # Redirect the user to the login page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Create a new user account if the provided username and password are valid.
    Otherwise, display an error message.
    The username must be unique.
    """
    if request.method == 'POST':
        # Extract the user's input from the request form
        username = request.form['username']
        password = request.form['password']
        # Validate the user's input
        if username and password:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('The username is already taken. Please choose a different one.')
                return redirect(url_for('signup'))
            # Create a new user account in the database
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            # Redirect the user to the login page
            return redirect(url_for('login'))
        else:
            # Display an error message and render the sign-up page again
            error_msg = 'Please fill out all fields.'
            return render_template('signup.html', error=error_msg)
    else:
        # Render the sign-up page
        return render_template('signup.html')


@app.route('/kanban', methods=["GET", "POST"])
@login_required
def kanban():
    '''
    Verifies uniqueness of a new task and adds it to the Kanban board.
    Filters the user's tasks by their status and displays them on the page.
    '''

    # Set the user for the current session
    g.user = current_user

    # Initialize variables
    tasks = None
    error = None

    # If the user submitted a new task, add it to the database
    if request.form:
        try:
            # Check if the task already exists
            if request.form.get("description") in [task.description for task in Task.query.all()]:
                error = "This is on the board! Try something else."
            else:
                # Create a new task with the description and status from the form
                task = Task(description=request.form.get("description"), status=request.form.get("status"), user_id=g.user.id)

                # Add the new task to the database
                db.session.add(task)
                db.session.commit()

        # If the task already exists, display an error message
        except Exception as repeated:
            print("Failed to add task")
            print(repeated)
            db.session.rollback()

    # Get all tasks for the current user
    tasks = Task.query.filter_by(user_id=g.user.id).all()

    # Get all tasks for the current user, filtered by status
    todo = Task.query.filter_by(status='todo', user_id=g.user.id).all()
    progress = Task.query.filter_by(status='progress', user_id=g.user.id).all()
    completed = Task.query.filter_by(status='done', user_id=g.user.id).all()

    # Render the Kanban board
    return render_template("board.html", error=error, tasks=tasks, todo=todo, progress=progress, completed=completed, myuser=current_user)


@app.route("/update", methods=["POST"])
def update():
    '''
    This method updates the task status.
    '''
    try:
        newstatus = request.form.get("newstatus") # Get the new status from the form
        name = request.form.get("name") # Get the task name from the form
        task = Task.query.filter_by(description=name).first() # Get the task from the database

        if not task: # If the task doesn't exist, display an error message
            raise ValueError(f"No task with description '{name}' found")

        task.status = newstatus # Update the task status
        db.session.commit() # Commit the changes to the database
    except Exception as failed:
        db.session.rollback()
        print(f"Couldn't update task status: {failed}")
        # Consider logging the error instead of printing it in the future version
        # log.exception(f"Couldn't update task status: {faield}")
    return redirect(url_for("kanban"))


@app.route("/delete", methods=["POST"])
def delete():
    '''
    This method deletes the task.
    '''
    try:
        description = request.form.get("description") # Get the task description from the form
        task = Task.query.filter_by(description=description).first() # Get the task from the database

        if not task:
            raise ValueError(f"No task with description '{description}' found")
        # If the task doesn't exist, display an error message

        db.session.delete(task) # Delete the task from the database
        db.session.commit() # Commit the changes to the database
    except Exception as fialed:
        db.session.rollback()
        print(f"Couldn't delete task: {fialed}")
        # Consider logging the error instead of printing it
        # log.exception(f"Couldn't delete task: {failed}")
    return redirect(url_for("kanban"))

from app import app 