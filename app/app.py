from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema,fields,ValidationError
import pymysql
import os

pymysql.install_as_MySQLdb()

app = Flask(__name__)

#Conexion con base de datos SQLAlchemy

database_url = os.getenv('DATABASE_URL', 'mysql://root:password@localhost/database')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inicializar marsmallow y sqlalchemy
db = SQLAlchemy(app)
ma = Marshmallow(app)

#definicion de modelos(tablas db)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    mascotas = db.relationship('Mascota', backref='usuario', lazy=True)

    def __init__(self,nombre,email,edad):
        self.nombre = nombre
        self.email = email
        self.edad = edad

class Mascota(db.Model):
    __tablename__ = 'mascotas'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    duenio_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def __init__(self,nombre,especie, duenio_id=None):
        self.nombre = nombre
        self.especie = especie
        self.duenio_id = duenio_id


#schema para marshmallow (usuarios y mascotas)

class MascotaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mascota
        include_fk = True
        load_instance = True

    
class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
    
    mascotas = fields.Nested(MascotaSchema, many=True, only=["nombre","especie"])

with app.app_context():
    db.create_all()


@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    request.json

    sUsuario = UsuarioSchema()

    usu = sUsuario.load(request.json)
    db.session.add(usu)
    db.session.commit()

    return jsonify({"status": 200, "Mensaje": "Usuario creado exitosamente"})


@app.route('/usuarios', methods=['GET'])
def ver_usuarios():
    usuarios = Usuario.query.all()

    sUsuario = UsuarioSchema(many=True)
    lista = sUsuario.dump(usuarios)

    return jsonify ({"results": lista})


@app.route('/usuarios/<int:id>', methods=['PUT'])
def modificar_usuario(id):
    
    Usuario.query.filter_by(id=id).update(request.json)
    db.session.commit()

    return jsonify({"status":200, "message": "usuario modificado"})


    

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usu = Usuario.query.get(id)

    db.session.delete(usu)
    db.session.commit()
    
    return jsonify({"status":200, "message":"usuario eliminado"})
    


@app.route('/mascotas', methods=['POST'])
def crear_mascota():
    request.json

    sMascota = MascotaSchema()

    mas = sMascota.load(request.json)
    db.session.add(mas)
    db.session.commit()

    return jsonify({"status": 200, "Mensaje": "Mascota creada exitosamente"})


@app.route('/mascotas', methods=['GET'])
def ver_mascotas():

    mascotas = Mascota.query.all()

    sMascota = MascotaSchema(many = True)
    lista = sMascota.dump(mascotas)

    return jsonify({"results": lista})


@app.route('/mascotas/<int:id>', methods=['DELETE'])
def eliminar_mascota(id):

    mas = Mascota.query.get(id)

    db.session.delete(mas)
    db.session.commit()

    return jsonify({"status":200, "message":"mascota eliminada"})

@app.route('/mascotas/<int:id>', methods=['PUT'])
def modificar_mascota(id):
    Mascota.query.filter_by(id=id).update(request.json)
    db.session.commit()

    return jsonify({"status":200, "message": "mascota modificada"})
     
     
    



@app.route('/')
def hello():
    return 'PRACTICA DE API REST!'

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)