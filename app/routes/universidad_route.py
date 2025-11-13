from flask import Blueprint, request, jsonify
from schemas import UniversidadSchema
from extensiones import db
from modelos import Universidad

universidad_bp=Blueprint(
    'universidad_routes',
    __name__
)

#definir schemas
sUniversidad = UniversidadSchema()
sUniversidades = UniversidadSchema(many = True)


#endpoints

@universidad_bp.route('/', methods=['POST'])
def crear_universidad():
        
    if not request.json:
        return jsonify({"Error": "Se requiere Json en el cuerpo de la solicitud"}),400

    uni = sUniversidad.load(request.json)

    try:

        db.session.add(uni)
        db.session.commit()

        return jsonify({"Exito":"Universidad agregada"}),201

    except Exception as e:

        db.session.rollback()
        return jsonify({"error": f"No se pudo guardar la universidad: {str(e)}"}),500

    

@universidad_bp.route('/', methods=['GET'])
def ver_universidades():
    
    universidades = Universidad.query.all()

    lista = sUniversidades.dump(universidades)

    return jsonify({"results": lista}),200


    

@universidad_bp.route('/<universidad_id>', methods=['PUT'])
def modificar_universidad(universidad_id):

    data = request.get_json()
    
    if not request.json:
        return jsonify({"Error": "Se requiere Json en el cuerpo de la solicitud"}),400

    universidad_a_modificar = db.session.get(Universidad, universidad_id)

    universidad_a_modificar.universidad = data.get('universidad', universidad_a_modificar.universidad)
    universidad_a_modificar.observaciones = data.get('observaciones', universidad_a_modificar.observaciones)

    user_modif = data.get('user_modif')
    universidad_a_modificar.user_modif = user_modif

    db.session.commit()

    return jsonify({
            'message': 'Universidad modificada con éxito',
            'data': {
                'universidad_id': universidad_a_modificar.universidad_id,
                'universidad': universidad_a_modificar.universidad,
                'observaciones': universidad_a_modificar.observaciones,
                'user_modif': universidad_a_modificar.user_modif,
            }
        }), 200
    

@universidad_bp.route('/<universidad_id>', methods=['DELETE'])
def eliminar_universidad(universidad_id):
    
    eliminar = Universidad.query.get(universidad_id)

    if not eliminar:
        return jsonify({"error":"Universidad no encontrada"}), 404
    
    try:
        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results": "Universidad eliminada"}),204
    
    except Exception as e:
        print(f"Error al eliminar la universidad: {e}")
        return jsonify({"error": "Error interno del servidor. Intente mas Tarde"}),500


    