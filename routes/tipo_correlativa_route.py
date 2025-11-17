from flask import Blueprint, request, jsonify
from schemas.tipo_correlativa_schema import TipoCorrelativaSchema
from extensiones import db
from models.tipo_correlativa_model import TipoCorrelativa 

tipo_correlativa_bp=Blueprint(
    'tipo_correlativa_route',
    __name__
)

#definir schemas
sTipoCorrelativa = TipoCorrelativaSchema()
sTipoCorrelativas = TipoCorrelativaSchema(many=True)

#endpoints

@tipo_correlativa_bp.route('/', methods=['POST'])
def crear_correlativa():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    correlativa = sTipoCorrelativa.load(request.json)

    try:
        db.session.add(correlativa)
        db.session.commit()

        return jsonify({"results":"correlativa agregada"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar la correlativa: {e}"}),500
    

@tipo_correlativa_bp.route('/', methods=['GET'])
def ver_correlativa():
    
    correlativas= TipoCorrelativa.query.all()

    lista = sTipoCorrelativas.dump(correlativas)

    return jsonify({"results":lista}),200


@tipo_correlativa_bp.route('/<tipo_correlativa_id>', methods=['PUT'])
def modificar_correlativa(tipo_correlativa_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        correlativa_a_modificar = db.session.get(TipoCorrelativa, tipo_correlativa_id)

        correlativa_a_modificar.tipo_correlativa = data.get('tipo_correlativa', correlativa_a_modificar.tipo_correlativa)

        db.session.commit()

        return jsonify({
            'message': 'tipo de correlativa modificada con éxito',
            'data': {
                'tipo_correlativa_id': correlativa_a_modificar.tipo_correlativa_id,
                'tipo_correlativa': correlativa_a_modificar.tipo_correlativa,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@tipo_correlativa_bp.route('/<tipo_correlativa_id>', methods=['DELETE'])
def eliminar_correlativa(tipo_correlativa_id):

    eliminar = TipoCorrelativa.query.get(tipo_correlativa_id)

    if not eliminar:
        return jsonify({"error":"Error. tipo de correlativa no encontrada"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"tipo de correlativa eliminada"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar la correlativa: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500