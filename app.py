from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

tasks = {
    "to_do": ["Task 1", "Task 2", "Task 3"],
    "doing": ["Task 4"],
    "done": ["Task 5", "Task 6"]
}

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form.get("task")
    tasks["to_do"].append(task)
    return redirect(request.referrer)

@app.route("/move_task", methods=["POST"])
def move_task():
    task = request.form.get("task")
    target_state = request.form.get("column")
    for task_state in tasks:
        if task in tasks[task_state]:
            tasks[task_state].remove(task)
            break
    tasks[target_state].append(task)
    return redirect(request.referrer)

@app.route("/delete_task", methods=["POST"])
def delete_task():
    task = request.form.get("task")
    for state in tasks:
        if task in tasks[state]:
            tasks[state].remove(task)
    return redirect(request.referrer)
