from extensiones import db
from uuid import uuid4
from datetime import datetime
from sqlalchemy import TIMESTAMP

class Universidad(db.Model):

    __tablename__ = "universidad"

    universidad_id =  db.Column(db.String(50), primary_key=True, default=lambda:str(uuid4()))
    universidad = db.Column(db.String(50), nullable=False, unique=True)
    observaciones = db.Column(db.String(200), nullable=True)
    fecha_modif = db.Column(TIMESTAMP(), 
                            nullable=False,
                            default=datetime.utcnow, 
                            onupdate=datetime.utcnow)
    user_modif = db.Column(db.String(50), nullable=False)

    #carrera = db.relationship('Carrera', backref='universidad', lazy=True)

    def __init__(self, universidad, observaciones, user_modif):
        self.universidad = universidad
        self.observaciones = observaciones
        self.user_modif = user_modif

