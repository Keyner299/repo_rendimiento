from extensiones import db



class CondicionNota(db.Model):
    #ejemplos de datos: regular,libre,promocionado

    __tablename__ = "condicion_nota"

    condicion_nota_id =  db.Column(db.Integer, primary_key=True)
    condicion_nota = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, condicion_nota):
        self.condicion_nota = condicion_nota
