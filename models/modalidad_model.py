from extensiones import db



class Modalidad(db.Model):

    __tablename__ = "modalidad"

    modalidad_id =  db.Column(db.Integer, primary_key=True)
    modalidad = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, modalidad):
        self.modalidad = modalidad
