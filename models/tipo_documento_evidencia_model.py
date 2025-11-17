from extensiones import db



class TipoDocumentoEvidencia(db.Model):
    #ejemplos de datos: analitico,regularidad,alquiler,nota,plan de estudio

    __tablename__ = "tipo_documento_evidencia"

    tipo_documento_evidencia_id =  db.Column(db.Integer, primary_key=True)
    tipo_documento_evidencia = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, tipo_documento_evidencia):
        self.tipo_documento_evidencia = tipo_documento_evidencia
