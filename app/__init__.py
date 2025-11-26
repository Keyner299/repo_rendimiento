from flask import Flask
from extensiones import db, ma

def create_app(config_class=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:26729325@localhost:5432/creus-rendimiento"
    
    # Ejemplo común si usas un entorno local sin contraseña:
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/rendimiento_academico"
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)

    return app