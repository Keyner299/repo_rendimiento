from flask import Blueprint, request, jsonify
from schemas.condicion_nota_schema import CondicionNotaSchema
from extensiones import db
from models.condicion_nota_model import CondicionNota 

condicion_nota_bp=Blueprint(
    'condicion_nota_route',
    __name__
)

#definir schemas
sCondicionNota = CondicionNotaSchema()
sCondicionNotas = CondicionNotaSchema(many=True)

#endpoints

@condicion_nota_bp.route('/', methods=['POST'])
def crear_condicion_nota():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    condicionNota = sCondicionNota.load(request.json)

    try:
        db.session.add(condicionNota)
        db.session.commit()

        return jsonify({"results":"Condicion Nota agregada"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar la Condicion de Nota: {e}"}),500
    

@condicion_nota_bp.route('/', methods=['GET'])
def ver_condicion_nota():
    
    CondicionNotas= CondicionNota.query.all()

    lista = sCondicionNotas.dump(CondicionNotas)

    return jsonify({"results":lista}),200


@condicion_nota_bp.route('/<condicion_nota_id>', methods=['PUT'])
def modificar_condicion_nota(condicion_nota_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        condicion_nota_a_modificar = db.session.get(CondicionNota, condicion_nota_id)

        condicion_nota_a_modificar.condicion_nota = data.get('condicion_nota', condicion_nota_a_modificar.condicion_nota)

        db.session.commit()

        return jsonify({
            'message': 'Condicion de Nota modificada con éxito',
            'data': {
                'condicion_nota_id': condicion_nota_a_modificar.condicion_nota_id,
                'condicion_nota': condicion_nota_a_modificar.condicion_nota,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@condicion_nota_bp.route('/<condicion_nota_id>', methods=['DELETE'])
def eliminar_condicion_nota(condicion_nota_id):

    eliminar = CondicionNota.query.get(condicion_nota_id)

    if not eliminar:
        return jsonify({"error":"Error. Condicion de Nota no encontrada"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"Condicion de Nota eliminada"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el Condicion de Nota: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500