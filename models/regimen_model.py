from extensiones import db



class Regimen(db.Model):
    #ejemplos de datos: anual, cuatrimestral 

    __tablename__ = "regimen"

    regimen_id =  db.Column(db.Integer, primary_key=True)
    regimen = db.Column(db.String(50), nullable=False, unique=True)
    

    
    def __init__(self, regimen):
        self.regimen = regimen
