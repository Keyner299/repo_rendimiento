from extensiones import db



class InstanciaEvaluacion(db.Model):
    #ejemplos de datos: final,parcial,recuperatorio,trabajo practico

    __tablename__ = "instancia_evaluacion"

    instancia_evaluacion_id =  db.Column(db.Integer, primary_key=True)
    instancia_evaluacion = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, instancia_evaluacion):
        self.instancia_evaluacion = instancia_evaluacion
