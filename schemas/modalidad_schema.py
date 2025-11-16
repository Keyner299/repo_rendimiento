from marshmallow import fields
from extensiones import ma
from models.modalidad_model import Modalidad

class ModalidadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Modalidad
        include_fk = True
        load_instance = True