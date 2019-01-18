from mongoengine import Document
from mongoengine.fields import IntField, FloatField, StringField
from marshmallow_mongoengine import ModelSchema


class Money(Document):
    meta = {'collection': 'money'}

    id = IntField(primary_key=True)
    cod_pl = IntField()
    s_money = FloatField()
    typerec = IntField()
    for_period = IntField()
    i_owner = IntField()
    supplier = StringField()
    cod_u = IntField()
    servicename = StringField()


class Owner(Document):
    meta = {'collection': 'owner'}

    i_owner = IntField()
    supplier = StringField()


class MoneySchema(ModelSchema):
    class Meta:
        model = Money


money_schema = MoneySchema()
