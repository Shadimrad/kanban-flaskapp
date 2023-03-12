from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'mysecretkey'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect('/')
        else:
            error = 'Invalid login credentials. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract the user's input from the request form
        username = request.form['username']
        password = request.form['password']
        # Validate the user's input
        if username and password:
            # Create a new user account in the database
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            # Redirect the user to the login page
            return redirect(url_for('login'))
        else:
            # Display an error message and render the sign-up page again
            error = 'Please fill out all fields.'
            return render_template('signup.html', error=error)
    else:
        # Render the sign-up page
        return render_template('signup.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print('Database created successfully')
    app.run(debug=True)
