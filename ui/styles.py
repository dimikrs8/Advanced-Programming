"""
styles.py – Wiederverwendbare Inline-Style-Konstanten und kleine Hilfsfunktionen.

Zentralisiert wiederkehrende .style(...)-Werte aus den Page-Modulen,
ohne das visuelle Design zu ändern.
"""
from __future__ import annotations

from nicegui import ui

# ── Farben ────────────────────────────────────────────────────────────────────
# Zentrale Farbwerte, damit gleiche Farben nicht in jeder Datei neu definiert werden.
COLOR_TEXT_PRIMARY = "#0f172a"
COLOR_TEXT_SECONDARY = "#64748b"
COLOR_TEXT_MUTED = "#94a3b8"
COLOR_TEXT_SLATE = "#475569"
COLOR_BLUE = "#2563eb"
COLOR_BLUE_DARK = "#1d4ed8"
COLOR_BLUE_TEXT = "#1e40af"
COLOR_BLUE_TEXT_DARK = "#1e3a8a"
COLOR_BLUE_SOFT = "#dbeafe"
COLOR_GREEN = "#16a34a"
COLOR_RED = "#dc2626"
COLOR_RED_DARK = "#991b1b"
COLOR_BORDER = "#e2e8f0"
COLOR_BORDER_LIGHT = "#f1f5f9"
COLOR_SURFACE = "#ffffff"
COLOR_SURFACE_SOFT = "#f8fafc"
COLOR_BG_BLUE = "#eff6ff"
COLOR_BG_BLUE_BORDER = "#bfdbfe"
COLOR_BG_RED = "#fff1f2"
SHADOW_CARD = "0 12px 30px rgba(15,23,42,0.06)"
SHADOW_CARD_HOVER = "0 18px 40px rgba(15,23,42,0.10)"
RADIUS_CARD = "18px"
RADIUS_INPUT = "12px"

# ── Seiten & Abschnitte ───────────────────────────────────────────────────────
# Wiederverwendbare Textstile für Seitentitel, Untertitel und Abschnittsüberschriften.
PAGE_TITLE = f"font-size:30px; font-weight:800; letter-spacing:-0.7px; color:{COLOR_TEXT_PRIMARY};"
PAGE_SUBTITLE = f"color:{COLOR_TEXT_SECONDARY}; font-size:14px;"
SECTION_HEADING = f"font-size:18px; font-weight:700; color:{COLOR_TEXT_PRIMARY};"
SECTION_HEADING_MT8 = SECTION_HEADING + " margin-top:8px;"
SECTION_HEADING_MB12 = SECTION_HEADING + " margin-bottom:12px;"
CARD_TITLE = SECTION_HEADING

# ── Dialoge ───────────────────────────────────────────────────────────────────
# Dialoggrößen und Dialogtexte werden zentral gehalten, damit Dialoge ähnlich aussehen.
DIALOG_TITLE = f"font-size:20px; font-weight:700; color:{COLOR_TEXT_PRIMARY};"
DIALOG_TITLE_BOLD = "font-size:20px; font-weight:700;"
DIALOG_TITLE_MB4 = DIALOG_TITLE + " margin-bottom:4px;"
DIALOG_TITLE_MB6 = DIALOG_TITLE + " margin-bottom:6px;"
DIALOG_TITLE_MB12 = DIALOG_TITLE + " margin-bottom:12px;"
DIALOG_TITLE_MB16 = DIALOG_TITLE + " margin-bottom:16px;"
DIALOG_TITLE_MB18 = DIALOG_TITLE + " margin-bottom:18px;"
DIALOG_TITLE_MB20 = DIALOG_TITLE + " margin-bottom:20px;"
DIALOG_SUBTITLE = f"font-size:12px; color:{COLOR_TEXT_SECONDARY}; margin-bottom:14px;"
DIALOG_SUBTITLE_MB16 = f"font-size:12px; color:{COLOR_TEXT_SECONDARY}; margin-bottom:16px;"

