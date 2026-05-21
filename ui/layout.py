"""
layout.py – Globales Layout: Sidebar + Header.
"""
from __future__ import annotations
from nicegui import ui, app


SIDEBAR_ITEMS = {
    "student": [
        ("dashboard",      "Dashboard",        "/dashboard"),
        ("calendar_month", "Stundenplan",       "/timetable"),
        ("alarm",          "Deadlines",         "/deadlines"),
        ("grade",          "Noten",             "/grades"),
        ("menu_book",      "Module",            "/modules"),
        ("smart_toy",      "KI-Assistent",      "/ai"),
    ],
    "dozent": [
        ("dashboard",      "Dashboard",         "/dozent/dashboard"),
        ("calendar_month", "Stundenplan",        "/timetable"),
        ("alarm",          "Deadlines",          "/deadlines"),
        ("school",         "Meine Vorlesungen",  "/dozent/courses"),
        ("grade",          "Noten eintragen",    "/dozent/grades"),
        ("smart_toy",      "KI-Assistent",       "/ai"),
    ],
    "admin": [
        ("dashboard",      "Dashboard",          "/admin/dashboard"),
        ("group",          "Klassen",            "/admin/classes"),
        ("menu_book",      "Module",             "/admin/modules"),
        ("people",         "Benutzer",           "/admin/users"),
        ("upload_file",    "Importieren",        "/admin/import"),
        ("calendar_month", "Stundenplan",        "/timetable"),
        ("alarm",          "Deadlines",          "/deadlines"),
        ("smart_toy",      "KI-Assistent",       "/ai"),
    ],
}

ROLE_LABELS = {
    "student": "Student",
    "dozent": "Dozent",
    "admin": "Admin",
}

ROLE_BADGE_CSS = {
    "student": "background:#ecfdf5;color:#047857;border:1px solid #a7f3d0;",
    "dozent": "background:#ecfeff;color:#0e7490;border:1px solid #a5f3fc;",
    "admin": "background:#f5f3ff;color:#6d28d9;border:1px solid #ddd6fe;",
}

ROLE_SIDEBAR_BADGE_CSS = {
    "student": "background:#14532d;color:#bbf7d0;border:1px solid #166534;",
    "dozent": "background:#164e63;color:#a5f3fc;border:1px solid #155e75;",
    "admin": "background:#4c1d95;color:#e9d5ff;border:1px solid #6d28d9;",
}

ROLE_AVATAR_BG = {
    "student": "#2563eb",
    "dozent": "#0891b2",
    "admin": "#7c3aed",
}

