from app.extensiones import db
from sqlalchemy import TIMESTAMP
import pendulum

class Universidad(db.Model):

    __tablename__ = "universidad"

    universidad_id =  db.Column(db.String(50), primary_key=True)
    universidad = db.Column(db.String(50), nullable=False, unique=True)
    observaciones = db.Column(db.String(200), nullable=True)

    def hora_argentina():
        return pendulum.now('America/Argentina/Buenos_Aires')
    
    fecha_modif = db.Column(TIMESTAMP(), 
                            nullable=False,
                            default=hora_argentina, 
                            onupdate=hora_argentina)
    user_modif = db.Column(db.String(50), nullable=False)

    carrera = db.relationship('Carrera', backref='universidad', lazy=True)

    def __init__(self, universidad, observaciones, user_modif):
        self.universidad = universidad
        self.observaciones = observaciones
        self.user_modif = user_modif

