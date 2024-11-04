from marshmallow import Schema, fields, validate


class DepartmentSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))

    def get_dict(self):
        return {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
            },
            'required': ['name']
        }


class CollaboratorSchema(Schema):
    full_name = fields.Str(required=True, validate=validate.Length(min=1))
    have_dependents = fields.Bool(missing=False)
    department_id = fields.Int(required=True)

    def get_dict(self):
        return {
            'type': 'object',
            'properties': {
                'full_name': {'type': 'string'},
                'department_id': {'type': 'integer'},
                'have_dependents': {'type': 'boolean'},
            },
            'required': ['full_name', 'department_id']
        }
