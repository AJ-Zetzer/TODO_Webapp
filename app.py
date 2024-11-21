import json
from flask import Flask, request, render_template, redirect
from src.model.todo import Todo, db
app = Flask(__name__, static_url_path='', static_folder='static')

with db:
    db.create_tables([Todo])


@app.before_request
def _db_connect():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

@app.route('/')
def index():
    return redirect("/todos")

@app.get('/todos')
def all_todos():

    view = request.args.get('view', None)
    search = request.args.get('search', None)
    todos = Todo.all(view, search)
    week = Todo.get_days()
    return render_template("index.html", todos=todos, view = view, search=search, week = week)

@app.post('/todos')
def create_todos():
    view = request.form.get('view', None)
    todo = Todo(text = request.form['todo'], day = request.form['day'], completed=False)
    todo.save()
    return redirect("/todos" + add_view_context(view))

@app.post('/todos/<id>/toggle')
def toggle_todo(id):
    view = request.form.get('view', None)
    todo = Todo.find(int(id))
    todo.toggle_completed()
    todo.save()
    todos = Todo.all(view)
    week = Todo.get_days()
    search = request.args.get('search', None)
    return render_template("main.html", todos=todos, view = view, search=search, week = week)


@app.get('/todos/add/<day>')
def get_create_todo(day):
    view = request.args.get('view', None)
    search = request.args.get('search', None)
    todos = Todo.all(view, search)
    week = Todo.get_days()
    return render_template("main.html", todos=todos, view=view, search=search, week=week, day = day, adding=1)



@app.post('/todos/add/<day>')
def create_todo(day):
    view = request.form.get('view', None)
    todo = Todo(text = "", day = day, completed=False)
    todo.save()
    return redirect("/todos/" + str(todo.get_id()) + "/edit")



@app.post('/todos/delete')
def delete_todos():
    Todo.deleteTodos()
    view = request.args.get('view', None)
    search = request.args.get('search', None)
    todos = Todo.all(view, search)
    week = Todo.get_days()
    return render_template("main.html", todos=todos, view=view, search=search, week=week)
    #return redirect("/todos" + add_view_context(view))

@app.post('/todos/<id>/delete')
def delete_todo(id):
    Todo.deleteTodo(id)
    view = request.args.get('view', None)
    search = request.args.get('search', None)
    todos = Todo.all(view, search)
    week = Todo.get_days()
    return render_template("main.html", todos=todos, view=view, search=search, week=week)






@app.get('/todos/<id>/edit')
def edit_todo(id):
    view = request.args.get('view', None)
    search = request.args.get('search', None)
    todos = Todo.all(view, search)
    week = Todo.get_days()
    return render_template("index.html", todos=todos, view=view, search=search, week=week, editing = int(id))

@app.post('/todos/<id>')
def update_todos(id):
    view = request.form.get('view', None)
    todo = Todo.find(int(id))
    todo.text = request.form['todo']
    todo.save()
    return redirect("/todos" + add_view_context(view))

@app.get('/todos/reorder/<day>')
def show_reorder_ui(day):
    view = request.args.get('view', None)
    todos = Todo.all(view, day=day)
    return render_template("reorder.html", todos=todos)

@app.post('/todos/reorder')
def update_todo_order():
    view = request.args.get('view', None)
    id_list = request.form.getlist("ids")
    Todo.reorder(id_list)
    todos = Todo.all(view)
    week = Todo.get_days()
    return render_template("main.html", todos=todos, view=view, editing=None, week=week)

@app.get('/todos/search')
def show_todo_search():
    view = request.args.get('view', None)
    search = request.args.get('search', None)

    todos = Todo.all(view, search)
    week = Todo.get_days()
    return render_template("main.html", todos=todos, view=view, search=search, searching=1, week=week)

def add_view_context(view):
    return ("?view=" + view) if view is not None else ""


if __name__ == '__main__':
    app.run(port=5000)