from extensiones import ma
from models.condicion_nota_model import CondicionNota

class CondicionNotaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CondicionNota
        include_fk = True
        load_instance = True