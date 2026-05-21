"""
auth_pages.py – Login, "Passwort vergessen" und Passwort-Reset Seiten.
"""
from __future__ import annotations
from nicegui import ui, app

from services.auth_service import AuthService
from services.mail_service import MailService
from services.user_service import UserService
from ui.session_helpers import run_auth, run_in_session
from ui.layout import CSS
from ui import styles as st


def _inject_auth_css():
    # Login/Reset-Seiten haben kein normales App-Layout, deshalb wird ihr CSS hier separat injiziert.
    # Icon-Font Fix ist gleich wie im globalen Layout, damit Material Icons korrekt dargestellt werden.
    ui.add_head_html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Icon-Font NICHT überschreiben */
    .q-icon, .material-icons, i[class*="material"] {
        font-family: 'Material Icons' !important;
        font-style: normal !important;
        line-height: 1 !important;
    }

    body, p, span, div, h1, h2, h3, label, input, button {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    body { margin: 0; }

    .auth-bg {
        position: fixed;
        inset: 0;
        width: 100vw;
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: clamp(16px, 4vw, 40px);
        box-sizing: border-box;
        overflow: auto;
        background:
            radial-gradient(circle at 18% 18%, rgba(37, 99, 235, 0.35), transparent 28%),
            radial-gradient(circle at 82% 22%, rgba(14, 165, 233, 0.22), transparent 30%),
            linear-gradient(135deg, #020617 0%, #0f172a 48%, #111827 100%);
    }
    .auth-bg::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.28;
        background-image:
            linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
        background-size: 44px 44px;
    }
    .auth-card {
        position: relative;
        z-index: 1;
        background: #fff;
        border-radius: 16px;
        padding: clamp(24px, 4vw, 40px);
        width: min(460px, calc(100vw - 32px));
        box-sizing: border-box;
        box-shadow: 0 25px 50px rgba(0,0,0,0.4);
    }
    .auth-logo  { font-size: 26px; font-weight: 800; color: #0f172a; font-family:'Inter',sans-serif; }
    .auth-sub   { font-size: 12px; color: #64748b; margin-top: 2px; text-transform:uppercase; letter-spacing:1px; }
    .auth-title { font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 24px; }
    .auth-desc  { font-size: 14px; color: #64748b; margin-top: 4px; }
    .auth-login-shell {
        position: relative;
        z-index: 1;
        width: min(980px, calc(100vw - 32px));
        display: grid;
        grid-template-columns: minmax(300px, 1fr) minmax(360px, 440px);
        overflow: hidden;
        border-radius: 28px;
        background: rgba(255,255,255,0.96);
        box-shadow: 0 30px 90px rgba(0,0,0,0.42);
        border: 1px solid rgba(255,255,255,0.35);
        backdrop-filter: blur(18px);
    }
    .auth-brand-panel {
        position: relative;
        padding: clamp(32px, 5vw, 56px);
        color: #ffffff;
        min-height: 520px;
        background:
            linear-gradient(145deg, rgba(37,99,235,0.92), rgba(15,23,42,0.98)),
            radial-gradient(circle at 20% 20%, rgba(255,255,255,0.26), transparent 30%);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .auth-brand-panel::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: -70px;
        bottom: -70px;
        border-radius: 999px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
    }
    .auth-brand-kicker {
        color: #bfdbfe;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
    }
    .auth-brand-title {
        color: #ffffff;
        font-size: clamp(34px, 4vw, 52px);
        line-height: 0.98;
        font-weight: 800;
        margin-top: 18px;
        letter-spacing: -1.4px;
    }
    .auth-brand-text {
        color: #dbeafe;
        font-size: 15px;
        line-height: 1.7;
        max-width: 420px;
        margin-top: 20px;
    }
    .auth-feature-list {
        display: grid;
        gap: 12px;
        margin-top: 30px;
    }
    .auth-feature-item {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #eff6ff;
        font-size: 13px;
        font-weight: 600;
    }
    .auth-feature-dot {
        width: 28px;
        height: 28px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.14);
        color: #ffffff;
        flex-shrink: 0;
    }
    .auth-form-panel {
        padding: clamp(30px, 4vw, 48px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #ffffff;
    }
    .auth-logo-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 28px;
    }
    .auth-logo-mark {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        box-shadow: 0 12px 28px rgba(37,99,235,0.28);
    }
    .auth-form-title {
        color: #0f172a;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.6px;
    }
    .auth-form-desc {
        color: #64748b;
        font-size: 14px;
        margin-top: 6px;
        line-height: 1.5;
    }
    .auth-field-label {
        color: #334155;
        font-size: 12px;
        font-weight: 700;
        margin-top: 18px;
        margin-bottom: 8px;
    }
    .auth-form-panel .q-field--outlined .q-field__control {
        min-height: 48px;
        border-radius: 14px;
        background: #f8fafc;
    }
    .auth-form-panel .q-field--focused .q-field__control {
        background: #ffffff;
        box-shadow: 0 0 0 4px rgba(37,99,235,0.10);
    }
    .auth-password-tools {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 5px;
        margin-top: 7px;
        color: #64748b;
        font-size: 12px;
        cursor: pointer;
        user-select: none;
    }
    .auth-error {
        color: #b91c1c;
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 12px;
        padding: 10px 12px;
        font-size: 13px;
        margin-top: 14px;
        display: none;
    }
    .auth-help-row {
        display: flex;
        justify-content: center;
        margin-top: 22px;
        padding-top: 18px;
        border-top: 1px solid #e2e8f0;
    }
    .auth-help-row a {
        color: #2563eb !important;
        font-size: 13px;
        font-weight: 600;
        text-decoration: none;
    }
    @media (max-width: 860px) {
        .auth-login-shell {
            grid-template-columns: 1fr;
            width: min(460px, calc(100vw - 32px));
        }
        .auth-brand-panel {
            min-height: auto;
            padding: 28px;
        }
        .auth-feature-list {
            display: none;
        }
        .auth-brand-title {
            font-size: 30px;
        }
    }

    /* Passwort-Wrapper: Input + Toggle-Button nebeneinander */
    .pw-wrapper {
        display: flex;
        flex-direction: row;
        align-items: center;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        overflow: hidden;
        margin-top: 12px;
        background: #fff;
        transition: border-color 0.15s;
    }
    .pw-wrapper:focus-within { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
    .pw-wrapper input {
        flex: 1;
        border: none;
        outline: none;
        padding: 11px 14px;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        background: transparent;
        color: #0f172a;
        min-width: 0;
    }
    .pw-toggle {
        background: none;
        border: none;
        cursor: pointer;
        padding: 0 12px;
        color: #94a3b8;
        font-size: 20px;
        display: flex;
        align-items: center;
        flex-shrink: 0;
        height: 100%;
        min-height: 44px;
    }
    .pw-toggle:hover { color: #2563eb; }
    .pw-toggle .material-icons {
        font-family: 'Material Icons' !important;
        font-size: 20px !important;
    }

    /* Standard-Input-Feld */
    .auth-input {
        width: 100%;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 11px 14px;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        color: #0f172a;
        outline: none;
        transition: border-color 0.15s;
        margin-top: 12px;
        box-sizing: border-box;
    }
    .auth-input:first-of-type { margin-top: 0; }
    .auth-input:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
    .auth-input::placeholder { color: #94a3b8; }

    /* Login-Button */
    .auth-btn {
        width: 100%;
        background: #2563eb;
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 13px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        margin-top: 16px;
        font-family: 'Inter', sans-serif;
        transition: background 0.15s;
    }
    .auth-btn:hover { background: #1d4ed8; }
    .main-action-btn {
        height: 48px !important;
        padding: 0 22px !important;
        border-radius: 14px !important;
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        box-shadow: 0 14px 30px rgba(37,99,235,0.28) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .main-action-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 18px 36px rgba(29,78,216,0.34) !important;
    }
    </style>
    """)


@ui.page("/login")
def login_page():
    # Login-Seite ist öffentlich, deshalb kein require_role().
    _inject_auth_css()
    ui.query("body").style("margin:0;")

    with ui.element("div").classes("auth-bg"):
        with ui.element("div").classes("auth-login-shell"):
            with ui.element("div").classes("auth-brand-panel"):
                with ui.element("div"):
                    ui.label("ACADEMIC PORTAL").classes("auth-brand-kicker")
                    ui.label("StudentRP").classes("auth-brand-title")
                    ui.label(
                        "Dein zentraler Zugang zu Stundenplan, Deadlines, Noten und KI-Assistenz."
                    ).classes("auth-brand-text")
                    with ui.element("div").classes("auth-feature-list"):
                        for icon_name, text in [
                            ("event", "Alle Termine und Fristen im Blick"),
                            ("grade", "Noten und Module sauber organisiert"),
                            ("smart_toy", "Studienassistent direkt integriert"),
                        ]:
                            with ui.element("div").classes("auth-feature-item"):
                                with ui.element("span").classes("auth-feature-dot"):
                                    ui.icon(icon_name).style("font-size:16px;")
                                ui.label(text)
                ui.label("Sicherer Login für Studenten, Dozenten und Admins.").style(
                    "color:#bfdbfe; font-size:13px; font-weight:600; position:relative; z-index:1;"
                )

            with ui.element("div").classes("auth-form-panel"):
                with ui.element("div").classes("auth-logo-row"):
                    with ui.element("div").classes("auth-logo-mark"):
                        ui.icon("school").style("font-size:24px;")
                    with ui.element("div"):
                        ui.label("StudentRP").classes("auth-logo")
                        ui.label("ACADEMIC PORTAL").classes("auth-sub")

                ui.label("Willkommen zurück").classes("auth-form-title")
                ui.label("Melde dich mit deiner E-Mail oder Student-ID an.").classes("auth-form-desc")

                # E-Mail / Student-ID: AuthService entscheidet später, ob identifier Zahl oder E-Mail ist.
                ui.label("E-Mail oder Student-ID").classes("auth-field-label")
                identifier = ui.input(
                    placeholder="student@uni.ch oder 10042",
                ).props("outlined dense hide-bottom-space").style(st.INPUT_FULL)
                with identifier.add_slot("prepend"):
                    ui.icon("alternate_email").style("color:#64748b;")

                # Passwort mit eigener Anzeigen/Verbergen-Logik.
                # So bleibt das Design unabhängig vom Standard-Quasar-Passwortslot.
                ui.label("Passwort").classes("auth-field-label")
                pw_state = {"show": False}
                pw_input = ui.input(
                    password=True,
                    placeholder="Dein Passwort",
                ).props("outlined dense hide-bottom-space").style(st.INPUT_FULL)
                with pw_input.add_slot("prepend"):
                    ui.icon("lock").style("color:#64748b;")

                def toggle_pw():
                    # State umschalten und das Input-Feld zwischen Text und Passwort wechseln.
                    pw_state["show"] = not pw_state["show"]
                    if pw_state["show"]:
                        pw_input.props("type=text")
                        toggle_icon.name = "visibility_off"
                        toggle_label.set_text("Passwort verbergen")
                    else:
                        pw_input.props("type=password")
                        toggle_icon.name = "visibility"
                        toggle_label.set_text("Passwort anzeigen")

                # Toggle liegt bewusst unter dem Feld, damit der Input selbst ruhig und breit bleibt.
                with ui.element("div").classes("auth-password-tools").on("click", toggle_pw):
                    toggle_icon = ui.icon("visibility").style("font-size:18px;")
                    toggle_label = ui.label("Passwort anzeigen")

                error_label = ui.label("").classes("auth-error")

                def do_login():
                    # Vor dem Service-Aufruf einfache Pflichtfeldprüfung in der UI.
                    if not identifier.value or not pw_input.value:
                        error_label.set_text("Bitte alle Felder ausfüllen.")
                        error_label.style("display:block;")
                        return
                    try:
                        # AuthService liefert bei Erfolg ein kleines Session-Dict zurück.
                        session_data = run_auth(
                            lambda auth: auth.login(identifier.value, pw_input.value)
                        )
                        if not session_data:
                            error_label.set_text("Ungültige Zugangsdaten oder Konto deaktiviert.")
                            error_label.style("display:block;")
                            return
                        # NiceGUI speichert die Sessiondaten pro Browser/User.
                        app.storage.user["user"] = session_data
                        if session_data.get("status") == "initial":
                            # Neue Benutzer müssen zuerst ihr Startpasswort ändern.
                            ui.navigate.to("/profile")
                            ui.notify("Bitte ändere dein Passwort beim ersten Login.", color="warning", position="top")
                        else:
                            ui.navigate.to("/dashboard")
                    except Exception as e:
                        error_label.set_text(f"Fehler: {e}")
                        error_label.style("display:block;")

                pw_input.on("keydown.enter", do_login)
                identifier.on("keydown.enter", do_login)

                ui.button("ANMELDEN", on_click=do_login).props("unelevated").classes("main-action-btn").style(
                    "width:100%; margin-top:20px;"
                )

                with ui.element("div").classes("auth-help-row"):
                    ui.link("Passwort vergessen?", "/forgot-password")





@ui.page("/forgot-password")
def forgot_password_page():
    # Öffentliche Seite zum Anfordern eines Passwort-Reset-Links.
    _inject_auth_css()
    ui.query("body").style("margin:0;")

    with ui.element("div").classes("auth-bg"):
        with ui.element("div").classes("auth-card"):
            ui.label("StudentRP").classes("auth-logo")
            ui.label("ACADEMIC PORTAL").classes("auth-sub")

            ui.label("Passwort zurücksetzen").classes("auth-title")
            ui.label(
                "Gib deine E-Mail ein. Wir senden dir einen Reset-Link."
            ).classes("auth-desc")
            ui.separator().style("margin: 20px 0;")

            email_input = ui.input("E-Mail", placeholder="student@uni.ch").props(
                "outlined dense"
            ).style(st.INPUT_FULL)

            msg_label = ui.label("").style("font-size:13px; margin-top:8px;")

            def do_reset_request():
                email = email_input.value.strip()
                if not email:
                    msg_label.set_text("Bitte E-Mail eingeben.")
                    msg_label.style("color:#dc2626;")
                    return
                def request_reset(auth):
                    token = auth.request_password_reset(email)
                    if token:
                        user = auth._dao.get_by_email(email)
                        MailService().send_password_reset_email(
                            to_email=email,
                            full_name=f"{user.first_name} {user.last_name}" if user else email,
                            reset_token=token,
                            base_url="http://localhost:8080",
                        )

                run_auth(request_reset)
                # Generische Meldung (Sicherheit)
                msg_label.set_text(
                    "✅ Falls diese E-Mail registriert ist, erhältst du in Kürze einen Reset-Link."
                )
                msg_label.style("color:#16a34a;")

            ui.button("RESET-LINK SENDEN", on_click=do_reset_request).props(
                "unelevated"
            ).classes("main-action-btn").style(st.INPUT_FULL_MT16)

            with ui.row().classes("justify-center mt-4"):
                ui.link("← Zurück zum Login", "/login").style("font-size:13px; color:#2563eb;")


@ui.page("/reset-password")
def reset_password_page(token: str = ""):
    _inject_auth_css()
    ui.query("body").style("margin:0;")

    with ui.element("div").classes("auth-bg"):
        with ui.element("div").classes("auth-card"):
            ui.label("StudentRP").classes("auth-logo")
            ui.label("Neues Passwort festlegen").classes("auth-title")
            ui.separator().style("margin: 20px 0;")

            pw1 = ui.input("Neues Passwort", password=True, password_toggle_button=True).props(
                "outlined dense"
            ).style("width:100%; margin-top:12px;")
            pw2 = ui.input("Passwort wiederholen", password=True).props(
                "outlined dense"
            ).style("width:100%; margin-top:12px;")

            msg = ui.label("").style("font-size:13px; margin-top:8px;")

            def do_reset():
                if not token:
                    msg.set_text("Kein Reset-Token gefunden. Bitte den Link aus der E-Mail verwenden.")
                    msg.style("color:#dc2626;")
                    return
                if pw1.value != pw2.value:
                    msg.set_text("Passwörter stimmen nicht überein.")
                    msg.style("color:#dc2626;")
                    return
                if len(pw1.value) < 8:
                    msg.set_text("Passwort muss mindestens 8 Zeichen haben.")
                    msg.style("color:#dc2626;")
                    return
                ok = run_auth(lambda auth: auth.reset_password(token.strip(), pw1.value))
                if ok:
                    msg.set_text("✅ Passwort erfolgreich zurückgesetzt!")
                    msg.style("color:#16a34a;")
                    ui.timer(2.0, lambda: ui.navigate.to("/login"), once=True)
                else:
                    msg.set_text("❌ Ungültiger oder abgelaufener Token.")
                    msg.style("color:#dc2626;")

            ui.button("PASSWORT SETZEN", on_click=do_reset).props(
                "unelevated"
            ).classes("main-action-btn").style(st.INPUT_FULL_MT16)

            with ui.row().classes("justify-center mt-4"):
                ui.link("← Zurück zum Login", "/login").style("font-size:13px; color:#2563eb;")


@ui.page("/profile")
def profile_page():
    from ui.layout import create_layout, get_session_user, require_role
    user = require_role()
    if not user:
        return
    create_layout("/profile")

    with ui.column().classes("page-content gap-6"):
        full_name = f"{user['first_name']} {user['last_name']}".strip()
        initial = full_name[0].upper() if full_name else "?"
        role_label = user["role"].capitalize()

        ui.label("Mein Profil").classes("section-title")
        ui.label("Persönliche Kontoübersicht und Passwortverwaltung").classes("section-sub")

        with ui.row().classes("w-full gap-6 flex-wrap").style("align-items:flex-start;"):
            with ui.card().classes("stat-card").style("flex:1; min-width:320px; max-width:520px;"):
                with ui.row().classes("items-center gap-4").style("margin-bottom:18px;"):
                    with ui.element("div").style(
                        "width:64px; height:64px; border-radius:999px; background:#2563eb; "
                        "display:flex; align-items:center; justify-content:center; flex-shrink:0; "
                        "box-shadow:0 10px 24px rgba(37,99,235,0.22);"
                    ):
                        ui.label(initial).style(
                            "color:#fff; font-size:24px; font-weight:800; line-height:1;"
                        )
                    with ui.column().classes("gap-1"):
                        ui.label(full_name).style(
                            "font-size:20px; font-weight:800; color:#0f172a;"
                        )
                        ui.label(role_label).style(
                            "width:fit-content; background:#eff6ff; color:#1d4ed8; "
                            "font-size:12px; font-weight:700; padding:4px 10px; border-radius:999px;"
                        )

                def profile_row(label: str, value: str, icon: str):
                    with ui.element("div").style(
                        "display:grid; grid-template-columns:28px 110px 1fr; align-items:center; "
                        "gap:10px; padding:12px 0; border-top:1px solid #f1f5f9;"
                    ):
                        ui.icon(icon).style("font-size:18px; color:#64748b;")
                        ui.label(label).style("font-size:12px; color:#64748b; font-weight:700;")
                        ui.label(value).style("font-size:14px; color:#0f172a; font-weight:500;")

                profile_row("E-Mail", user["email"], "mail")
                profile_row("Benutzer-ID", str(user["user_id"]), "badge")

            with ui.card().classes("stat-card").style("flex:1; min-width:320px; max-width:520px;"):
                ui.label("Passwort ändern").style(
                    "font-size:18px; font-weight:800; color:#0f172a;"
                )
                ui.label(
                    "Wähle ein sicheres Passwort mit mindestens 8 Zeichen."
                ).style("font-size:13px; color:#64748b; margin-top:4px; margin-bottom:16px;")

                pw1 = ui.input("Neues Passwort", password=True, password_toggle_button=True).props("outlined dense").style(st.INPUT_FULL)
                pw2 = ui.input("Passwort wiederholen", password=True, password_toggle_button=True).props("outlined dense").style(st.INPUT_FULL_MT10)
                msg = ui.label("").style("font-size:13px; margin-top:8px; min-height:18px;")

                def change_pw():
                    was_initial = app.storage.user.get("user", {}).get("status") == "initial"
                    if pw1.value != pw2.value:
                        msg.set_text("Passwörter stimmen nicht überein.")
                        msg.style("color:#dc2626;")
                        return
                    if len(pw1.value) < 8:
                        msg.set_text("Mindestens 8 Zeichen.")
                        msg.style("color:#dc2626;")
                        return
                    def change_password(session):
                        AuthService(session).change_password(user["user_id"], pw1.value)
                        usr_svc = UserService(session)
                        usr = usr_svc._dao.get_by_id(user["user_id"])
                        if usr and usr.status == "initial":
                            usr.status = "active"
                            usr_svc._dao.update(usr)
                            app.storage.user["user"]["status"] = "active"

                    run_in_session(change_password)
                            
                    msg.set_text("Passwort geändert.")
                    msg.style("color:#16a34a;")
                    if was_initial:
                        ui.timer(1.0, lambda: ui.navigate.to("/dashboard"), once=True)

                ui.button("Passwort ändern", on_click=change_pw).props(
                    "color=primary unelevated"
                ).style("width:100%; height:42px; margin-top:14px; font-weight:700;")
