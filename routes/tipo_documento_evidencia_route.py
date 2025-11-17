from flask import Blueprint, request, jsonify
from schemas.tipo_documento_evidencia_schema import TipoDocumentoEvidenciaSchema
from extensiones import db
from models.tipo_documento_evidencia_model import  TipoDocumentoEvidencia

tipo_documento_evidencia_bp=Blueprint(
    'tipo_documento_evidencia_route',
    __name__
)

#definir schemas
sTipoDocumentoEvidencia = TipoDocumentoEvidenciaSchema()
sTipoDocumentoEvidencias = TipoDocumentoEvidenciaSchema(many=True)

#endpoints

@tipo_documento_evidencia_bp.route('/', methods=['POST'])
def crear_tipo_documento_evidencia():

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    
    documento = sTipoDocumentoEvidencia.load(request.json)

    try:
        db.session.add(documento)
        db.session.commit()

        return jsonify({"results":"documento agregado"}),201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar el documento: {e}"}),500
    

@tipo_documento_evidencia_bp.route('/', methods=['GET'])
def ver_tipo_documento_evidencia():
    
    instancia= TipoDocumentoEvidencia.query.all()

    lista = sTipoDocumentoEvidencias.dump(instancia)

    return jsonify({"results":lista}),200


@tipo_documento_evidencia_bp.route('/tipo_documento_evidencia_id>', methods=['PUT'])
def modificar_tipo_documento_evidencia(tipo_documento_evidencia_id):
    
    data = request.get_json()

    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    
    try:

       documento_a_modificar = db.session.get(TipoDocumentoEvidencia,tipo_documento_evidencia_id)

       documento_a_modificar.tipo_documento_evidencia = data.get('tipo_documento_evidencia',TipoDocumentoEvidencia.tipo_documento_evidencia)

       db.session.commit()

       return jsonify({
            'message': 'Instancia modificada con éxito',
            'data': {
                'tipo_documento_evidencia_id':documento_a_modificar.tipo_documento_evidencia_id,
                'tipo_documento_evidencia':documento_a_modificar.tipo_documento_evidencia,
            }
        }), 200


    except Exception as e:
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500
    

#OJO PUEDE TENER REGISTROS EN OTRA TABLA, CAUSA DE PROBLEMA PARA ELIMINAR
@tipo_documento_evidencia_bp.route('/tipo_documento_evidencia_id>', methods=['DELETE'])
def eliminar_tipo_documento_evidencia(tipo_documento_evidencia_id):

    eliminar = TipoDocumentoEvidencia.query.get(tipo_documento_evidencia_id)

    if not eliminar:
        return jsonify({"error":"Error. documento no encontrado"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"documento eliminado"}),204

    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar el documento: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500