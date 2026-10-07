# Automatización Reporte Kibana

## Descripción

Automatización desarrollada en Python para generar y distribuir automáticamente un reporte diario desde Kibana.

El proceso realiza las siguientes actividades:

- Accede a Kibana.
- Inicia sesión automáticamente.
- Selecciona el Workspace correspondiente.
- Accede al dashboard:
  - Dashboard_Ejemplo
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
OUTLOOK_ERROR_TO
```

`REPORTES_DIR`, `LOG_FILE` y `ERRORS_DIR` aceptan rutas absolutas.  Los destinatarios de Outlook se separan con punto y coma; `OUTLOOK_TO` es obligatorio para preparar el correo y `OUTLOOK_CC` puede quedar vacío.
`OUTLOOK_ERROR_TO` es el destinatario exclusivo de avisos de falla y no recibe las copias del reporte.

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
OUTLOOK_ERROR_TO=alertas@empresa.com
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

Si el proceso falla, intenta enviar una notificación de error a `OUTLOOK_TO` y `OUTLOOK_CC` mediante Outlook. El aviso incluye el tipo y mensaje del error, la fecha y la ruta del log. Si Outlook no está disponible, el fallo del aviso también queda registrado en el log y se conserva el error original del proceso.

---

# Ejecución programada

La automatización puede programarse con el **Programador de tareas de Windows**. Configura una tarea con dos desencadenadores semanales para ejecutarla de lunes a viernes a las 08:00 y a las 20:00.

```text
Lunes a Viernes
08:00 AM
08:00 PM
```

## Crear la tarea

1. Verifica que el archivo `.env` esté configurado y que la ejecución manual con `python generar_reporte.py` funcione.
2. Abre **Programador de tareas** desde el menú Inicio y selecciona **Crear tarea...** (no **Crear tarea básica...**).
3. En **General**:
   - Asigna un nombre, por ejemplo `Reporte diario S4`.
   - Selecciona la cuenta de Windows que tiene configurado el perfil de Outlook.
   - Selecciona **Ejecutar solo cuando el usuario haya iniciado sesión**. Outlook se automatiza mediante el perfil de escritorio de esa cuenta.
4. En **Desencadenadores**, crea dos desencadenadores:
   - Selecciona **Según una programación** y **Semanal**; marca de lunes a viernes y configura la hora como **08:00:00**.
   - Repite el proceso para un segundo desencadenador a las **20:00:00**, también de lunes a viernes.
5. En **Acciones**, crea una acción **Iniciar un programa**:
   - **Programa o script**: selecciona el ejecutable de Python usado para instalar las dependencias. Si se usa un entorno virtual, selecciona `venv\Scripts\python.exe` dentro de la carpeta del proyecto.
   - **Agregar argumentos**: escribe la ruta completa entre comillas al script `generar_reporte.py`, por ejemplo:

     ```text
     "C:\ruta\al\proyecto\generar_reporte.py"
     ```

   - **Iniciar en (opcional)**: escribe la ruta completa de la carpeta del proyecto, sin comillas, por ejemplo:

     ```text
     C:\ruta\al\proyecto
     ```

     No agregues `generar_reporte.py` en este campo.
6. En **Configuración**, puedes habilitar **Ejecutar la tarea lo antes posible después de que se omita un inicio programado**. Para evitar ejecuciones duplicadas, configura **Si la tarea ya se está ejecutando** como **No iniciar una instancia nueva**.
7. Guarda la tarea y prueba con clic derecho sobre ella y **Ejecutar**. Revisa `Reporte_S4.log` para confirmar el resultado.

## Requisitos para que se ejecute

- El equipo debe estar encendido y conectado a la red; evita que entre en suspensión durante los horarios programados.
- GlobalProtect debe estar conectado para que la aplicación pueda acceder a Kibana.
- La cuenta seleccionada debe tener Outlook configurado y disponible. Si no se puede acceder a Outlook, el resultado se registrará en el log.
- Usa rutas locales válidas para el proyecto y el entorno virtual. El archivo `.env` se lee desde la carpeta del proyecto.

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
