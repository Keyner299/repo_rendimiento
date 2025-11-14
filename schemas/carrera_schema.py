from marshmallow import fields
from app.extensiones import ma
from models.carrera_model import Carrera

class CarerraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Carrera
        include_fk = True
        load_instance = True