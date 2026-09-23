import os

from dotenv import load_dotenv

load_dotenv()

class Config:

    # Configuración de login y descarga
    USUARIO = os.getenv("KIBANA_USER")

    PASSWORD = os.getenv("KIBANA_PASSWORD")

    if not USUARIO:

        raise ValueError(
            "Variable KIBANA_USER no encontrada"
        )

    if not PASSWORD:

        raise ValueError(
            "Variable KIBANA_PASSWORD no encontrada"
        )

    URL_KIBANA = "https://172.16.17.55:5601"

    CARPETA_DESCARGAS = (
        r"C:\Users\jose.mendez\OneDrive - Scontinuidad Latam SA de CV\Documentos\S4Automation\Reportes_S4"
    )

    ARCHIVO_LOG = (
        r"C:\Users\jose.mendez\OneDrive - Scontinuidad Latam SA de CV\Documentos\S4Automation\Reporte_S4.log"
    )

    CARPETA_ERRORES = os.path.join(
        r"C:\Users\jose.mendez\OneDrive - Scontinuidad Latam SA de CV\Documentos\S4Automation",
    "Errores"
    )

    MAX_ERRORES = 10