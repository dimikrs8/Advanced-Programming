"""
components.py – Wiederverwendbare NiceGUI-Bausteine.
Alle Icon+Text-Kombinationen nutzen explizite div-Flexbox statt ui.row(),
um Quasar-CSS-Konflikte und Overlap zu vermeiden.
"""
from __future__ import annotations
from typing import Callable, Optional
from nicegui import ui
from ui import styles as st


def page_header(
    title: str,
    subtitle: str = "",
    action_label: str = "",
    action_fn: Optional[Callable] = None,
    action_class: str = "",
    action_style: str = "",
):
    """Seitentitel mit optionalem Action-Button."""
    # Wird auf vielen Seiten verwendet, damit Breadcrumb, Titel und Button überall gleich aussehen.
    with ui.element("div").style(
        st.FLEX_PAGE_HEADER
        + " padding-bottom:18px; border-bottom:1px solid #e2e8f0;"
    ):
        with ui.element("div").style(st.FLEX_COLUMN_GAP4):
            # Breadcrumb zeigt den groben Bereich und die aktuelle Seite.
            with ui.element("div").style(st.BREADCRUMB):
                ui.element("span").text = "ACADEMIC"
                ui.element("span").style(st.BREADCRUMB_SEP).text = "›"
                ui.element("span").style(st.BREADCRUMB_ACTIVE).text = title.upper()
            ui.label(title).classes("section-title")
            if subtitle:
                ui.label(subtitle).classes("section-sub")

        if action_label and action_fn:
            # Optionaler Hauptbutton rechts oben, z. B. "+ Nutzer anlegen".
            ui.button(action_label, on_click=action_fn).props(
                "unelevated"
            ).classes(action_class).style(
                "height:44px; border-radius:14px; font-size:13px; font-weight:700; "
                "align-self:flex-start; padding:0 20px; background:#2563eb; color:#fff; "
                "box-shadow:0 12px 26px rgba(37,99,235,0.25);"
                + (f" {action_style}" if action_style else "")
            )


def stat_card(
    label: str,
    value: str,
    subtitle: str = "",
    icon: str = "",
    color: str = "#2563eb",
    on_click: Optional[Callable] = None,
):
    """Statistik-Karte für Dashboards – Icon und Label überlappen nicht."""
    # Karten können optional klickbar sein; dann wird ein Pointer-Cursor gesetzt.
    style = (
        "min-width:220px; flex:1; max-width:320px; "
        "transition: transform 0.18s, box-shadow 0.18s; position:relative; overflow:hidden;"
    )
    if on_click:
        style += " cursor:pointer;"

    with ui.card().classes("stat-card").style(style) as card:
        if on_click:
            # Klick auf die ganze Karte, nicht nur auf einen Button.
            card.on("click", on_click)
            card.style("user-select: none;")

        # Dezente Akzentlinie oben macht Karten leichter unterscheidbar.
        ui.element("div").style(
            f"position:absolute; left:0; top:0; right:0; height:4px; background:{color};"
        )
        with ui.element("div").style(
            "display:flex; flex-direction:row; align-items:center; "
            "justify-content:space-between; width:100%; flex-wrap:nowrap; gap:8px;"
        ):
            ui.label(label).classes("stat-card-label")
            if icon:
                with ui.element("div").style(
                    f"width:38px; height:38px; border-radius:12px; background:{color}14; "
                    "display:flex; align-items:center; justify-content:center; flex-shrink:0;"
                ):
                    ui.icon(icon).style(
                        f"color:{color}; font-size:22px; line-height:1;"
                    )
        ui.label(value).classes("stat-card-title")
        if subtitle:
            ui.label(subtitle).classes("stat-card-sub")


def badge(text: str, color: str = "blue"):
    """Farbiger Status-Badge."""
    # color ist ein einfacher logischer Name; CSS-Klassen definieren das genaue Aussehen.
    color_map = {
        "red":    "badge-red",
        "green":  "badge-green",
        "blue":   "badge-blue",
        "yellow": "badge-yellow",
        "gray":   "badge-gray",
    }
    css = f"badge {color_map.get(color, 'badge-blue')}"
    ui.label(text).classes(css)


def empty_state(message: str, icon: str = "inbox"):
    """Leerer Zustand – wird angezeigt wenn keine Daten vorhanden."""
    # Einheitlicher leerer Zustand verhindert leere Tabellen oder kahle Bereiche.
    with ui.element("div").style(
        "display:flex; flex-direction:column; align-items:center; "
        "justify-content:center; gap:14px; padding:48px 32px; color:#94a3b8; "
        "background:linear-gradient(180deg,#ffffff,#f8fafc); border:1px dashed #cbd5e1; "
        "border-radius:18px; min-height:190px; width:100%; "
        "box-shadow:0 10px 24px rgba(15,23,42,0.04);"
    ):
        with ui.element("div").style(
            "width:64px; height:64px; border-radius:999px; background:#f1f5f9; "
            "display:flex; align-items:center; justify-content:center;"
        ):
            ui.icon(icon).style("font-size:34px; line-height:1; color:#94a3b8;")
        ui.label(message).style(
            "font-size:15px; color:#64748b; font-weight:500; text-align:center;"
        )


def confirm_dialog(title: str, message: str, on_confirm: Callable) -> ui.dialog:
    """Bestätigungsdialog für destruktive Aktionen."""
    # Der Dialog wird zurückgegeben, damit der Aufrufer ihn mit .open() anzeigen kann.
    with ui.dialog() as dialog, ui.card().style(st.DIALOG_CONFIRM):
        with ui.row().classes("items-center gap-3"):
            with ui.element("div").style(
                "width:38px; height:38px; border-radius:12px; background:#fef2f2; "
                "display:flex; align-items:center; justify-content:center;"
            ):
                ui.icon("warning").style("font-size:20px; color:#dc2626;")
            ui.label(title).style(st.DIALOG_CONFIRM_TITLE)
        ui.label(message).style(st.DIALOG_CONFIRM_MSG)
        with ui.row().classes("justify-end gap-3 mt-4"):
            ui.button("Abbrechen", on_click=dialog.close).props("flat")
            ui.button(
                # Erst Aktion ausführen, dann Dialog schließen.
                "Bestätigen", on_click=lambda: (on_confirm(), dialog.close())
            ).props("color=negative")
    return dialog


def notification(message: str, type: str = "positive"):
    """Zeigt eine kurze Benachrichtigung."""
    # Wrapper um ui.notify, damit Position und Timeout überall gleich sind.
    ui.notify(message, type=type, position="top-right", timeout=3000)


def loading_spinner():
    """Lade-Spinner."""
    # Zentrierter Spinner für Bereiche, in denen Daten nachgeladen werden könnten.
    with ui.element("div").style(
        "display:flex; justify-content:center; align-items:center; padding:32px; width:100%;"
    ):
        ui.spinner(size="lg")
