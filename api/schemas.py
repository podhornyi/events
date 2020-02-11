from marshmallow import Schema, fields, validate, validates_schema, ValidationError


def get_event_schema(required=True):
    class EventSchema(Schema):
        id = fields.Int(required=required, validate=validate.Range(min=0, max=9999))
        uid = fields.Int(required=required, validate=validate.Range(min=0, max=9999))
        action = fields.Str(required=required, validate=validate.Length(min=4, max=12))

    return EventSchema


event_schema = get_event_schema(False)


class GetEventSchema(event_schema):
    day = fields.DateTime(format='%d-%m-%Y')
    month = fields.DateTime(format='%m-%Y')

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if not data.get('day') and not data.get('month'):
            raise ValidationError('Missing day or month param.')
        if data.get('day') and data.get('month'):
            raise ValidationError('Send one of [day, month] param.')
