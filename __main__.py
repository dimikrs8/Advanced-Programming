"""__main__.py – Einstiegspunkt"""
from nicegui import ui
import config
from application import setup_app

if __name__ in {"__main__", "__mp_main__"}:
    setup_app()
    ui.label("System bereit!")
    ui.run(host=config.APP_HOST, port=config.APP_PORT, title="StudentRP", storage_secret=config.SECRET_KEY, show=True)
