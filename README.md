# Automatización S4 Servicio Administrado de Conectividad

## Descripción

Automatización desarrollada en Python para generar y distribuir automáticamente el reporte diario del servicio S4 desde Kibana.

El proceso realiza las siguientes actividades:

- Accede a Kibana.
- Inicia sesión automáticamente.
- Selecciona el Workspace correspondiente.
- Accede al dashboard:
  - S4 SERVICIO ADMINISTRADO DE CONECTIVIDAD
- Valida indicadores críticos de disponibilidad.
- Aplica el filtro de fecha:
  - Today
- Genera el reporte PDF.
- Descarga el reporte.
- Guarda el PDF localmente.
- Envía el reporte mediante Outlook.
- Registra la ejecución en un archivo de log.
- Genera evidencia automática ante errores.

---

# Arquitectura

## Config

Archivo encargado de centralizar parámetros de configuración.

Responsabilidades:

- Usuario Kibana.
- Contraseña Kibana (mediante `.env`).
- URL Kibana.
- Rutas de reportes.
- Ruta de logs.
- Ruta de capturas de error.
- Configuración de mantenimiento.

---

## Logger

Encargado de registrar eventos, errores y operaciones de mantenimiento.

Ejemplos de eventos registrados:

- Inicio de ejecución.
- Login exitoso.
- Validación de disponibilidades.
- Generación de PDF.
- Envío de correo.
- Mantenimiento.
- Errores.

---

## Mantenimiento

Encargado de las tareas de mantenimiento preventivo.

Responsabilidades:

- Limpieza automática de PDFs antiguos.
- Limpieza automática de capturas antiguas.
- Control de crecimiento del archivo de log.

Métodos:

```python
limpiar_log()
limpiar_pdfs()
limpiar_errores()
```

---

## KibanaClient

Encapsula toda la automatización de Playwright.

Responsabilidades:

- Login.
- Selección de Workspace.
- Apertura del dashboard.
- Validación de disponibilidades.
- Aplicación de filtros.
- Apertura de menú Share.
- Exportación del PDF.
- Descarga del reporte.
- Captura automática de errores.

Métodos:

```python
login()
seleccionar_espacio()
abrir_dashboard()
validar_disponibilidades()
aplicar_filtro_today()
abrir_share()
abrir_export()
exportar_pdf()
capturar_error()
generar_reporte()
ejecutar()
```

---

## OutlookClient

Encargado del envío de correo.

Responsabilidades:

- Crear correo.
- Adjuntar reporte.
- Generar saludo dinámico.
- Enviar correo.
- Registrar eventos relacionados.

Saludo dinámico:

```text
Antes de las 12:00 -> Buenos días
Después de las 12:00 -> Buenas noches
```

---

## ReporteS4

Clase responsable de coordinar el flujo de negocio.

Flujo:

```text
Kibana
↓
Generación PDF
↓
Outlook
↓
Correo enviado
```

---

## Main

Punto de entrada de la aplicación.

```python
main()
```

---

# Estructura del proyecto

```text
S4Automation
│
├── main.py
├── config.py
├── logger.py
├── mantenimiento.py
├── kibana_client.py
├── outlook_client.py
├── reporte_s4.py
│
├── Reportes_S4/
├── Errores/
│
├── .env
└── Reporte_S4.log
```

---

# Requisitos

Instalar dependencias:

```bash
pip install playwright
pip install pywin32
pip install python-dotenv
```

Instalar navegador para Playwright:

```bash
python -m playwright install
```

Conexión VPN:

```text
GlobalProtect
```

---

# Configuración de credenciales

La configuración se carga desde `.env` en la raíz del proyecto. Para preparar el archivo local, copia `.env.example` como `.env` y completa estos valores:

```text
KIBANA_USER
KIBANA_PASSWORD
KIBANA_URL
REPORTES_DIR
LOG_FILE
ERRORS_DIR
MAX_ERRORS
OUTLOOK_TO
OUTLOOK_CC
```

`REPORTES_DIR`, `LOG_FILE` y `ERRORS_DIR` aceptan rutas absolutas. Si se omiten, se usan ubicaciones predeterminadas junto al proyecto. Los destinatarios de Outlook se separan con punto y coma; `OUTLOOK_TO` es obligatorio para preparar el correo y `OUTLOOK_CC` puede quedar vacío.

