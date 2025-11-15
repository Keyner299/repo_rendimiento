#importamos los modelos universidad y carrera aqui antes de que flask los use, para evitar problemas con las relaciones
from .universidad_model import Universidad
from .carrera_model import Carrera