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

    def to_dict(self):
        return {
            'id': self.id,
            'cod_pl': self.cod_pl,
            's_money': self.s_money,
            'typerec': self.typerec,
            'for_period': self.for_period,
            'i_owner': self.i_owner,
            'supplier': self.supplier,
            'cod_u': self.cod_u,
            'servicename': self.servicename
        }


class MoneySchema(ModelSchema):
    class Meta:
        model = Money


money_schema = MoneySchema()
