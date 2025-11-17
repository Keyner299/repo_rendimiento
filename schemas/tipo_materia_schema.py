from marshmallow import fields
from extensiones import ma
from models.tipo_materia_model import TipoMateria

class TipoMateriaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoMateria
        include_fk = True
        load_instance = True