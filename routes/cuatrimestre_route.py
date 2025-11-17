from flask import Blueprint, request, jsonify
from schemas.cuatrimestre_schema import CuatrimestreSchema
from extensiones import db
from models.cuatrimestre_model import Cuatrimestre 

cuatrimestre_bp=Blueprint(
    'cuatrimestre_route',
    __name__
)

#definir schemas
sCuatrimestre = CuatrimestreSchema()
sCuatrimestres = CuatrimestreSchema(many=True)

#endpoints

@cuatrimestre_bp.route('/', methods=['POST'])
def crear_cuatrimestre():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    cuatri = sCuatrimestre.load(request.json)

    try:
        db.session.add(cuatri)
        db.session.commit()

        return jsonify({"results":"Cuatrimestre agregado"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar el cuatrimestre: {e}"}),500
    

@cuatrimestre_bp.route('/', methods=['GET'])
def ver_cuatrimestre():
    
    cuatrimestres= Cuatrimestre.query.all()

    lista = sCuatrimestres.dump(cuatrimestres)

    return jsonify({"results":lista}),200


@cuatrimestre_bp.route('/<cuatrimestre_id>', methods=['PUT'])
def modificar_cuatrimestre(cuatrimestre_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        cuatrimestre_a_modificar = db.session.get(Cuatrimestre, cuatrimestre_id)

        cuatrimestre_a_modificar.cuatrimestre = data.get('cuatrimestre', cuatrimestre_a_modificar.cuatrimestre)

        db.session.commit()

        return jsonify({
            'message': 'cuatrimestre modificado con éxito',
            'data': {
                'cuatrimestre_id': cuatrimestre_a_modificar.cuatrimestre_id,
                'cuatrimestre': cuatrimestre_a_modificar.cuatrimestre,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@cuatrimestre_bp.route('/<cuatrimestre_id>', methods=['DELETE'])
def eliminar_cuatrimestre(cuatrimestre_id):

    eliminar = Cuatrimestre.query.get(cuatrimestre_id)

    if not eliminar:
        return jsonify({"error":"Error. cuatrimestre no encontrado"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"cuatrimestre eliminado"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el cuatrimestre: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500