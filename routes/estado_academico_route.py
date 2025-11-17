from flask import Blueprint, request, jsonify
from schemas.estado_academico_schema import EstadoAcademicoSchema
from extensiones import db
from models.estado_academico_model import EstadoAcademico 

estado_academico_bp=Blueprint(
    'estado_academico_bp',
    __name__
)

#definir schemas
sEstadoAcademico = EstadoAcademicoSchema()
sEstadoAcademicos = EstadoAcademicoSchema(many=True)

#endpoints

@estado_academico_bp.route('/', methods=['POST'])
def crear_estado_academico():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    estado = sEstadoAcademico.load(request.json)

    try:
        db.session.add(estado)
        db.session.commit()

        return jsonify({"results":"estado academico agregado"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar el estado academico: {e}"}),500
    

@estado_academico_bp.route('/', methods=['GET'])
def ver_estado_academico():
    
    estado= EstadoAcademico.query.all()

    lista = sEstadoAcademicos.dump(estado)

    return jsonify({"results":lista}),200


@estado_academico_bp.route('/<estado_academico_id>', methods=['PUT'])
def modificar_estado_academico(estado_academico_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        estado_a_modificar = db.session.get(EstadoAcademico, estado_academico_id)

        estado_a_modificar.estado_academico = data.get('estado_academico', estado_a_modificar.estado_academico)

        db.session.commit()

        return jsonify({
            'message': 'estado academico modificado con éxito',
            'data': {
                'estado_academico_id': estado_a_modificar.estado_academico_id,
                'estado_academico': estado_a_modificar.estado_academico,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@estado_academico_bp.route('/<estado_academico_id>', methods=['DELETE'])
def eliminar_estado_academico(estado_academico_id):

    eliminar = EstadoAcademico.query.get(estado_academico_id)

    if not eliminar:
        return jsonify({"error":"Error. estado academico no encontrado"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"estado academico eliminado"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el estado academico: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500