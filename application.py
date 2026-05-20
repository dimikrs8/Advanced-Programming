"""application.py – Setup"""
from nicegui import app, ui
import config
from data_access.db import create_db_and_tables

def setup_app() -> None:
    create_db_and_tables()
    app.storage.secret_key = config.SECRET_KEY
