from marshmallow import fields
from extensiones import ma
from models.estado_academico_model import EstadoAcademico

class EstadoAcademicoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EstadoAcademico
        include_fk = True
        load_instance = True