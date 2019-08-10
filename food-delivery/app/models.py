from werkzeug.security import generate_password_hash, check_password_hash
from app import db

from enum import IntEnum
from datetime import datetime
import operator

class Role(IntEnum):
    ANNONYMOUS = 0
    DELIVERY_AGENT = 1
    STORE_MANAGER = 2
    ADMIN = 3


priority_name_to_number_map = {
    'high': 2,
    'medium': 1,
    'low': 0
}


class User(db.Model):
    # __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer)

    def __init__(self, name, email, password, role=Role.ANNONYMOUS):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def __setattr__(self, name, value):
        if name == 'password':
            super(User, self).__setattr__(
                'password_hash', generate_password_hash(value))
        else:
            super(User, self).__setattr__(name, value)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def create_delivery_task(self, task_name, destination, priority):
        new_task = DeliveryTask(
            task_name=task_name, destination=destination,
            priority=priority, created_by=self)
        return new_task

    def cancel_task(self, task):
        raise NotImplementedError

    def accept_task(self, task):
        # if self.role == Role.DELIVERY_AGENT:
        # task which is accepted/completed/declined/cancelled cannot be accepted
        if task in self.tasks_accepted or task.current_state in ('completed', 'declined', 'cancelled'):
            return False # should raise some exception

        self.tasks_accepted.append(task)
        task.states.append(DeliveryTaskState(task, state='accepted'))
        return True

    def complete_task(self, task):
        raise NotImplementedError

    def decline_task(self, task):
        # if self.role == Role.DELIVERY_AGENT:
        if task in self.tasks_accepted:
            self.tasks_accepted.remove(task)
            task.states.append(DeliveryTaskState(task, state='declined'))
            return True
        return False


class DeliveryTask(db.Model):
    # __tablename__ = 'delivery_tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(20))
    priority = db.Column(db.String(10), nullable=False)
    destination = db.Column(db.String(140), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    accepted_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    created_by = db.relationship(
        'User', foreign_keys=[created_by_user_id], backref=db.backref('delivery_tasks', lazy=True))
    accepted_by = db.relationship(
        'User', foreign_keys=[accepted_by_user_id], backref=db.backref('tasks_accepted', lazy=True))

    def __init__(self, task_name, destination, priority, created_by):
        self.task_name = task_name
        self.destination = destination
        self.priority = priority
        self.created_by = created_by
        self.states.append(DeliveryTaskState(task=self, state='new'))

    def __repr__(self):
        return '<DeliveryTask {}>'.format(self.task_name)

    @property
    def current_state(self):
        # print('SKDBASDBJKASDBJKASBDKASBKDJBASJKDBJKASDBJKASBDJKASB')
        # latest_state = self.states.order_by(DeliveryTaskState.updated_at.desc()).first()
        # print(latest_state)
        # return latest_state.state_name
        return "not implemented"


class DeliveryTaskState(db.Model):
    # __tablename__ = 'delivery_task_states'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('delivery_task.id'), nullable=False)
    state_name = db.Column(db.String(10), default='new')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    task = db.relationship('DeliveryTask', backref=db.backref('states'))

    def __init__(self, task, state='new'):
        self.state_name = state
        self.task = task
