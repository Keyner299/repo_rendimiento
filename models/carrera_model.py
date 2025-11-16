from extensiones import db
from sqlalchemy import TIMESTAMP
import pendulum


class Carrera(db.Model):

    __tablename__ = "carrera"

    carrera_id =  db.Column(db.Integer(), primary_key=True)
    carrera = db.Column(db.String(50), nullable=False, unique=True)
    universidad_id = db.Column(db.Integer, db.ForeignKey('universidad.universidad_id'), nullable=False)

    modalidad_id = db.Column(db.Integer, db.ForeignKey('modalidad.modalidad_id'), nullable=False)
    modalidad = db.relationship('Modalidad', backref='carrera')

    duracion_anios = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.String(200), nullable=True)

    def hora_argentina():
        return pendulum.now('America/Argentina/Buenos_Aires').replace(microsecond=0, tzinfo=None)
    
    fecha_modif = db.Column(TIMESTAMP(), 
                            nullable=False,
                            default=hora_argentina, 
                            onupdate=hora_argentina)
    user_modif = db.Column(db.String(50), nullable=False)

    def __init__(self, carrera, universidad_id, modalidad_id, duracion_anios, observaciones, user_modif):
        self.carrera = carrera
        self.universidad_id = universidad_id
        self.modalidad_id = modalidad_id
        self.duracion_anios = duracion_anios
        self.observaciones = observaciones
        self.user_modif = user_modif


