from playwright.sync_api import sync_playwright
from datetime import datetime
from config import Config
import os

class KibanaClient:

    def __init__(
        self,
        logger,
        usuario,
        password,
        url_kibana,
        carpeta_descargas
    ):

        self.logger = logger
        self.usuario = usuario
        self.password = password
        self.url_kibana = url_kibana
        self.carpeta_descargas = carpeta_descargas

    def obtener_ruta_pdf(self):

        fecha_archivo = datetime.now().strftime(
            "%d-%m-%Y_%H-%M"
        )

        return os.path.join(
            self.carpeta_descargas,
            f"S4 SERVICIO ADMINISTRADO DE CONECTIVIDAD_{fecha_archivo}.pdf"
        )
    
    def login(self,page):

        self.logger.escribir_log(
            "Abriendo Kibana"
        )

        page.goto(
            self.url_kibana
        )

        page.wait_for_timeout(3000)

        self.logger.escribir_log(
            "Ingresando credenciales"
        )

        page.locator(
            "input[type='text']"
        ).fill(
            self.usuario
        )

        page.locator(
            "input[type='password']"
        ).fill(
            self.password
        )

        page.locator(
            "button"
        ).last.click()

        page.wait_for_timeout(5000)

    def seleccionar_espacio(self,page):

        self.logger.escribir_log(
            "Seleccionando espacio Workspace de Verificación"
        )

        page.wait_for_timeout(5000)

        page.get_by_role(
            "link",
            name="Workspace de Verificación"
        ).click()

        page.wait_for_timeout(5000)

    def abrir_dashboard(self,page):

        self.logger.escribir_log(
            "Abriendo lista de Dashboards"
        )

        page.goto(
            "https://172.16.17.55:5601/app/dashboards#/list",
            wait_until="networkidle"
        )

        page.wait_for_timeout(5000)

        self.logger.escribir_log(
            "Abriendo Dashboard S4"
        )

        page.get_by_text(
            "S4 SERVICIO ADMINISTRADO DE CONECTIVIDAD",
            exact=False
        ).first.click()

        page.wait_for_timeout(10000)

    def validar_disponibilidades(self,page):

        metricas = page.locator(
            '[data-test-subj="metric_value"]'
        ).all_text_contents()

        indicadores_disponibilidad = {
            "Disponibilidad del servicio": 1,
            "Disponibilidad por ping": 11,
            "BAN_SWCORE_DC_PRIMARIO": 19,
            "BAN_SWADMIN_DC_PRIMARIO": 22,
            "Disponibilidad L2L TRANSTELCO PRODUCCIÓN": 25,
            "Disponibilidad L2L TRANSTELCO REPLICA": 27,
            "Disponibilidad L2L ALESTRA PRODUCCIÓN": 29,
            "Disponibilidad L2L ALESTRA REPLICA": 31,
            "Disponibilidad Internet": 33
        }

        for nombre, indice in indicadores_disponibilidad.items():

            valor = metricas[indice].strip()

            self.logger.escribir_log(
                f"Validando {nombre}: {valor}"
            )

            if valor != "100.00%":

                raise Exception(
                    f"{nombre} No cumple con la disponibilidad requerida: {valor}"
                )

        self.logger.escribir_log(
            "Validación de disponibilidades exitosa"
        )

    def aplicar_filtro_today(self,page):
        self.logger.escribir_log("Aplicando filtro Today")

        page.locator(
            "[aria-label='Date quick select']"
        ).click()

        page.wait_for_timeout(2000)

        page.get_by_text(
            "Today", exact=True).click()

        page.wait_for_timeout(10000)

    def abrir_share(self,page):

        self.logger.escribir_log("Abriendo Share")

        page.get_by_text(
            "Share",
            exact=True
        ).click()

        page.wait_for_timeout(2000)

    def abrir_export(self, page):
        
        self.logger.escribir_log(
            "Abriendo Export"
        )

        export_btn = page.get_by_text(
            "Export",
            exact=True
        )

        export_btn.wait_for(
            state="visible",
            timeout=10000
        )

        export_btn.click()

        page.wait_for_timeout(2000)

    def exportar_pdf(self, page):

        self.logger.escribir_log(
            "Solicitando PDF"
        )

        page.get_by_text(
            "Export file",
            exact=True
        ).click()

        self.logger.escribir_log(
            "Esperando generación del PDF"
        )

        page.get_by_text(
            "Download report",
            exact=True
        ).wait_for(timeout=300000)

        self.logger.escribir_log(
            "Reporte listo"
        )

        enlace = page.locator(
            "a:has-text('Download report')"
        )

        with page.expect_download(timeout=300000) as download_info:
            enlace.click()

        descarga = download_info.value

        archivo_pdf = self.obtener_ruta_pdf()

        descarga.save_as(archivo_pdf)

        self.logger.escribir_log(
            f"PDF guardado: {archivo_pdf}"
        )

        return archivo_pdf

    def generar_reporte(self,page):

        self.seleccionar_espacio(page)

        self.abrir_dashboard(page)

        self.validar_disponibilidades(page)

        self.aplicar_filtro_today(page)

        self.abrir_share(page)

        self.abrir_export(page)

        return self.exportar_pdf(page)

    def capturar_error(self,page):

            try:

                os.makedirs(
                Config.CARPETA_ERRORES,
                exist_ok=True
                )

                nombre_archivo = os.path.join(
                Config.CARPETA_ERRORES,
                "error_"
                + datetime.now().strftime(
                    "%d-%m-%Y_%H-%M"
                )
                + ".png"
            )

                page.screenshot(
                    path=nombre_archivo,
                    full_page=True
                )

                self.logger.escribir_log(
                    f"Captura de error guardada: {nombre_archivo}"
                )

            except Exception as e:

                self.logger.escribir_log(
                    f"No fue posible generar captura: {e}"
                )

    def ejecutar(self):

        with sync_playwright() as p:

            browser = p.chromium.launch(
                channel="msedge",
                headless=True
            )

            context = browser.new_context(
                ignore_https_errors=True,
                accept_downloads=True
            )

            page = context.new_page()

            try:

                self.login(page)

                archivo_pdf = self.generar_reporte(
                    page
                )

                return archivo_pdf

            except Exception:

                self.capturar_error(
                    page
                )

                raise

            finally:

                context.close()
                browser.close()