```text
KIBANA_USER=TU_USUARIO
KIBANA_PASSWORD=TU_PASSWORD
KIBANA_URL=https://servidor-kibana:5601
REPORTES_DIR=C:/ruta/al/proyecto/Reportes_S4
LOG_FILE=C:/ruta/al/proyecto/Reporte_S4.log
ERRORS_DIR=C:/ruta/al/proyecto/Errores
MAX_ERRORS=10
OUTLOOK_TO=destinatario@empresa.com
OUTLOOK_CC=copia1@empresa.com;copia2@empresa.com
```

No subas `.env` ni credenciales reales al repositorio. El archivo `.env` está excluido mediante:

```text
.gitignore
```

---

# Ejecución manual

```bash
python generar_reporte.py
```

---

# Ejecución programada

La automatización está diseñada para ejecutarse mediante:

```text
Task Scheduler
```

Frecuencia:

```text
Lunes a Viernes
08:00 AM
08:00 PM
```

---

# Mantenimiento automático

Antes de iniciar la generación del reporte se ejecutan tareas preventivas.

## Limpieza de PDFs

Se eliminan automáticamente los PDF con más de 30 días de antigüedad almacenados en:

```text
Reportes_S4
```

---

## Limpieza del log

Cuando el archivo:

```text
Reporte_S4.log
```

supera el tamaño configurado (1 MB por defecto), se reinicia automáticamente.

---

## Limpieza de capturas

La carpeta:

```text
Errores/
```

mantiene únicamente las últimas capturas configuradas mediante:

```python
MAX_ERRORES
```

Las capturas más antiguas son eliminadas automáticamente.

---

## Registro de mantenimiento

Cada ejecución registra en el log las tareas realizadas.

Ejemplo:

```text
[23-09-2026 08:00:01] Mantenimiento: 2 PDF(s) eliminados
[23-09-2026 08:00:01] Mantenimiento: 3 captura(s) eliminada(s)
```

---

# Validación de disponibilidades

Antes de generar el PDF se validan automáticamente los indicadores críticos de disponibilidad.

Indicadores monitoreados:

```text
   Disponibilidad del servicio
   Disponibilidad por ping
   BAN_SWCORE_DC_PRIMARIO
   BAN_SWADMIN_DC_PRIMARIO
   Disponibilidad L2L TRANSTELCO PRODUCCIÓN
   Disponibilidad L2L TRANSTELCO REPLICA
   Disponibilidad L2L ALESTRA PRODUCCIÓN
   Disponibilidad L2L ALESTRA REPLICA
   Disponibilidad Internet
```

Condición requerida:

```text
100.00%
```

Si alguno de los indicadores es menor a:

```text
100.00%
```

entonces:

```text
Se detiene el proceso
Se registra el error
Se genera captura automática
No se genera el PDF
No se envía correo
```

---

# Capturas automáticas de error

Cuando ocurre una excepción durante la ejecución:

- Se genera una captura de pantalla automática.
- Se almacena evidencia visual.
- Se registra la ruta en el log.

Ubicación:

```text
Errores/
```

Formato:

```text
error_DD-MM-AAAA_HH-MM-SS.png
```

Ejemplo:

```text
Errores/error_23-09-2026_13-15-22.png
```

---

# Salidas

## Reportes

Ubicación:

```text
Reportes_S4
```

Formato:

```text
S4 SERVICIO ADMINISTRADO DE CONECTIVIDAD_DD-MM-AAAA_HH-MM.pdf
```

---

## Logs

Ubicación:

```text
Reporte_S4.log
```

Ejemplo:

```text
[23-09-2026 14:31:25] Validación de disponibilidades exitosa
[23-09-2026 14:32:20] Correo enviado correctamente
[23-09-2026 14:32:20] Fin de ejecución
```

---

# Flujo completo

```text
Inicio
↓
Mantenimiento
↓
Login Kibana
↓
Workspace
↓
Dashboard S4
↓
Validación de disponibilidades
↓
Filtro Today
↓
Share
↓
Export
↓
Generación PDF
↓
Descarga
↓
Outlook
↓
Correo
↓
Fin
```

---

# Estado actual

## Versión estable

Características implementadas:

- Arquitectura POO.
- Configuración mediante `.env`.
- Generación automática de PDF.
- Envío automático por Outlook.
- Validación automática de disponibilidades.
- Capturas automáticas de error.
- Limpieza automática de reportes.
- Limpieza automática de logs.
- Limpieza automática de capturas.
- Ejecución automática mediante Task Scheduler.
- Gestión mediante Git y GitHub.

Estado:

```text
Producción
Estable
```
