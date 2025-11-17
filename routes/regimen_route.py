from flask import Blueprint, request, jsonify
from schemas.regimen_schema import RegimenSchema
from extensiones import db
from models.regimen_model import Regimen 

regimen_bp=Blueprint(
    'regimen_route',
    __name__
)

#definir schemas
sRegimen = RegimenSchema()
sRegimenes = RegimenSchema(many=True)

#endpoints

@regimen_bp.route('/', methods=['POST'])
def crear_regimen():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    regimen = sRegimen.load(request.json)

    try:
        db.session.add(regimen)
        db.session.commit()

        return jsonify({"results":"Regimen agregado"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar el regimen: {e}"}),500
    

@regimen_bp.route('/', methods=['GET'])
def ver_regimen():
    
    regimenes= Regimen.query.all()

    lista = sRegimenes.dump(regimenes)

    return jsonify({"results":lista}),200


@regimen_bp.route('/<regimen_id>', methods=['PUT'])
def modificar_regimen(regimen_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        regimen_a_modificar = db.session.get(Regimen, regimen_id)

        regimen_a_modificar.regimen = data.get('regimen', regimen_a_modificar.regimen)

        db.session.commit()

        return jsonify({
            'message': 'regimen modificada con éxito',
            'data': {
                'regimen_id': regimen_a_modificar.regimen_id,
                'regimen': regimen_a_modificar.regimen,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@regimen_bp.route('/<regimen_id>', methods=['DELETE'])
def eliminar_regimen(regimen_id):

    eliminar = Regimen.query.get(regimen_id)

    if not eliminar:
        return jsonify({"error":"Error. regimen no encontrado"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"regimen eliminado"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el regimen: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500