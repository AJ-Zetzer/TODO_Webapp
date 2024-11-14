from peewee import *
import logging

db = SqliteDatabase('todos.db')

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Todo(Model):
    text = CharField()
    completed = BooleanField()
    order = IntegerField(null=True)
    day = CharField()



    def toggle_completed(self):
        self.completed = not self.completed

    @classmethod
    def all(cls, view = None, search=None, day = None):
        select = Todo.select()
        if view == "active":
            select = select.where(Todo.completed == False)
        if view == "complete":
            select = select.where(Todo.completed == True)

        if search:
            select = select.where(Todo.text.ilike("%" + search + "%"))

        if day:
            select = select.where(Todo.day == day)
        return select.order_by(Todo.order)

    @classmethod
    def find(cls, todo_id):
        return Todo.get(Todo.id == todo_id)

    @classmethod
    def reorder(cls, id_list):
        i = 0
        for tid in id_list:
            todo = Todo.find(int(tid))
            todo.order = i
            i += 1
            todo.save()

    @classmethod
    def get_days(cls):
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


    def deleteTodos(cls):
        todos = cls.all()
        for tid in todos:
            if tid.completed:
                tid.delete()
        return todos

    class Meta:
        database = db