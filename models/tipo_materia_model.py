from extensiones import db



class TipoMateria(db.Model):
    #ejemplos de datos: obligatira, electiva, CBC, Introductoria 

    __tablename__ = "tipo_materia"

    tipo_materia_id =  db.Column(db.Integer, primary_key=True)
    tipo_materia = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, tipo_materia):
        self.tipo_materia = tipo_materia
