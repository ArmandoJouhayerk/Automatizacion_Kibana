timport os
import time
import win32com.client
from datetime import datetime

from config import Config


class OutlookClient:

    def __init__(self, logger):

        self.logger = logger

    # Función para enviar el reporte por correo electrónico
    def enviar_reporte(
        self,
        archivo_pdf
        ):

        hora_actual = datetime.now().hour

        if hora_actual < 12:
            saludo = "Buenos días"
        else:
            saludo = "Buenas noches"

        self.logger.escribir_log(
            "Iniciando Outlook"
        )

        outlook = win32com.client.Dispatch(
            "Outlook.Application"
        )

        self.logger.escribir_log(
            "Outlook iniciado"
        )

        correo = None

        for intento in range(5):

            try:

                correo = outlook.CreateItem(0)

                self.logger.escribir_log(
                    f"Correo creado en intento {intento + 1}"
                )

                break

            except Exception as error:

                self.logger.escribir_log(
                    f"CreateItem falló intento {intento + 1}: {error}"
                )

                time.sleep(5)

        if correo is None:

            raise Exception(
                "No fue posible crear el correo en Outlook"
            )

        if not Config.OUTLOOK_TO:
            raise ValueError("Variable OUTLOOK_TO no encontrada")

        correo.To = Config.OUTLOOK_TO
        correo.CC = Config.OUTLOOK_CC

        correo.Subject = (
            "Subject -"
            + datetime.now().strftime("%d-%m-%Y_%H-%M")
        )

        correo.Body = f"""{saludo}, equipo:

Cuerpo de correo.
        """

        if not archivo_pdf:

            raise Exception(
                f"archivo_pdf viene vacío: {archivo_pdf}"
            )

        if not os.path.exists(str(archivo_pdf)):

            raise Exception(
                f"No existe el archivo: {archivo_pdf}"
            )

        correo.Attachments.Add(
            archivo_pdf
        )

        self.logger.escribir_log(
            "Reporte agregado al correo"
        )

        correo.Send()

        self.logger.escribir_log(
            "Correo enviado correctamente"
        )

        correo = None
        outlook = None

    def enviar_notificacion_fallo(self, error):
        if not Config.OUTLOOK_ERROR_TO:
            raise ValueError("Variable OUTLOOK_ERROR_TO no encontrada")

        self.logger.escribir_log(
            "Preparando notificación de falla por Outlook"
        )

        outlook = win32com.client.Dispatch(
            "Outlook.Application"
        )

        correo = None

        for intento in range(5):
            try:
                correo = outlook.CreateItem(0)
                break
            except Exception as error_outlook:
                self.logger.escribir_log(
                    f"CreateItem para notificación falló intento {intento + 1}: {error_outlook}"
                )
                if intento < 4:
                    time.sleep(5)

        if correo is None:
            raise RuntimeError(
                "No fue posible crear el correo de notificación de falla en Outlook"
            )

        correo.To = Config.OUTLOOK_ERROR_TO
        correo.CC = ""
        correo.Subject = (
            "FALLA - Automatización- "
            + datetime.now().strftime("%d-%m-%Y_%H-%M")
        )
        correo.Body = (
            "La ejecución de la automatización terminó con error.\n\n"
            f"Error: {type(error).__name__}: {error}\n"
            f"Fecha y hora: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"Archivo de log: {Config.ARCHIVO_LOG}\n"
        )
        correo.Send()

        self.logger.escribir_log(
            "Notificación de falla enviada correctamente"
        )