DIALOG_CARD_SM = "min-width:380px; padding:30px; border-radius:18px;"
DIALOG_CARD_MD = "min-width:400px; padding:30px; border-radius:18px;"
DIALOG_CARD_LG = "width:600px; max-width:95vw; padding:28px; border-radius:18px;"
DIALOG_CARD_WIDE = (
    "width:760px; max-width:97vw; padding:30px; border-radius:18px; "
    "max-height:95vh; overflow-y:auto;"
)
DIALOG_CARD_EDIT = "min-width:440px; max-width:520px; padding:32px; border-radius:18px;"
DIALOG_CARD_TASK = "width:480px; max-width:95vw; padding:24px; border-radius:18px;"
DIALOG_CARD_LECTURE = "width:520px; max-width:95vw; padding:26px; border-radius:18px;"
DIALOG_CONFIRM = "min-width:320px; padding:26px; border-radius:18px;"
DIALOG_CONFIRM_TITLE = f"font-size:18px; font-weight:700; color:{COLOR_TEXT_PRIMARY};"
DIALOG_CONFIRM_MSG = f"font-size:14px; color:{COLOR_TEXT_SECONDARY}; margin-top:8px;"

# ── Text & Tabellen ───────────────────────────────────────────────────────────
# Kleine Text- und Tabellenstyles, die in vielen UI-Seiten wiederverwendet werden.
BODY_SM = f"font-size:13px; color:{COLOR_TEXT_SECONDARY};"
BODY_SM_SLATE = f"font-size:13px; color:{COLOR_TEXT_SLATE};"
BODY_MD = f"font-size:14px; color:{COLOR_TEXT_SLATE};"
LABEL_XS = f"font-size:11px; font-weight:600; color:{COLOR_TEXT_SECONDARY};"
LABEL_XS_MT4 = LABEL_XS + " margin-top:4px;"
LABEL_UPPER = (
    f"font-size:12px; font-weight:600; color:{COLOR_TEXT_SECONDARY}; "
    "text-transform:uppercase; letter-spacing:0.5px;"
)
LABEL_UPPER_MT16 = LABEL_UPPER + " margin-top:16px;"
ID_TEXT = f"color:{COLOR_TEXT_MUTED}; font-size:12px;"
META_TEXT = f"color:{COLOR_TEXT_MUTED}; font-size:11px;"
CELL_TEXT = BODY_SM
CELL_BOLD = "font-weight:500;"
CELL_BOLD_DARK = "font-weight:600;"
GRADE_VALUE = f"font-weight:700; font-size:15px; color:{COLOR_TEXT_PRIMARY};"
STAT_VALUE_LG = "font-size:36px; font-weight:700; margin-top:4px;"
TIMELINE_TITLE = f"font-size:14px; font-weight:600; color:{COLOR_TEXT_PRIMARY};"
TIMELINE_SUB = (
    f"font-size:12px; color:{COLOR_TEXT_SECONDARY}; white-space:nowrap; "
    "overflow:hidden; text-overflow:ellipsis;"
)
EMPTY_HINT = f"font-size:12px; color:{COLOR_TEXT_MUTED};"
ERROR_LIST_ITEM = f"color:{COLOR_RED_DARK}; font-size:13px; font-family:monospace;"
SUCCESS_TEXT = f"color:{COLOR_GREEN};"
OFFICIAL_SECTION_LABEL = (
    f"font-size:12px; font-weight:700; color:{COLOR_GREEN}; "
    "text-transform:uppercase; letter-spacing:0.5px;"
)
PERSONAL_SECTION_LABEL = (
    f"font-size:12px; font-weight:700; color:{COLOR_BLUE}; "
    "text-transform:uppercase; letter-spacing:0.5px;"
)
ICON_SM_SECONDARY = f"color:{COLOR_TEXT_SECONDARY}; font-size:15px;"
TEXT_TIME = "color:#374151; font-size:13px; font-weight:500;"
DEADLINE_LABEL = "color:#ef4444;"

