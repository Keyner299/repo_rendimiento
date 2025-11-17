from flask import Blueprint, request, jsonify
from schemas.instancia_evaluacion_schema import InstanciaEvaluacionSchema
from extensiones import db
from models.instancia_evaluacion_model import InstanciaEvaluacion 

instancia_evaluacion_bp=Blueprint(
    'instancia_evaluacion_route',
    __name__
)

#definir schemas
sInstanciaEvaluacion = InstanciaEvaluacionSchema()
sInstanciaEvaluaciones = InstanciaEvaluacionSchema(many=True)

#endpoints

@instancia_evaluacion_bp.route('/', methods=['POST'])
def crear_instancia_evaluacion():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    instancia = sInstanciaEvaluacion.load(request.json)

    try:
        db.session.add(instancia)
        db.session.commit()

        return jsonify({"results":"Instancia agregada"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar la Instancia: {e}"}),500
    

@instancia_evaluacion_bp.route('/', methods=['GET'])
def ver_instancia_evaluacion():
    
    instancia= InstanciaEvaluacion.query.all()

    lista = sInstanciaEvaluaciones.dump(instancia)

    return jsonify({"results":lista}),200


@instancia_evaluacion_bp.route('/<instancia_evaluacion_id>', methods=['PUT'])
def modificar_instancia_evaluacion(instancia_evaluacion_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        instancia_evaluacion_a_modificar = db.session.get(InstanciaEvaluacion, instancia_evaluacion_id)

        instancia_evaluacion_a_modificar.instancia_evaluacion = data.get('instancia_evaluacion', instancia_evaluacion_a_modificar.instancia_evaluacion)

        db.session.commit()

        return jsonify({
            'message': 'Instancia modificada con éxito',
            'data': {
                'instancia_evaluacion_id': instancia_evaluacion_a_modificar.instancia_evaluacion_id,
                'instancia_evaluacion': instancia_evaluacion_a_modificar.instancia_evaluacion,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@instancia_evaluacion_bp.route('/<instancia_evaluacion_id>', methods=['DELETE'])
def eliminar_instancia_evaluacion(instancia_evaluacion_id):

    eliminar = InstanciaEvaluacion.query.get(instancia_evaluacion_id)

    if not eliminar:
        return jsonify({"error":"Error. Instancia no encontrada"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"Instancia eliminada"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el Instancia: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500