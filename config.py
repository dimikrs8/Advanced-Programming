"""
config.py – Liest Konfiguration aus der .env-Datei.
"""
import os
from dotenv import load_dotenv

# Lädt lokale Einstellungen aus .env in die Umgebungsvariablen.
# Falls eine Variable fehlt, wird unten jeweils ein sinnvoller Entwicklungs-Standard genutzt.
load_dotenv()

# Datenbank-URL: Standard ist eine lokale SQLite-Datei im aktuellen Arbeitsverzeichnis.
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./studentrp.db")

# Secret wird für NiceGUI-Storage verwendet; in Produktion muss es geheim und eindeutig sein.
SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Mail
# MAIL_MODE="mock" schreibt E-Mails in mail.log; "resend" verschickt echte E-Mails.
MAIL_MODE: str = os.getenv("MAIL_MODE", "mock")          # "mock" | "resend"
RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
RESEND_FROM_EMAIL: str = os.getenv("RESEND_FROM_EMAIL", "noreply@studentrp.local")

# AI
# AI_MODE="mock" nutzt einfache Regelantworten; "groq" ruft die externe Groq-API auf.
AI_MODE: str = os.getenv("AI_MODE", "groq")                # "mock" | "groq"
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

# App
# Host 0.0.0.0 macht die App auch im lokalen Netzwerk erreichbar.
APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")

# Port 8080 ist der Standard-Port für die NiceGUI-App.
APP_PORT: int = int(os.getenv("APP_PORT", "8080"))

# Reload ist für Entwicklung praktisch, sollte aber nicht zwingend in Abgaben/Produktion aktiv sein.
APP_RELOAD: bool = os.getenv("APP_RELOAD", "false").lower() == "true"
