# Automatización S4 Servicio Administrado de Conectividad

## Descripción

Automatización desarrollada en Python para generar y distribuir automáticamente el reporte diario del servicio S4 desde Kibana.

El proceso realiza las siguientes actividades:

1. Accede a Kibana.
2. Inicia sesión automáticamente.
3. Selecciona el Workspace correspondiente.
4. Accede al dashboard:
   - S4 SERVICIO ADMINISTRADO DE CONECTIVIDAD
5. Aplica el filtro de fecha:
   - Today
6. Genera el reporte PDF.
7. Descarga el reporte.
8. Guarda el PDF localmente.
9. Envía el reporte mediante Outlook.
10. Registra la ejecución en un archivo de log.

---

## Arquitectura

### Config

Archivo encargado de centralizar parámetros de configuración.

```python
Config
```

Contiene:

- Usuario Kibana
- Contraseña Kibana
- URL Kibana
- Ruta de reportes
- Ruta de logs

---

### Logger

Encargado de registrar eventos y errores.

```python
Logger
```

Ejemplos de eventos registrados:

- Inicio de ejecución
- Login exitoso
- Generación de PDF
- Envío de correo
- Errores

---

### KibanaClient

Encapsula toda la automatización de Playwright.

```python
KibanaClient
```

Responsabilidades actuales:

- Login
- Selección de Workspace
- Apertura del dashboard
- Aplicación de filtros
- Apertura de menú Share
- Exportación del PDF
- Descarga del reporte

Métodos:

```python
login()
seleccionar_espacio()
abrir_dashboard()
aplicar_filtro_today()
abrir_share()
abrir_export()
exportar_pdf()
generar_reporte()
ejecutar()
```

---

### OutlookClient

Encargado del envío de correo.

```python
OutlookClient
```

Responsabilidades:

- Crear correo
- Adjuntar reporte
- Enviar correo
- Registrar eventos relacionados

---

### ReporteS4

Clase responsable de coordinar el flujo de negocio.

```python
ReporteS4
```

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

### Main

Punto de entrada de la aplicación.

```python
main()
```

---

## Estructura del proyecto

```text
S4Automation
│
├── generar_reporte.py
├── config.py
├── logger.py
├── kibana_client.py
├── outlook_client.py
├── reporte_s4.py
│
├── Reportes_S4/
│
└── Reporte_S4.log
```

---

## Requisitos

Instalar dependencias:

```bash
pip install playwright
pip install pywin32
```

Instalar navegador para Playwright:

```bash
python -m playwright install
```

---

## Ejecución manual

```bash
python generar_reporte.py
```

---

## Ejecución programada

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

## Salidas

### Reportes

Ubicación:

```text
Reportes_S4
```

Formato:

```text
S4 SERVICIO ADMINISTRADO DE CONECTIVIDAD v4_DD-MM-AAAA_HH-MM.pdf
```

### Logs

Ubicación:

```text
Reporte_S4.log
```

Ejemplo:

```text
[03-09-2026 12:32:24] Correo enviado correctamente
[03-09-2026 12:32:25] Fin de ejecución
```

---

## Flujo completo

```text
Inicio
↓
Kibana Login
↓
Workspace
↓
Dashboard S4
↓
Today
↓
Share
↓
Export
↓
PDF
↓
Descarga
↓
Outlook
↓
Correo
↓
Fin
```