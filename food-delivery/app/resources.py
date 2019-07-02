from flask_restful import Resource
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, current_user

from datetime import datetime

from app import api, db
from .models import User, Role, DeliveryTask, DeliveryTaskState
from .schemas import UserSchema, DeliveryTaskSchema
from .utils import error_object
from .auth import LoginResource, requires_role


class UserList(Resource):
    # @requires_role(Role.ADMIN) working!
    def get(self):
        users = User.query.all()
        return UserSchema().dump(users, many=True).data, 200

    @use_args(UserSchema())
    def post(self, user_args):
        try:
            user = User(user_args['name'], user_args['email'], user_args['password'])
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return error_object('User already exists', 422)
        return UserSchema().dump(user).data, 201


class UserResource(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return error_object('User not found', 404)
        return UserSchema().dump(user).data, 200

    @use_args(UserSchema())
    def put(self, user_args, id):
        user = User.query.get(id)
        if user is None:
            return error_object('User not found', 404)
        for key, value in user_args.items():
            setattr(user, key, value)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return error_object('Email already registered', 422)
        return UserSchema().dump(user).data, 200

    def delete(self, id):
        user = User.query.get(id)
        if user is None:
            return error_object('User not found', 404)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class DeliveryTaskList(Resource):
    @jwt_required
    def get(self):
        tasks = DeliveryTask.query
        if current_user.role == Role.STORE_MANAGER:
            tasks = tasks.filter_by(created_by=current_user).all()
        elif current_user.role == Role.DELIVERY_AGENT:
            tasks = tasks.filter_by(accepted_by=current_user).all()
        else:
            # work-around for the half-baked RBAC system
            # other roles than store-manager and delivery-agents get no tasks
            tasks = []
        return DeliveryTaskSchema(exclude=('states',)).dump(tasks, many=True).data, 200

    @jwt_required
    @use_args(DeliveryTaskSchema(exclude=('states')))
    def post(self, task_args):
        task = current_user.create_delivery_task(
            task_args['task_name'], task_args['destination'], task_args['priority'])
        db.session.add(task)
        db.session.commit()
        return DeliveryTaskSchema(exclude=('states')).dump(task).data, 201


class DeliveryTaskDetail(Resource):
    @jwt_required
    def get(self, id):
        task = DeliveryTask.query.filter_by(id=id, created_by=current_user).first()
        if task is None:
            return error_object('Task not found', 404)
        return DeliveryTaskSchema().dump(task).data, 200

    @jwt_required
    @use_args(DeliveryTaskSchema(exclude=('created_by',)))
    def put(self, task_args, id):
        task = DeliveryTask.query.filter_by(id=id, created_by=current_user)
        if task is None:
            return error_object('Task not found', 404)
        for key, value in task_args:
            setattr(task, key, value)
        task.last_updated_at = datetime.utcnow()
        db.session.add(task)
        db.session.commit()
        return DeliveryTaskSchema().dump(task).data, 200

    @jwt_required
    def delete(self, id):
        task = DeliveryTask.query.filter_by(id=id, created_by=current_user)
        if task is None:
            return error_object('Task not found', 404)
        state = task.last_state
        if state in ('accepted', 'delivered', 'cancelled'):
            return error_object('Cannot cancel task. Task has already been {}'.format(state), 409)
        task.states.append(DeliveryTaskState(state_name='cancelled', task=task))
        task.last_updated_at = datetime.utcnow()
        db.session.add(task)
        db.session.commit()
        return make_response(jsonify(msg='Successfully cancelled task'), 200)


class ChangeTaskStateResource(Resource):
    @jwt_required
    def post(self, id, new_state):
        if new_state == 'cancel':
            task = DeliveryTask.query.filter_by(id=id, created_by=current_user)
        else:
            task = DeliveryTask.query.filter_by(id=id, accepted_by=current_user)
        if task is None:
            return error_object('Task not found', 404)
        elif new_state == 'complete':
            current_user.complete_task(task)
        elif new_state == 'accept':
            current_user.accept_task(task)
        elif new_state == 'decline':
            current_user.decline_task(task)
        elif new_state == 'cancel':
            current_user.cancel_task(task)
        db.session.add(task)
        try:
            db.session.commit()
            return make_response(jsonify(msg='Success!'), 200)
        except Exception:
            return error_object('Error changing state', 500)



api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/user/<int:id>')
api.add_resource(LoginResource, '/login')
api.add_resource(DeliveryTaskList, '/tasks')
api.add_resource(DeliveryTaskDetail, '/task/<int:id>')
api.add_resource(ChangeTaskStateResource, '/task/<int:id>/<string:new_state>')


# endpoints
# /login -> getting access token JWT

# for store managers
# ------------------
# POST /tasks -> create new task
# GET /tasks -> get all tasks created by store manager
# GET /task/<id> -> get particular task detail
# POST /task/<id>/cancel -> cancel particular task
 
# for delivery agents
# -------------------
# GET /tasks/available -> view single new state task with highest priority  ****
# GET /task/<id> -> get particular task detail
# POST /task/<id>/decline -> decline a previously accepted task
# POST /task/<id>/complete -> complete a previously accepted task
# GET /tasks/<id>/accept -> accept a task