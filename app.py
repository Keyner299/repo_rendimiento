from flask import Flask
from dotenv import load_dotenv
from extensiones import ma, db
from routes.universidad_route import universidad_bp
from routes.carrera_route import carrera_bp
from routes.modalidad_route import modalidad_bp
from routes.tipo_materia_route import tipoMateria_bp
from routes.regimen_route import regimen_bp
from routes.cuatrimestre_route import cuatrimestre_bp
from routes.estado_nota_route import estado_nota_bp
from routes.condicion_nota_route import condicion_nota_bp
from routes.instancia_evaluacion_route import instancia_evaluacion_bp
from routes.tipo_documento_evidencia_route import tipo_documento_evidencia_bp
from routes.estado_validacion_route import estado_validacion_bp
from routes.estado_academico_route import estado_academico_bp




load_dotenv()

def create_app():

    app = Flask(__name__)

    app.config.from_prefixed_env()

    #Inicializar extenciones(importar)
    db.init_app(app)  #base de datos
    ma.init_app(app)  #marshmallow

    #registrar blueprints
    app.register_blueprint(universidad_bp,url_prefix='/api/v1/universidad')
    app.register_blueprint(carrera_bp,url_prefix='/api/v1/carrera')
    app.register_blueprint(modalidad_bp,url_prefix='/api/v1/modalidad')
    app.register_blueprint(tipoMateria_bp,url_prefix='/api/v1/tipo_materia')
    app.register_blueprint(regimen_bp,url_prefix='/api/v1/regimen')
    app.register_blueprint(cuatrimestre_bp,url_prefix='/api/v1/cuatrimestre')
    app.register_blueprint(estado_nota_bp,url_prefix='/api/v1/estado_nota')
    app.register_blueprint(condicion_nota_bp,url_prefix='/api/v1/condicion_nota')
    app.register_blueprint(instancia_evaluacion_bp,url_prefix='/api/v1/instancia_evaluacion_bp')
    app.register_blueprint(tipo_documento_evidencia_bp,url_prefix='/api/v1/tipo_documento_evidencia_bp')
    app.register_blueprint(estado_validacion_bp,url_prefix='/api/v1/estado_validacion_bp')
    app.register_blueprint(estado_academico_bp,url_prefix='/api/v1/estado_academico_bp')

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)