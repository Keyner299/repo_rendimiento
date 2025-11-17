from extensiones import ma
from models.tipo_documento_evidencia_model import TipoDocumentoEvidencia

class TipoDocumentoEvidenciaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TipoDocumentoEvidencia
        include_fk = True
        load_instance = True