# ─────────────────────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Basis-Font NUR für Text-Elemente – NICHT für Icon-Elemente */
body, p, span, div, h1, h2, h3, h4, h5, h6,
input, textarea, button, label, td, th, a, li,
.nicegui-label, .nicegui-row, .nicegui-column,
.q-field__native, .q-field__label, .q-btn__content,
.q-item__label, .q-item__section {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

/* KRITISCH: Icon-Font wiederherstellen – sonst zeigen q-icon Rohtexte */
.q-icon,
.material-icons,
.material-icons-round,
.material-icons-outlined,
.material-icons-sharp,
.material-symbols-outlined,
.material-symbols-rounded,
i[class*="material"] {
    font-family: 'Material Icons' !important;
    font-style: normal !important;
    font-weight: normal !important;
    font-size: inherit;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    display: inline-block !important;
    white-space: nowrap !important;
    word-wrap: normal !important;
    direction: ltr !important;
    -webkit-font-smoothing: antialiased !important;
}

body { background: #f8fafc; margin: 0; }

/* ── Sidebar ── */
.sidebar {
    background: #0f172a !important;
    border-right: none !important;
    width: 228px !important;
    top: 0 !important;
    height: 100vh !important;
}

.sidebar .q-drawer__content,
.q-drawer--left .q-drawer__content {
    background: #0f172a !important;
    padding-top: 0 !important;
}

.q-drawer--left {
    top: 0 !important;
    height: 100vh !important;
}

.srp-nav-item {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;
    flex-wrap: nowrap !important;
    padding: 10px 16px !important;
    margin: 2px 8px !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    text-decoration: none !important;
    color: #94a3b8 !important;
    gap: 0 !important;
    user-select: none;
}
.srp-nav-item:hover  { background: #1e293b !important; color: #e2e8f0 !important; }
.srp-nav-item.active { background: #1e40af !important; color: #fff !important; }

.srp-nav-item .q-icon {
    font-size: 18px !important;
    width: 20px !important;
    min-width: 20px !important;
    flex-shrink: 0 !important;
    margin-right: 12px !important;
    color: inherit !important;
}

.srp-nav-label {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: inherit !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    line-height: 1.4 !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Header ── */
.app-header {
    background: transparent !important;
    border-bottom: none !important;
    height: 64px !important;
    padding: 0 !important;
    box-shadow: none !important;
    transition: all 0.3s;
}

@media (min-width: 1024px) {
    .app-header {
        left: 228px !important;
        width: calc(100% - 228px) !important;
    }
}

@media (max-width: 1023px) {
    .app-header {
        left: 0 !important;
        width: 100% !important;
    }
}

/* ── Page ── */
.page-content {
    /* Nutzt auf grossen Monitoren die verfügbare Breite, statt bei 1200px stehen zu bleiben. */
    width: 100%;
    max-width: none;
    margin: 0;
    padding: clamp(24px, 3vw, 44px);
    box-sizing: border-box;
}

/* ── Cards ── */
.stat-card {
    background: #fff;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    padding: 20px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.stat-card-label {
    color: #64748b; font-size: 11px; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.5px;
    font-family: 'Inter', sans-serif;
}
.stat-card-title {
    color: #0f172a; font-size: 20px; font-weight: 700; margin-top: 4px;
    font-family: 'Inter', sans-serif;
}
.stat-card-sub {
    color: #94a3b8; font-size: 13px; margin-top: 2px;
    font-family: 'Inter', sans-serif;
}

/* ── Badges ── */
.badge {
    display: inline-flex; align-items: center; padding: 3px 10px;
    border-radius: 20px; font-size: 11px; font-weight: 600;
    font-family: 'Inter', sans-serif;
}
.badge-red    { background: #fef2f2; color: #dc2626; }
.badge-green  { background: #f0fdf4; color: #16a34a; }
.badge-blue   { background: #eff6ff; color: #2563eb; }
.badge-yellow { background: #fefce8; color: #ca8a04; }
.badge-gray   { background: #f1f5f9; color: #64748b; }

/* ── Tables ── */
.data-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-family: 'Inter', sans-serif;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    overflow: hidden;
}
.data-table th {
    text-align: left; padding: 12px 16px; font-size: 11px; font-weight: 700;
    color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;
    border-bottom: 1px solid #e2e8f0; background: #f8fafc;
}
.data-table td {
    padding: 12px 16px; font-size: 14px; color: #374151;
    border-bottom: 1px solid #f1f5f9;
    vertical-align: middle;
}
.data-table tr:hover td { background: #f8fafc; }
.data-table tbody tr:last-child td { border-bottom: 0; }
.data-table .q-btn {
    min-width: 30px !important;
    min-height: 30px !important;
}

/* ── Forms ── */
.section-title { font-size: 22px; font-weight: 700; color: #0f172a; font-family: 'Inter', sans-serif; }
.section-sub   { font-size: 14px; color: #64748b; margin-top: 4px; font-family: 'Inter', sans-serif; }

/* Klassen-Mehrfachauswahl im Modul-Dialog: feste Chip-Bereichshöhe, damit der Dialog
   beim Hinzufügen weiterer Chips nicht wächst. Überzählige Chips scrollen im Feld. */
.module-classes-multiselect {
    width: 100%;
    max-width: 100%;
    min-width: 0;
}
.module-classes-multiselect .q-field__native {
    min-height: 76px;
    max-height: 76px;
    overflow-y: auto;
    overflow-x: hidden;
    align-content: flex-start;
    flex-wrap: wrap;
}
.module-classes-multiselect .q-chip {
    max-width: 240px;
}
.module-classes-multiselect .q-chip__content {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.module-classes-dropdown {
    max-height: 220px !important;
    overflow-y: auto !important;
}
.module-classes-dropdown .q-item__label {
    font-size: 13px;
}
"""


def get_session_user() -> dict | None:
    # Nach dem Login liegt der eingeloggte User als Dict im NiceGUI User-Storage.
    return app.storage.user.get("user") or None


def _role_label(role: str) -> str:
    return ROLE_LABELS.get(role, role.capitalize())


def _render_role_badge(role: str, *, dark: bool = False) -> None:
    """Kleines Rollen-Badge für Header (hell) oder Sidebar (dunkel)."""
    styles = ROLE_SIDEBAR_BADGE_CSS if dark else ROLE_BADGE_CSS
    style = styles.get(role, styles["student"])
    ui.label(_role_label(role)).style(
        "display:inline-flex; align-items:center; font-size:11px; font-weight:700; "
        "padding:3px 10px; border-radius:999px; letter-spacing:0.04em; "
        "text-transform:uppercase; white-space:nowrap; font-family:'Inter',sans-serif; "
        f"{style}"
    )


def require_role(*roles: str):
    # Diese Funktion schützt Seiten vor Zugriff ohne Login oder mit falscher Rolle.
    user = get_session_user()
    if not user:
        ui.navigate.to("/login")
        return None
        
    if user.get("status") == "initial" and roles:
        # Initiale Accounts müssen zuerst ihr Passwort im Profil ändern.
        ui.navigate.to("/profile")
        ui.notify("Bitte ändere dein Passwort, bevor du fortfährst.", color="warning", position="top")
        return None

    if roles and user.get("role") not in roles:
        # Falls die Rolle nicht erlaubt ist, geht es zurück zum passenden Dashboard.
        ui.navigate.to("/dashboard")
        return None
    return user


def create_layout(current_path: str = "/"):
    # Gemeinsames Layout für alle geschützten Seiten: Sidebar + Header.
    user = get_session_user()
    if not user:
        return

    role  = user.get("role", "student")
    name  = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
    initial = name[0].upper() if name else "?"

    ui.add_head_html(f"<style>{CSS}</style>")


    # ── Sidebar ───────────────────────────────────────────────────────────
    # Nutze das Quasar Layout 'Lhh lpR fFf', damit die Sidebar (L) links die volle Höhe nimmt
    ui.query(".q-layout").props("view='Lhh lpR fFf'")
    
    drawer = ui.left_drawer(value=False, fixed=True, bordered=False).props(
        "show-if-above breakpoint=1024"
    ).classes("sidebar")
    ui.query(".q-drawer--left").style("top: 0 !important; height: 100vh !important;")
    with drawer:
        # Logo-Block (Standard)
        with ui.element("div").style(
            "padding:24px 20px 8px; display:flex; flex-direction:column; gap:2px;"
        ):
            ui.label("StudentRP").style(
                "color:#fff; font-size:20px; font-weight:700; line-height:1.2; font-family:'Inter',sans-serif;"
            )
            ui.label("ACADEMIC PORTAL").style(
                "color:#475569; font-size:10px; text-transform:uppercase; "
                "letter-spacing:1.5px; font-family:'Inter',sans-serif;"
            )

        ui.separator().style("background:#1e293b; margin:8px 0;")

        # Navigationspunkte
        if user.get("status") == "initial":
            # Vor der Passwortänderung soll keine normale Navigation sichtbar sein.
            items = []
        else:
            items = SIDEBAR_ITEMS.get(role, SIDEBAR_ITEMS["student"])
            
        for icon_name, label_text, path in items:
            # Der aktive Navigationspunkt bekommt eine eigene CSS-Klasse.
            is_active = current_path == path or (path != "/" and current_path.startswith(path))
            css_class = "srp-nav-item active" if is_active else "srp-nav-item"

            with ui.element("div").classes(css_class).on("click", lambda p=path: ui.navigate.to(p)):
                ui.icon(icon_name)
                ui.label(label_text).classes("srp-nav-label")

        # Profil & Logout – unten fixiert
        with ui.element("div").style(
            "position:absolute; bottom:20px; left:0; right:0; padding:0 8px;"
        ):
            ui.separator().style("background:#1e293b; margin-top:8px; margin-bottom:8px;")

            with ui.element("div").style(
                "padding:10px 12px 12px; margin:0 8px 8px; border-radius:10px; "
                "background:#1e293b; display:flex; flex-direction:column; gap:6px;"
            ):
                ui.label(name).style(
                    "color:#e2e8f0; font-size:13px; font-weight:600; "
                    "font-family:'Inter',sans-serif; white-space:nowrap; overflow:hidden; "
                    "text-overflow:ellipsis;"
                )
                _render_role_badge(role, dark=True)

            with ui.element("div").classes("srp-nav-item").on(
                "click", lambda: ui.navigate.to("/profile")
            ):
                ui.icon("manage_accounts")
                ui.label("Profil").classes("srp-nav-label")

            with ui.element("div").classes("srp-nav-item").style("color:#f87171 !important;").on(
                "click", _logout
            ):
                ui.icon("logout").style("color:#f87171 !important;")
                ui.label("Logout").classes("srp-nav-label").style("color:#f87171 !important;")

    # ── Header ────────────────────────────────────────────────────────────
    with ui.header().classes("app-header"):
        # Nutze justify-between, um Menü links und Profil rechts zu platzieren
        with ui.element("div").classes("w-full h-full flex items-center justify-between").style("padding: 0 32px;"):
            # Linke Seite: Mobile Menu Button (NUR sichtbar auf kleinen Screens)
            with ui.row().classes("items-center"):
                ui.button(on_click=lambda: drawer.toggle()).props("flat round icon=menu").classes("text-slate-600 lg:hidden")

            # Rechte Seite: Profil
            with ui.element("div").style(
                "display:flex; align-items:center; justify-content:flex-end; "
                "gap:20px; padding-right:4px;"
            ):


                # Name, Rolle und Avatar – Rolle ist auf den ersten Blick sichtbar.
                with ui.element("div").style(
                    "display:flex; flex-direction:row; align-items:center; "
                    "gap:10px; flex-wrap:nowrap;"
                ):
                    with ui.element("div").style(
                        "display:flex; flex-direction:column; align-items:flex-end; gap:4px;"
                    ):
                        ui.label(name).style(
                            "font-size:14px; font-weight:600; color:#0f172a; "
                            "white-space:nowrap; font-family:'Inter',sans-serif;"
                        )
                        _render_role_badge(role)
                    avatar_bg = ROLE_AVATAR_BG.get(role, ROLE_AVATAR_BG["student"])
                    with ui.element("div").style(
                        f"width:34px; height:34px; border-radius:50%; "
                        f"background:{avatar_bg}; display:flex; align-items:center; "
                        "justify-content:center; flex-shrink:0; cursor:pointer;"
                    ).on("click", lambda: ui.navigate.to("/profile")):
                        ui.label(initial).style(
                            "color:#fff; font-size:13px; font-weight:700; "
                            "line-height:1; font-family:'Inter',sans-serif;"
                        )


def _logout():
    # User-Storage leeren reicht, weil die Sessiondaten dort gespeichert sind.
    app.storage.user.clear()
    ui.navigate.to("/login")
