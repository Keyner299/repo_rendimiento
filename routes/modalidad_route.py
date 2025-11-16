from flask import Blueprint, request, jsonify
from schemas.modalidad_schema import ModalidadSchema
from extensiones import db
from models.modalidad_model import Modalidad

modalidad_bp=Blueprint(
    'modalidad_routes',
    __name__
)

#definir schemas
sModalidad = ModalidadSchema()
sModalidades = ModalidadSchema(many=True)

#endpoints

@modalidad_bp.route('/', methods=['POST'])
def crear_modalidad():
    
    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    mod = sModalidad.load(request.json)

    try:
        db.session.add(mod)
        db.session.commit()

        return jsonify({"results":"Modalidad agregada"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar la Modalidad: {e}"}),500
    

@modalidad_bp.route('/', methods=['GET'])
def ver_modalidades():
    
     
    modalidades= Modalidad.query.all()

    lista = sModalidades.dump(modalidades)

    return jsonify({"results":lista}),200


@modalidad_bp.route('/<modalidad_id>', methods=['PUT'])
def modificar_modalidad(modalidad_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        modalidad_a_modificar = db.session.get(Modalidad, modalidad_id)

        modalidad_a_modificar.modalidad = data.get('modalidad', modalidad_a_modificar.modalidad)

        db.session.commit()

        return jsonify({
            'message': 'modalidad modificada con éxito',
            'data': {
                'modalidad_id': modalidad_a_modificar.modalidad_id,
                'modalidad': modalidad_a_modificar.modalidad,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500


@modalidad_bp.route('/<modalidad_id>', methods=['DELETE'])
def eliminar_modalidad(modalidad_id):
    
    eliminar = Modalidad.query.get(modalidad_id)

    if not eliminar:
        return jsonify({"error":"Error. Modalidad no encontrada"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"Modalidad eliminada"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar la modalidad: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
