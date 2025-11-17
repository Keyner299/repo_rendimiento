from extensiones import db



class Cuatrimestre(db.Model):
    #ejemplos de datos: 1C, 2C, 3C 

    __tablename__ = "cuatrimestre"

    cuatrimestre_id =  db.Column(db.Integer, primary_key=True)
    cuatrimestre = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, cuatrimestre):
        self.cuatrimestre = cuatrimestre
