"""
dialog_helpers.py – Gemeinsame Bausteine für Formular-Dialoge (Create/Edit/Delete).

Nur strukturelle Wiederverwendung; Styles und Verhalten bleiben unverändert.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from typing import Callable, Iterator, Optional

from nicegui import ui

from ui import styles as st
from ui.components import confirm_dialog, notification


class SaveAborted(Exception):
    """Speichern abbrechen, wenn die UI bereits eine Fehlermeldung gezeigt hat."""
    # Wird genutzt, wenn eine Validierung schon eine Notification angezeigt hat.


@contextmanager
def form_dialog(card_style: str) -> Iterator[ui.dialog]:
    """Standard-Dialog mit Karte; liefert das Dialog-Objekt."""
    # Contextmanager spart wiederholten Code in Create/Edit-Dialogen.
    enhanced_style = (
        card_style
        + " box-shadow:0 24px 70px rgba(15,23,42,0.22); "
        "border:1px solid #e2e8f0;"
    )
    with ui.dialog() as dialog, ui.card().style(enhanced_style):
        yield dialog


def dialog_title(text: str, *, style: str | None = None) -> None:
    # Einheitlicher Dialogtitel mit optionalem Sonderstyle.
    ui.label(text).style(
        style or (st.DIALOG_TITLE + " letter-spacing:-0.3px;")
    )


def dialog_actions(
    dialog: ui.dialog,
    on_save: Callable,
    *,
    save_label: str = "Speichern",
    cancel_label: str = "Abbrechen",
    row_classes: str = "justify-end gap-3 mt-4",
    row_style: str = "",
    save_props: str = "color=primary",
) -> None:
    """Abbrechen- und Speichern-Zeile (wie in den Admin-/Student-Dialogen)."""
    # Buttons unten rechts: Abbrechen schließt sofort, Speichern ruft Callback auf.
    row = ui.row().classes(row_classes)
    if row_style:
        row.style(row_style)
    with row:
        ui.button(cancel_label, on_click=dialog.close).props("flat no-caps").style(
            "height:40px; border-radius:12px; color:#64748b; font-weight:600;"
        )
        ui.button(save_label, on_click=on_save).props(f"{save_props} unelevated no-caps").style(
            "height:40px; border-radius:12px; font-weight:700; padding:0 18px;"
        )


def run_save(
    dialog: ui.dialog,
    on_saved: Optional[Callable],
    action: Callable[[], None],
    *,
    success_message: str,
    error_prefix: str = "Fehler",
) -> None:
    """Führt Speicher-Logik aus, schliesst Dialog und zeigt Meldungen."""
    try:
        # action enthält die konkrete Service-/DAO-Arbeit.
        action()
        notification(success_message, "positive")
        dialog.close()
        if on_saved:
            # on_saved aktualisiert meistens die Tabelle oder navigiert zurück zur Seite.
            on_saved()
    except SaveAborted:
        # Kein zusätzlicher Fehlertext, weil die UI den Grund schon angezeigt hat.
        return
    except Exception as exc:
        notification(f"{error_prefix}: {exc}", "negative")


def delete_and_notify(
    action: Callable[[], None],
    message: str,
    *,
    on_after: Optional[Callable] = None,
    navigate_to: Optional[str] = None,
    notify_type: str = "negative",
    confirm_title: str = "Löschen bestätigen",
    confirm_message: str = "Möchtest du diesen Eintrag wirklich löschen?",
) -> None:
    """Fragt nach Bestätigung, löscht danach und zeigt die Rückmeldung."""
    def confirmed_action() -> None:
        # Erst löschen, dann Feedback anzeigen und optional neu laden/navigieren.
        action()
        notification(message, notify_type)
        if on_after:
            on_after()
        elif navigate_to:
            ui.navigate.to(navigate_to)

    confirm_dialog(confirm_title, confirm_message, confirmed_action).open()


def weight_from_percent_input(weight_input) -> Optional[float]:
    """Gewichtungsfeld (Prozent) → Dezimalwert für GradeService."""
    # UI arbeitet mit Prozent, Datenbank/Service mit Dezimalzahl, z. B. 50 % -> 0.5.
    if weight_input.value:
        return float(weight_input.value) / 100.0
    return None


def parse_due_datetime(manual: str) -> Optional[datetime]:
    """Parst TT.MM.JJJJ HH:MM aus dem manuellen Datumsfeld."""
    # Gibt None zurück statt Exception, damit die UI eine freundliche Meldung zeigen kann.
    manual = (manual or "").strip()
    if not manual:
        return None
    try:
        return datetime.strptime(manual, "%d.%m.%Y %H:%M")
    except ValueError:
        return None


def require_due_datetime(manual: str, *, invalid_message: str | None = None) -> Optional[datetime]:
    # Kombination aus Parsen und direkter Fehlermeldung.
    due = parse_due_datetime(manual)
    if due is None:
        notification(
            invalid_message or "Bitte ein gültiges Datum angeben. Format: TT.MM.JJJJ HH:MM",
            "negative",
        )
    return due


def parse_qdate(raw) -> str:
    """
    Quasar-Datumswert → 'YYYY/MM/DD' (für Vorlesungs-Dialoge).
    """
    if not raw:
        return ""
    if isinstance(raw, list):
        # Quasar kann Werte je nach Event als Liste liefern.
        raw = raw[0] if raw else ""
    if isinstance(raw, dict):
        try:
            # Manche Datepicker liefern year/month/day als Dict.
            y, m, d = raw["year"], raw["month"], raw["day"]
            return f"{y:04d}/{m:02d}/{d:02d}"
        except Exception:
            return ""
    s = str(raw).strip()
    if not s:
        return ""
    for fmt in ("%Y/%m/%d", "%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            # Mehrere Formate akzeptieren, intern aber YYYY/MM/DD verwenden.
            return datetime.strptime(s, fmt).strftime("%Y/%m/%d")
        except ValueError:
            continue
    return ""
