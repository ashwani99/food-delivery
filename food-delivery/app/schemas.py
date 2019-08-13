from marshmallow import Schema, fields


class MetaSctrictModeMixin(Schema):
    class Meta:
        strict = True


class UserSchema(MetaSctrictModeMixin):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class LoginSchema(MetaSctrictModeMixin):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class TaskStateSchema(MetaSctrictModeMixin):
    state = fields.Str(attribute='state_name')
    updated_at = fields.DateTime()


class DeliveryTaskSchema(MetaSctrictModeMixin):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True, attribute='task_name')
    priority = fields.Str(required=True, validate=lambda p: p in ('low', 'medium', 'high'))
    destination = fields.Str(required=True)
    created_by = fields.Integer(required=True, dump_only=True, attribute='created_by_user_id')
    created_at = fields.DateTime(dump_only=True)
    last_updated_at = fields.DateTime(dump_only=True)
    states = fields.Nested(TaskStateSchema, many=True, dump_only=True)
    current_state = fields.Nested(TaskStateSchema)
    accepted_by = fields.Integer(required=True, dump_only=True, attribute='accepted_by_user_id')