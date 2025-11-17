from extensiones import db



class EstadoValidacion(db.Model):
    #ejemplos de datos: anual, cuatrimestral 

    __tablename__ = "estado_validacion"

    estado_validacion_id =  db.Column(db.Integer, primary_key=True)
    estado_validacion = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, estado_validacion):
        self.estado_validacion = estado_validacion
