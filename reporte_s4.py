class ReporteS4:

    def __init__(
        self,
        kibana_client,
        outlook_client,
        logger
    ):

        self.kibana_client = kibana_client
        self.outlook_client = outlook_client
        self.logger = logger

    def ejecutar(self):

        archivo_pdf = (
            self.kibana_client.ejecutar()
        )

        self.outlook_client.enviar_reporte(
            archivo_pdf
        )
        