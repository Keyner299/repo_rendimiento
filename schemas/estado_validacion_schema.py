from marshmallow import fields
from extensiones import ma
from models.estado_validacion_model import EstadoValidacion

class EstadoValidacionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EstadoValidacion
        include_fk = True
        load_instance = True