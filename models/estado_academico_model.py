from extensiones import db



class EstadoAcademico(db.Model):
    #ejemplos de datos: apto, no_apto, observado 

    __tablename__ = "estado_academico"

    estado_academico_id =  db.Column(db.Integer, primary_key=True)
    estado_academico = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, estado_academico):
        self.estado_academico = estado_academico
