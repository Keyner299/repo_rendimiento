from extensiones import db



class EstadoNota(db.Model):
    #ejemplos de datos: aprobada, desaprobada, regular

    __tablename__ = "estado_nota"

    estado_nota_id =  db.Column(db.Integer, primary_key=True)
    estado_nota = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, estado_nota):
        self.estado_nota = estado_nota
