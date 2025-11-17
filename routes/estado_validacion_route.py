from flask import Blueprint, request, jsonify
from schemas.estado_validacion_schema import EstadoValidacionSchema
from extensiones import db
from models.estado_validacion_model import EstadoValidacion

estado_validacion_bp=Blueprint(
    'estado_validacion_bp',
    __name__
)

#definir schemas
sEstadoValidacion = EstadoValidacionSchema()
sEstadoValidaciones = EstadoValidacionSchema(many=True)

#endpoints

@estado_validacion_bp.route('/', methods=['POST'])
def crear_estado_validacion():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    estado = sEstadoValidacion.load(request.json)

    try:
        db.session.add(estado)
        db.session.commit()

        return jsonify({"results":"Estado de validacion agregado"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar el estado de validacion: {e}"}),500
    

@estado_validacion_bp.route('/', methods=['GET'])
def ver_estado_validacion():
    
    estados= EstadoValidacion.query.all()

    lista = sEstadoValidaciones.dump(estados)

    return jsonify({"results":lista}),200


@estado_validacion_bp.route('/<estado_validacion_id>', methods=['PUT'])
def modificar_estado_validacion(estado_validacion_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        estado_a_modificar = db.session.get(EstadoValidacion, estado_validacion_id)

        estado_a_modificar.estado_validacion = data.get('estado_validacion', estado_a_modificar.estado_validacion)

        db.session.commit()

        return jsonify({
            'message': 'estado de validacion modificada con éxito',
            'data': {
                'estado_validacion_id': estado_a_modificar.estado_validacion_id,
                'estado_validacion': estado_a_modificar.estado_validacion,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@estado_validacion_bp.route('/<estado_validacion_id>', methods=['DELETE'])
def eliminar_estado_validacion(estado_validacion_id):

    eliminar = EstadoValidacion.query.get(estado_validacion_id)

    if not eliminar:
        return jsonify({"error":"Error. estado de validacion no encontrado"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"estado de validacion eliminado"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el estado de validacion: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500