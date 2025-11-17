from flask import Blueprint, request, jsonify
from schemas.estado_nota_schema import EstadoNotaSchema
from extensiones import db
from models.estado_nota_model import EstadoNota

estado_nota_bp=Blueprint(
    'estado_nota_route',
    __name__
)

#definir schemas
sEstadoNota = EstadoNotaSchema()
sEstadoNotas = EstadoNotaSchema(many=True)

#endpoints

@estado_nota_bp.route('/', methods=['POST'])
def crear_estado_nota():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    estado = sEstadoNota.load(request.json)

    try:
        db.session.add(estado)
        db.session.commit()

        return jsonify({"results":"Estado de nota agregado"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar el estado de nota: {e}"}),500
    

@estado_nota_bp.route('/', methods=['GET'])
def ver_estado_nota():
    
    estado_notas= EstadoNota.query.all()

    lista = sEstadoNotas.dump(estado_notas)

    return jsonify({"results":lista}),200


@estado_nota_bp.route('/<estado_nota_id>', methods=['PUT'])
def modificar_estado_nota(estado_nota_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        estado_nota_a_modificar = db.session.get(EstadoNota, estado_nota_id)

        estado_nota_a_modificar.estado_nota = data.get('estado_nota', estado_nota_a_modificar.estado_nota)

        db.session.commit()

        return jsonify({
            'message': 'estado de nota modificado con éxito',
            'data': {
                'estado_nota_id': estado_nota_a_modificar.estado_nota_id,
                'estado_nota': estado_nota_a_modificar.estado_nota,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@estado_nota_bp.route('/<estado_nota_id>', methods=['DELETE'])
def eliminar_estado_nota(estado_nota_id):

    eliminar = EstadoNota.query.get(estado_nota_id)

    if not eliminar:
        return jsonify({"error":"Error. estado de nota no encontrado"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"estado de nota eliminado"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el estado de nota: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500