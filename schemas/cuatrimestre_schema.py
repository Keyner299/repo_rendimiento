from marshmallow import fields
from extensiones import ma
from models.cuatrimestre_model import Cuatrimestre

class CuatrimestreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cuatrimestre
        include_fk = True
        load_instance = True