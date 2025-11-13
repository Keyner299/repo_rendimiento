from flask import Flask
from dotenv import load_dotenv
from extensiones import ma, db
from routes.universidad_route import universidad_bp



load_dotenv()

def create_app():

    app = Flask(__name__)

    app.config.from_prefixed_env()

    #Inicializar extenciones(importar)
    db.init_app(app)  #base de datos
    ma.init_app(app)  #marshmallow

    #registrar blueprints
    app.register_blueprint(universidad_bp,url_prefix='/api/v1/universidad')


    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()

    app.run(debug=True)