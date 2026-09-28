import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    USUARIO = os.getenv("KIBANA_USER", "").strip()
    PASSWORD = os.getenv("KIBANA_PASSWORD", "")
    URL_KIBANA = os.getenv("KIBANA_URL", "").strip().rstrip("/")

    CARPETA_DESCARGAS = Path(
        os.getenv("REPORTES_DIR", str(BASE_DIR / "Reportes_S4"))
    ).expanduser().resolve()
    ARCHIVO_LOG = Path(
        os.getenv("LOG_FILE", str(BASE_DIR / "Reporte_S4.log"))
    ).expanduser().resolve()
    CARPETA_ERRORES = Path(
        os.getenv("ERRORS_DIR", str(BASE_DIR / "Errores"))
    ).expanduser().resolve()
    MAX_ERRORES = int(os.getenv("MAX_ERRORS", "10"))

    OUTLOOK_TO = os.getenv("OUTLOOK_TO", "").strip()
    OUTLOOK_CC = os.getenv("OUTLOOK_CC", "").strip()
    OUTLOOK_ERROR_TO = os.getenv("OUTLOOK_ERROR_TO", "").strip()

    if not USUARIO:
        raise ValueError("Variable KIBANA_USER no encontrada")

    if not PASSWORD:
        raise ValueError("Variable KIBANA_PASSWORD no encontrada")

    if not URL_KIBANA:
        raise ValueError("Variable KIBANA_URL no encontrada")

    if MAX_ERRORES < 0:
        raise ValueError("MAX_ERRORS debe ser un entero mayor o igual a 0")
