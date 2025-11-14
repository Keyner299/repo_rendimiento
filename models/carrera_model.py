from app.extensiones import db
from sqlalchemy import TIMESTAMP
import pendulum


class Carrera(db.Model):

    __tablename__ = "carrera"

    carrera_id =  db.Column(db.String(50), primary_key=True)
    universidad_id = db.Column(db.String(50), db.ForeignKey('universidad.universidad_id'), nullable=False)
    carrera = db.Column(db.String(50), nullable=False, unique=True)
    duracion_anios = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.String(200), nullable=True)

    def hora_argentina():
        return pendulum.now('America/Argentina/Buenos_Aires')
    
    fecha_modif = db.Column(TIMESTAMP(), 
                            nullable=False,
                            default=hora_argentina, 
                            onupdate=hora_argentina)
    user_modif = db.Column(db.String(50), nullable=False)

    def __init__(self, carrera, duracion_anios, observaciones, user_modif):
        self.carrera = carrera
        self.duracion_anios = duracion_anios
        self.observaciones = observaciones
        self.user_modif = user_modif


