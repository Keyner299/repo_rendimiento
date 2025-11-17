from marshmallow import fields
from extensiones import ma
from models.tipo_correlativa_model import TipoCorrelativa

class TipoCorrelativaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoCorrelativa
        include_fk = True
        load_instance = True