from extensiones import db



class TipoCorrelativa(db.Model):
    #ejemplos de datos: aprobada,regular 

    __tablename__ = "tipo_correlativa"

    tipo_correlativa_id =  db.Column(db.Integer, primary_key=True)
    tipo_correlativa = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, tipo_correlativa):
        self.tipo_correlativa = tipo_correlativa
