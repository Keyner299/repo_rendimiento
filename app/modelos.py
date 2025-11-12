from extensiones import db
from uuid import uuid4

class Universidad(db.Model):

    __tablename__ = "universidad"

    universidad_id =  db.Column(db.String(50), primary_key=True, default=lambda:str(uuid4()))
    universidad = db.Column(db.String(50), nullable=False, unique=True)
    observaciones = db.Column(db.String(200), nullable=True)

    def __init__(self, universidad, observaciones):
        self.universidad = universidad
        self.observaciones = observaciones

