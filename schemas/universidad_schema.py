from marshmallow import fields
from extensiones import ma
from models.universidad_model import Universidad

class UniversidadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Universidad
        include_fk = True
        load_instance = True