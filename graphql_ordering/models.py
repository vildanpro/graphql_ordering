from mongoengine import Document
from mongoengine.fields import IntField, FloatField, ReferenceField, StringField


class Period(Document):

    meta = {'collection': 'period'}
    name = StringField()


class Service(Document):

    meta = {'collection': 'service'}
    name = StringField()
    cod_u = StringField()


class Supplier(Document):

    meta = {'collection': 'supplier'}
    name = StringField()
    i_owner = StringField()


class Money(Document):

    meta = {'collection': 'money'}
    amount = FloatField()
    typerec = IntField()
    period = ReferenceField(Period)
    supplier = ReferenceField(Supplier)
    service = ReferenceField(Service)
