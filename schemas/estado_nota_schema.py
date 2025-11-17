from marshmallow import fields
from extensiones import ma
from models.estado_nota_model import EstadoNota

class EstadoNotaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EstadoNota
        include_fk = True
        load_instance = True