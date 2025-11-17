from extensiones import ma
from models.instancia_evaluacion_model import InstanciaEvaluacion

class InstanciaEvaluacionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InstanciaEvaluacion
        include_fk = True
        load_instance = True