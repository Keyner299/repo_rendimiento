from flask import Blueprint, request, jsonify
from schemas import UniversidadSchema
from extensiones import db

universidad_bp=Blueprint(
    'universidad_routes',
    __name__
)

#definir schemas
sUniversidad = UniversidadSchema()
sUniversidades = UniversidadSchema(many = True)


#endpoints