# ── Layout-Hilfen ─────────────────────────────────────────────────────────────
# Flexbox- und Layout-Strings für Header, Breadcrumbs, Karten und Inputs.
FLEX_PAGE_HEADER = (
    "display:flex; flex-direction:row; align-items:flex-start; "
    "justify-content:space-between; width:100%; margin-bottom:24px; flex-wrap:wrap; gap:12px;"
)
FLEX_COLUMN_GAP4 = "display:flex; flex-direction:column; gap:4px;"
BREADCRUMB = (
    "display:flex; flex-direction:row; align-items:center; gap:4px; "
    f"color:{COLOR_TEXT_SECONDARY}; font-size:12px; font-weight:600;"
)
BREADCRUMB_SEP = "margin:0 2px;"
BREADCRUMB_ACTIVE = f"color:{COLOR_BLUE};"

STAT_CARD_FLEX = "flex:1; min-width:240px;"
STAT_CARD_FLEX_200 = "flex:1; min-width:220px;"
QUICK_ACTION_PRIMARY = "width:100%; height:48px; font-weight:700; border-radius:14px;"
QUICK_ACTION_OUTLINE = "width:100%; height:44px; margin-top:10px; border-radius:12px;"

INPUT_FULL = "width:100%;"
INPUT_FULL_MT10 = "width:100%; margin-top:10px;"
INPUT_FULL_MT16 = "width:100%; margin-top:16px;"
INPUT_SOFT = f"width:100%; background:{COLOR_SURFACE}; border-radius:{RADIUS_INPUT};"

TIP_CARD = (
    f"background:{COLOR_BG_BLUE}; border:1px solid {COLOR_BG_BLUE_BORDER}; "
    "border-radius:10px; padding:16px; margin-top:16px;"
)
TIP_LABEL = f"font-size:10px; font-weight:700; color:{COLOR_BLUE_TEXT};"
TIP_TEXT = f"font-size:13px; color:{COLOR_BLUE_TEXT_DARK}; margin-top:6px;"
INFO_CARD_BLUE = f"padding: 20px; background: {COLOR_BG_BLUE}; border: 1px solid {COLOR_BG_BLUE_BORDER};"
IMPORT_RESULT_BOX = (
    f"max-height:200px; overflow-y:auto; padding:10px; "
    f"background:{COLOR_BG_RED}; border-radius:8px;"
)


def grade_color(value: float | None, *, neutral: str = COLOR_TEXT_MUTED) -> str:
    """Grün ab Note 4.0, sonst rot (Schweizer Notensystem)."""
    # None bedeutet: keine Note vorhanden, deshalb neutrale Farbe.
    if value is None:
        return neutral
    return COLOR_GREEN if value >= 4.0 else COLOR_RED


def grade_style(value: float | None, *, prefix: str = "", neutral: str = COLOR_TEXT_MUTED) -> str:
    """CSS color:-Deklaration für Notenwerte."""
    return f"{prefix}color:{grade_color(value, neutral=neutral)};"


def stat_value_style(value: float | None) -> str:
    """Grosser Statistik-Wert (z. B. Notendurchschnitt auf dem Dashboard)."""
    return f"{STAT_VALUE_LG} color:{grade_color(value)};"


def grade_summary_bg(value: float | None) -> str:
    """Hintergrund für Noten-Durchschnittszeile (grün/rot)."""
    bg = "#f0fdf4" if value is not None and value >= 4.0 else "#fef2f2"
    return f"background:{bg}; border-radius:8px; padding:8px 12px;"


def primary_action_button_css(class_name: str) -> str:
    """CSS für blaue Hauptaktions-Buttons (admin / deadlines / dozent)."""
    # class_name erlaubt denselben Buttonstyle mit unterschiedlichen CSS-Klassen.
    return f"""
    <style>
    .{class_name} {{
        height: 44px !important;
        padding: 0 24px !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, {COLOR_BLUE}, {COLOR_BLUE_DARK}) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        box-shadow: 0 12px 26px rgba(37, 99, 235, 0.25) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }}
    .{class_name}:hover {{
        transform: translateY(-1px);
        box-shadow: 0 16px 32px rgba(29, 78, 216, 0.32) !important;
    }}
    .{class_name}.q-btn--disable {{
        opacity: 1 !important;
        background: {COLOR_BLUE} !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }}
    </style>
    """


def add_primary_action_button_css(class_name: str) -> None:
    # Fügt den CSS-Block direkt in den HTML-Head der aktuellen Seite ein.
    ui.add_head_html(primary_action_button_css(class_name))
