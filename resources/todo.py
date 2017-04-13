import datetime

from flask import Blueprint

from flask_restful import (Resource, Api, reqparse,
                           fields, marshal,
                           marshal_with, url_for)

# from auth import auth
import models

todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'edited': fields.Boolean,
    'completed': fields.Boolean,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}


class TodoList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'edited',
            required=True,
            help='No edit status provided',
            location=['form', 'json'],
            type=bool
        )
        self.reqparse.add_argument(
            'completed',
            required=True,
            help='No completed status provided',
            location=['form', 'json'],
            type=bool
        )
        super().__init__()

    def get(self):
        todos = [marshal(todo, todo_fields)
                 for todo in models.Todo.select()]
        return todos

    @marshal_with(todo_fields)
    # @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return (todo, 201, {
                'Location': url_for('resources.todos.todo', id=todo.id)})


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'edited',
            required=True,
            help='No edit status provided',
            location=['form', 'json'],
            type=bool
        )
        self.reqparse.add_argument(
            'completed',
            required=True,
            help='No completed status provided',
            location=['form', 'json'],
            type=bool
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        todo = models.Todo.get(models.Todo.id == id)
        return todo

    @marshal_with(todo_fields)
    # @auth.login_required
    def put(self, id):
        args = self.reqparse.parse_args()
        args['updated_at'] = datetime.datetime.now()
        query = models.Todo.update(**args).where(models.Todo.id == id)
        query.execute()
        return (models.Todo.get(models.Todo.id == id), 200,
                {'Location': url_for('resources.todos.todo', id=id)})

    # @auth.login_required
    def delete(self, id):
        query = models.Todo.delete().where(models.Todo.id == id)
        query.execute()
        return '', 204, {'Location': url_for('resources.todos.todos')}


todos_api = Blueprint('resources.todos', __name__)
api = Api(todos_api)
api.add_resource(
    TodoList,
    '/api/v1/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/api/v1/todos/<int:id>',
    endpoint='todo'
)
