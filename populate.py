# populate.py
import sys
import os
from sqlalchemy.exc import IntegrityError

# Ajustar el path para importar desde el directorio base de la aplicación
# Esto puede variar según tu estructura.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

# Asume que estas importaciones son válidas en tu estructura de proyecto
from app import create_app  # Función que crea la instancia de la aplicación Flask
from extensiones import db
from models.modalidad_model import Modalidad
from models.tipo_materia_model import TipoMateria
from models.condicion_nota_model import CondicionNota


def seed_data():
    """
    Función principal para poblar las tablas de normalización.
    """
    app = create_app()
    
    # El app_context es necesario para acceder a la base de datos y a las extensiones
    with app.app_context():
        print("Iniciando la siembra de datos...")
        
        try:
            # 1. Poblar Modalidades
            seed_modalidad()
            
            # 2. Poblar Tipos de Materia
            seed_tipo_materia()
            
            # 3. Poblar Condiciones de Nota
            seed_condicion_nota()

            db.session.commit()
            print("\n✅ Siembra de datos completada exitosamente.")
            
        except IntegrityError:
            db.session.rollback()
            print("\n⚠️ Advertencia: Algunos datos ya existen en la base de datos (IntegrityError). Se realizó un rollback.")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ ERROR: Fallo al poblar la base de datos: {e}")
            
# --- Funciones de Seeding Específicas ---

def seed_modalidad():
    """Inserta datos en la tabla Modalidad."""
    modalidades = [
        
        {'modalidad': 'Presencial'}, 
        {'modalidad': 'Virtual'},
        {'modalidad': 'Híbrida'}
    ]
    
    for data in modalidades:
        if not Modalidad.query.filter_by(modalidad=data['modalidad']).first():
            db.session.add(Modalidad(**data))
    print(f"-> Modalidades: {len(modalidades)} registros procesados.")


def seed_tipo_materia():
    """Inserta datos en la tabla TipoMateria."""
    tipos = [
        
        {'tipo_materia': 'Obligatoria'},
        {'tipo_materia': 'Electiva'},
        {'tipo_materia': 'CBC'}
    ]
    
    for data in tipos:
        if not TipoMateria.query.filter_by(tipo_materia=data['tipo_materia']).first():
            db.session.add(TipoMateria(**data))
    print(f"-> Tipos de Materia: {len(tipos)} registros procesados.")


def seed_condicion_nota():
    """Inserta datos en la tabla CondicionNota."""
    condiciones = [

        {'condicion_nota': 'Aprobado'},
        {'condicion_nota': 'Desaprobado'},
        {'condicion_nota': 'Ausente'},
        {'condicion_nota': 'Pendiente'}
    ]
    
    for data in condiciones:
        if not CondicionNota.query.filter_by(condicion_nota=data['condicion_nota']).first():
            db.session.add(CondicionNota(**data))
    print(f"-> Condiciones de Nota: {len(condiciones)} registros procesados.")

if __name__ == '__main__':
    seed_data()