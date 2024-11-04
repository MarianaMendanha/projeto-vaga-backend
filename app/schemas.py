from marshmallow import Schema, fields, validate


class DepartmentSchema(Schema):
    name = fields.Str()


class CollaboratorSchema(Schema):
    full_name = fields.Str()
    have_dependents = fields.Boolean()
