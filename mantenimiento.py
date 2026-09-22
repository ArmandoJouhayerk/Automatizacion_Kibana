import os
from datetime import datetime, timedelta


class Mantenimiento:

    @staticmethod
    def limpiar_log(
        archivo_log,
        max_mb=1
    ):

        if not os.path.exists(archivo_log):
            return

        tamano_actual = os.path.getsize(
            archivo_log
        )

        limite = max_mb * 1024 * 1024

        if tamano_actual > limite:

            with open(
                archivo_log,
                "w",
                encoding="utf-8"
            ) as log:

                log.write(
                    "[MANTENIMIENTO] Log reiniciado por exceder el tamaño permitido.\n"
                )

    @staticmethod
    def limpiar_pdfs(
        carpeta,
        dias=30
    ):

        eliminados = 0

        fecha_limite = (
            datetime.now()
            - timedelta(days=dias)
        )

        for archivo in os.listdir(carpeta):

            ruta = os.path.join(
                carpeta,
                archivo
            )

            if not os.path.isfile(ruta):
                continue

            if not archivo.lower().endswith(
                ".pdf"
            ):
                continue

            fecha_modificacion = datetime.fromtimestamp(
                os.path.getmtime(ruta)
            )

            if fecha_modificacion < fecha_limite:

                os.remove(ruta)
                eliminados += 1

        return eliminados