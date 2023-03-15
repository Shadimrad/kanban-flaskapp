# kanban-flaskapp
A web-based personalized Kanban (board) made using flask
#### Demo
[Link to the YouTube video](https://youtu.be/kGfiQkaXrAk)

#### app structure:
```
app/
├── __init__.py
├── main_app.py
├── models.py
│
├── templates/
│   ├── base.html
│   ├── board.html
│   ├── login.html
│   └── signup.html
│ 
└── static/
    └── css/
        └── styles.css
```
# Installations

## Virtual Environment set up

    $python3.6 -m venv .venv
    
#### For Linux & macOS:
    $source .venv/bin/activate
    
#### For Windows:
    $env\Scripts\activate
    
## Installing the requirements 
    $pip3 install -r requirements.txt
 
## Running the Flask app
    
#### For Linux & macOS:

    $cd kanban-flaskapp #locate the directory
    $export FLASK_APP=kanban.py
	$export FLASK_DEBUG=true
	$flask run

#### For Windows:

    $cd kanban-flaskapp #locate the directory
    $set FLASK_APP=kanban.py
	$set FLASK_DEBUG=true
	$flask run
    
## Test the app

     $cd kanban-flaskapp #locate the directory
     $python tests.py

#### References
- [Mastering Flask Playlist](https://www.youtube.com/watch?v=stjXX1VMa30&list=PLTgRMOcmRb3OgwZndNgwe4Nhk6lcHY6ZW&index=1)

- [Harvard CS50](https://www.youtube.com/watch?v=oVA0fD13NGI&t=692s)

- [Flask Documentation](https://flask.palletsprojects.com/en/2.2.x/errorhandling/)

- [Error Handeling with Flask](https://pythonprogramming.net/flask-error-handling-basics/)

- [To do list with flask and SQLalchemy](https://www.youtube.com/watch?v=4kD-GRF5VPs)

- [Flask Login](https://flask-login.readthedocs.io/en/latest/)
