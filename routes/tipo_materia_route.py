from flask import Blueprint, request, jsonify
from schemas.tipo_materia_schema import TipoMateriaSchema
from extensiones import db
from models.tipo_materia_model import TipoMateria 

tipoMateria_bp=Blueprint(
    'tipo_materia_routes',
    __name__
)

#definir schemas
sTipoMateria = TipoMateriaSchema()
sTipoMaterias = TipoMateriaSchema(many=True)

#endpoints

@tipoMateria_bp.route('/', methods=['POST'])
def crear_tipo_materia():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    tipo = sTipoMateria.load(request.json)

    try:
        db.session.add(tipo)
        db.session.commit()

        return jsonify({"results":"Tipo de materia agregada"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar el tipo de materia: {e}"}),500
    

@tipoMateria_bp.route('/', methods=['GET'])
def ver_tipo_materia():
    
    tipoMaterias= TipoMateria.query.all()

    lista = sTipoMaterias.dump(tipoMaterias)

    return jsonify({"results":lista}),200


@tipoMateria_bp.route('/<tipo_materia_id>', methods=['PUT'])
def modificar_tipo_materia(tipo_materia_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

        tipo_materia_modificar = db.session.get(TipoMateria, tipo_materia_id)

        tipo_materia_modificar.tipo_materia = data.get('tipo_materia', tipo_materia_modificar.tipo_materia)

        db.session.commit()

        return jsonify({
            'message': 'tipo_materia modificada con éxito',
            'data': {
                'tipo_materia_id': tipo_materia_modificar.tipo_materia_id,
                'tipo_materia': tipo_materia_modificar.tipo_materia,
            }
        }), 200

    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@tipoMateria_bp.route('/<tipo_materia_id>', methods=['DELETE'])
def eliminar_tipo_materia(tipo_materia_id):
    
    eliminar = TipoMateria.query.get(tipo_materia_id)

    if not eliminar:
        return jsonify({"error":"Error. tipo_materia no encontrada"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"tipo de materia eliminada"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el tipo de materia: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500