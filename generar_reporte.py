import os
from config import Config
from logger import Logger
from outlook_client import OutlookClient
from kibana_client import KibanaClient
from reporte_s4 import ReporteS4
from mantenimiento import Mantenimiento

# configuracion de login y descarga 
USUARIO = Config.USUARIO
PASSWORD = Config.PASSWORD

URL_KIBANA = Config.URL_KIBANA

CARPETA_DESCARGAS = Config.CARPETA_DESCARGAS

ARCHIVO_LOG = Config.ARCHIVO_LOG

os.makedirs(CARPETA_DESCARGAS, exist_ok=True)

# Inicialización de logger y clientes
logger = Logger(ARCHIVO_LOG)

outlook_client = OutlookClient(logger)

kibana_client = KibanaClient(
    logger, 
    USUARIO, 
    PASSWORD, 
    URL_KIBANA, 
    CARPETA_DESCARGAS
    )

reporte_s4 = ReporteS4(
    kibana_client,
    outlook_client,
    logger
    )


# Función principal
def main():

    try:

        Mantenimiento.limpiar_log(
            ARCHIVO_LOG,
            max_mb=1
        )
        pdfs_eliminados = (
            Mantenimiento.limpiar_pdfs(
                CARPETA_DESCARGAS,
                dias=30
            )
        )

        logger.escribir_log(
            f"Mantenimiento: {pdfs_eliminados} PDF(s) eliminados"
        )

        logger.escribir_log(
            "Inicio de ejecución"
        )

        reporte_s4.ejecutar()

        logger.escribir_log(
            "Fin de ejecución"
        )

    except Exception as e:

        logger.escribir_log(
            f"ERROR GENERAL: {str(e)}"
        )

        raise

# Punto de entrada del script
if __name__ == "__main__":
    main() 