from flask import Blueprint, request, jsonify
from schemas.carrera_schema import CarerraSchema
from app.extensiones import db
from models.carrera_model import Carrera

Carrera_bp=Blueprint(
    'carrera_routes',
    __name__
)

#definir schemas
sCarrera = CarerraSchema()
sCarreras = CarerraSchema(many=True)

#endpoints

@Carrera_bp.route('/', methods=['POST'])
def crear_carrera():
    
    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    car = sCarrera.load(request.json)

    try:
        db.session.add(car)
        db.session.commit()

        return jsonify({"results":"Carrera agregada"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar la carrera {e}"}),500

@Carrera_bp.route('/', methods=['GET'])
def ver_carreras():
    
    carreras= Carrera.query.all()

    lista = sCarreras.dump(carreras)

    return jsonify({"results":lista}),200


@Carrera_bp.route('/<carrera_id>', methods=['PUT'])
def modificar_carreras(carrera_id):

    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        carrera_a_modificar = db.session.get(Carrera, carrera_id)

        carrera_a_modificar.carrera = data.get('carrera', carrera_a_modificar.carrera)
        carrera_a_modificar.duracion_anios = data.get('duracion_anios', carrera_a_modificar.duracion_anios)
        carrera_a_modificar.observaciones = data.get('observaciones', carrera_a_modificar.observaciones)

        user_modif = data.get('user_modif')
        carrera_a_modificar.user_modif = user_modif

        db.session.commit()

        return jsonify({
            'message': 'Carrera modificada con éxito',
            'data': {
                'carrera_id': carrera_a_modificar.carrera_id,
                'carrera': carrera_a_modificar.carrera,
                'observaciones': carrera_a_modificar.observaciones,
                'user_modif': carrera_a_modificar.user_modif,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500

@Carrera_bp.route('/<carrera_id>', methods=['DELETE'])
def eliminar_carrera(carrera_id):
    
    eliminar = Carrera.query.get(carrera_id)

    if not eliminar:
        return jsonify({"error":"Error. Carrera no encontrada"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"Carrera eliminada"}),204

    except Exception as e:
        print(f"Error al eliminar la carrera: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500

