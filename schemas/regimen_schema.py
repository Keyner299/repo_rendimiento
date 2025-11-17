from marshmallow import fields
from extensiones import ma
from models.regimen_model import Regimen

class RegimenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Regimen
        include_fk = True
        load_instance = True