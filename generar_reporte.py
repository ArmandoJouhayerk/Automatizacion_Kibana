import os

from config import Config
from logger import Logger
from outlook_client import OutlookClient
from kibana_client import KibanaClient
from reporte_s4 import ReporteS4
from mantenimiento import Mantenimiento

USUARIO = Config.USUARIO
PASSWORD = Config.PASSWORD

URL_KIBANA = Config.URL_KIBANA

CARPETA_DESCARGAS = Config.CARPETA_DESCARGAS

ARCHIVO_LOG = Config.ARCHIVO_LOG

os.makedirs(CARPETA_DESCARGAS, exist_ok=True)

logger = Logger(ARCHIVO_LOG)

outlook_client = OutlookClient(logger)

kibana_client = KibanaClient(
    logger, 
    USUARIO, 
    PASSWORD, 
    URL_KIBANA, 
    CARPETA_DESCARGAS
    )

reporte = Reporte(
    kibana_client,
    outlook_client,
    logger
    )

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

        errores_eliminados = (
            Mantenimiento.limpiar_errores(
                Config.CARPETA_ERRORES,
                max_archivos=Config.MAX_ERRORES
            )
        )

        logger.escribir_log(
            f"Mantenimiento: {pdfs_eliminados} PDF(s) eliminados"
        )

        logger.escribir_log(
            f"Mantenimiento: {errores_eliminados} captura(s) eliminada(s)"
        )

        logger.escribir_log(
            "Inicio de ejecución"
        )

        reporte.ejecutar()

        logger.escribir_log(
            "Fin de ejecución"
        )

    except Exception as e:

        logger.escribir_log(
            f"ERROR GENERAL: {str(e)}"
        )

        try:
            outlook_client.enviar_notificacion_fallo(e)
        except Exception as error_notificacion:
            logger.escribir_log(
                f"No fue posible enviar la notificación de falla: {error_notificacion}"
            )

        raise


if __name__ == "__main__":
    main()
