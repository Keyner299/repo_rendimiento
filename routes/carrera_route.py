from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from schemas.carrera_schema import CarerraSchema
from extensiones import db
from models.carrera_model import Carrera

carrera_bp=Blueprint(
    'carrera_routes',
    __name__
)

#definir schemas
sCarrera = CarerraSchema()
sCarreras = CarerraSchema(many=True)

#endpoints

@carrera_bp.route('/', methods=['POST'])
def crear_carrera():
    
    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400
    

    try:
        datos = sCarrera.load(request.json)
        car = Carrera(**datos)
        db.session.add(car)
        db.session.commit()

        resultado = sCarrera.dump(car)

        return jsonify({"results":"Carrera agregada",
                        "datos":resultado}),201
    
    except ValidationError as err:
        #manejo de errores de validacion(datos faltante so incorrectos)
        return jsonify({"error": "Error de validacion","datos faltantes o incorrectos": err.messages}), 400
    
    except IntegrityError as err:
        #manejo de errores de BD (nombre ya registrado o invalido)
        db.session.rollback()
        return jsonify({"error": "Nombre de carrera ya registrado o invalido"}),409

    except Exception as e:
        db.session.rollback()
        return jsonify({"error":f"No se pudo agregar la carrera: {e}"}),500

@carrera_bp.route('/', methods=['GET'])
def ver_carreras():

    try: 
    
        carreras= Carrera.query.all()

        if not carreras:
            return jsonify({"error":"No hay carreras registradas"}),200

        lista = sCarreras.dump(carreras)

        return jsonify({"results":lista}),200

    except Exception as e:
        print(f"Error interno al obtener la lista de carreras: {e}")
        return jsonify({"error": "Error interno del servidor, intente mas tarde"}),500

@carrera_bp.route('/<int:carrera_id>', methods=['PUT'])
def modificar_carreras(carrera_id):


    if not request.json:
        return jsonify({"error":"Se requiere Json en el cuerpo de la solicitud"}),400

    data = request.json
    
    try:

        carrera_a_modificar = db.session.get(Carrera, carrera_id)

        if carrera_a_modificar is None:
            return jsonify({"error": f"Carrera con ID: {carrera_id} no encontrada"}),404

        datos_validados = sCarrera.load(data, partial=True, unknown="EXCLUDE")

        for key, value in datos_validados.items():
            setattr(carrera_a_modificar,key,value)


        db.session.commit()

        resultado_serializado = sCarrera.dump(carrera_a_modificar)

        return jsonify({
            'message': 'Carrera modificada con éxito',
            'data': resultado_serializado
        }), 200

    except ValidationError as err:
        # Manejo de errores de validación de Marshmallow 
        return jsonify({
            "error": "Error de validación de datos", 
            "messages": err.messages
        }), 400

    except IntegrityError:
        # Manejo de errores de la BD 
        db.session.rollback()
        return jsonify({"error": "Violación de una restricción de la base de datos (Ej: ID de Universidad o Modalidad inválida)."}), 409
        
    except Exception as e:
        db.session.rollback()
        
        print(f"Error interno al modificar la carrera por ID: {e}") 
        return jsonify({"error": "Error interno del servidor. Intente más tarde"}), 500

@carrera_bp.route('/<int:carrera_id>', methods=['DELETE'])
def eliminar_carrera(carrera_id):
    
    eliminar = Carrera.query.get(carrera_id)

    if not eliminar:
        return jsonify({"error":"Error. Carrera no encontrada"}),404

    try:

        db.session.delete(eliminar)
        db.session.commit()

        return jsonify({"results":"Carrera eliminada"}),204
    
    except IntegrityError as e:
        
        db.session.rollback()
        #Manejo de errores de BD. Este error ocurre si otras tablas dependen de esta Carrera
        print(f"Error: No se puede eliminar la carrera debido a dependencias: {e}")
        return jsonify({
            "error": "Conflicto de eliminación",
            "message": "La carrera no puede ser eliminada porque existen otras entidades (ej. materias o estudiantes) que dependen de ella."
        }), 409


    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar la carrera: {e}")
        return jsonify({"error":"Error interno del servidor. Intente mas tarde"}),500

