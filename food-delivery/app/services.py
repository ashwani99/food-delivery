from flask_jwt_extended import current_user

from app import db
from app.models import DeliveryTask, DeliveryTaskState, Role


def can_task_change_state(old_state, new_state):
    # contains movable states from current state
    state_map = {
        'new': ['accepted', 'cancelled'],
        'accepted': ['completed', 'declined', 'cancelled'],
        'completed': [],
        'declined': ['new'],
        'cancelled': []
    }

    if new_state not in state_map[old_state]:
        return False
    return True


def change_task_state(task, new_state):
    if not can_task_change_state:
        raise Exception('Cannot change {} state {} to {}'.format(task, new_state, task.current_state))

    if new_state == 'cancelled':
        if current_user.role == Role.STORE_MANAGER:
            task.states.append(DeliveryTaskState(task, state=new_state))
        else:
            print('UNAUTHORISED')
            pass # should raise unauthorised error
    else:
        if current_user.role == Role.DELIVERY_AGENT:
            task.states.append(DeliveryTaskState(task, state=new_state))
        else:
            print('BAD REQUEST')
            pass # should raise bad request
    return task


