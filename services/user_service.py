"""
user_service.py – Benutzer anlegen (manuell + CSV-Import).
Ruft MailService für Willkommens-E-Mails auf.
"""
from __future__ import annotations
import csv
import secrets
import string
from io import StringIO
from typing import Optional

from pydantic import ValidationError
from sqlmodel import Session

from data_access.user_dao import UserDAO
from domain.models import User, ClassGroup, DozentClass
from domain.schemas import UserCreateSchema
from domain.enums import RoleType
from data_access.academic_dao import AcademicDAO
from services.auth_service import hash_password
from services.mail_service import MailService


def _generate_password(length: int = 12) -> str:
    # Zufälliges Startpasswort für neu angelegte User.
    alphabet = string.ascii_letters + string.digits + "!@#$"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _validate_import_role(role_raw: str, label: str) -> tuple[Optional[RoleType], Optional[str]]:
    """Rolle prüfen; bei Fehler (None, Fehlermeldung)."""
    # Importdateien können Groß-/Kleinschreibung enthalten, deshalb normalisieren.
    role_val = (role_raw or "").strip().lower()
    if not role_val:
        return None, f"{label}: Rolle fehlt."
    try:
        return RoleType(role_val), None
    except ValueError:
        return None, (
            f"{label}: Ungültige Rolle '{role_val}'. Erlaubt: student, dozent, admin"
        )


def _validate_import_email(email: str, label: str) -> Optional[str]:
    """E-Mail prüfen; bei Fehler Fehlermeldung, sonst None."""
    email = email.strip()
    if not email or email.count("@") != 1 or "." not in email.split("@")[-1]:
        return f"{label}: Ungültige E-Mail Adresse."
    return None


def _validate_import_name(name: str, field_label: str, label: str) -> Optional[str]:
    """Vor-/Nachname prüfen; bei Fehler Fehlermeldung, sonst None."""
    name = name.strip()
    if name and not all(c.isalpha() or c in " -" for c in name):
        return (
            f"{label}: {field_label} darf nur Buchstaben, Leerzeichen "
            "und Bindestriche enthalten."
        )
    return None


def _prepare_import_class_assignment(
    role: RoleType,
    resolved_cg_ids: list[int],
    label: str,
) -> tuple[list[int], Optional[int], Optional[str]]:
    """
    Klassenzuordnung für Import vorbereiten.
    Gibt (bereinigte Klassen-IDs, primary_class_id für Student, Fehlermeldung) zurück.
    """
    # Admins gehören keiner Klasse an.
    if role == RoleType.admin:
        return [], None, None
    # Studenten müssen genau eine Klasse haben.
    if role == RoleType.student:
        if len(resolved_cg_ids) != 1:
            return resolved_cg_ids, None, (
                f"{label}: Student muss genau einer Klasse zugeordnet sein."
            )
        return resolved_cg_ids, resolved_cg_ids[0], None
    return resolved_cg_ids, None, None


def _build_user_create_schema(
    email: str,
    first_name: str,
    last_name: str,
    role: RoleType,
    class_group_id: Optional[int],
) -> UserCreateSchema:
    """UserCreateSchema aus validierten Import-Feldern erzeugen."""
    return UserCreateSchema(
        email=email.strip(),
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        role=role,
        class_group_id=class_group_id,
    )


class UserService:
    def __init__(self, session: Session):
        self._dao = UserDAO(session)
        self._mail = MailService()

    def get_all_users(self) -> list[User]:
        return self._dao.get_all()

    def get_users_by_role(self, role_name: str) -> list[User]:
        return self._dao.get_by_role(role_name)

    def class_labels_for_users(self, users: list[User]) -> dict[int, str]:
        """Anzeige-Text für die Klassenspalte in der Benutzerverwaltung."""
        acad = AcademicDAO(self._dao.session)
        labels: dict[int, str] = {}
        for u in users:
            # Dozenten können mehreren Klassen zugeordnet sein, Studenten normalerweise nur einer.
            if u.role and u.role.name == "dozent":
                assigns = acad.get_class_assignments_by_dozent(u.user_id)
                names = [a.class_group.name for a in assigns if a.class_group]
                labels[u.user_id] = (
                    ", ".join(names) if names
                    else (u.class_group.name if u.class_group else "–")
                )
            else:
                labels[u.user_id] = u.class_group.name if u.class_group else "–"
        return labels

    def _resolve_class_groups(self, item: dict) -> list[int]:
        """Sucht ClassGroup-IDs anhand ID oder Name (kommagetrennt). Erstellt Klasse wenn Name neu."""
        # Der Import akzeptiert verschiedene Spaltennamen, damit CSV-Dateien flexibler sind.
        cg_id_raw = item.get("class_group_id") or item.get("class_id")
        cg_name = item.get("class_name") or item.get("klasse") or item.get("Klasse")

        acad_dao = AcademicDAO(self._dao.session)
        ids = []

        if cg_id_raw:
            try:
                # Mehrere Klassen können kommagetrennt angegeben werden.
                for part in str(cg_id_raw).split(","):
                    cid = int(part.strip())
                    if acad_dao.get_class_group_by_id(cid):
                        ids.append(cid)
            except (ValueError, TypeError):
                pass

        if not ids and cg_name:
            for part in str(cg_name).split(","):
                name = part.strip()
                if name and name.lower() not in ("none", "null", "", "-"):
                    # Neue Klassennamen aus Importdateien werden automatisch angelegt.
                    cg = acad_dao.get_class_group_by_name(name)
                    if not cg:
                        cg = acad_dao.create_class_group(ClassGroup(
                            name=name,
                            description="Automatisch erstellt beim Benutzerimport.",
                        ))
                    ids.append(cg.class_group_id)

        return list(set(ids))

    def _assign_dozent_to_classes(self, dozent_id: int, class_group_ids: list[int]) -> None:
        # Dozenten können über DozentClass mehreren Klassen zugewiesen werden.
        dao = AcademicDAO(self._dao.session)
        for cg_id in class_group_ids:
            dao.assign_dozent_to_class(DozentClass(dozent_id=dozent_id, class_group_id=cg_id))

    def _import_record(
        self,
        item: dict,
        label: str,
        base_url: str,
    ) -> tuple[Optional[User], Optional[str]]:
        """Ein Import-Datensatz aus einer CSV-Zeile verarbeiten."""
        # Erst Klassen auflösen, dann Rolle/Name/E-Mail validieren.
        resolved_cg_ids = self._resolve_class_groups(item)

        role, err = _validate_import_role(item.get("role", ""), label)
        if err:
            return None, err

        email = item.get("email", "")
        first_name = item.get("first_name", "")
        last_name = item.get("last_name", "")

        if err := _validate_import_email(email, label):
            return None, err
        if err := _validate_import_name(first_name, "Vorname", label):
            return None, err
        if err := _validate_import_name(last_name, "Nachname", label):
            return None, err

        resolved_cg_ids, primary_class_id, err = _prepare_import_class_assignment(
            role, resolved_cg_ids, label
        )
        if err:
            return None, err

        schema = _build_user_create_schema(
            email, first_name, last_name, role, primary_class_id
        )
        user, err_msg = self.create_user(schema, base_url)
        if not user:
            return None, err_msg

        if role == RoleType.dozent and resolved_cg_ids:
            # Bei Dozenten werden alle importierten Klassen als DozentClass gespeichert.
            self._assign_dozent_to_classes(user.user_id, resolved_cg_ids)
        return user, None

    def create_user(
        self,
        schema: UserCreateSchema,
        base_url: str = "http://localhost:8080",
        send_mail: bool = True,
    ) -> tuple[Optional[User], str]:
        """
        Legt einen neuen Benutzer an.
        Gibt (User, plain_password) zurück oder (None, error_message).
        """
        if self._dao.email_exists(schema.email):
            return None, f"E-Mail {schema.email!r} ist bereits vergeben."

        role = self._dao.get_role_by_name(schema.role.value)
        if not role:
            return None, f"Rolle {schema.role.value!r} nicht gefunden."

        # Neue User starten mit Zufallspasswort und Status "initial".
        plain_pw = _generate_password()
        user = User(
            role_id=role.role_id,
            class_group_id=schema.class_group_id,
            first_name=schema.first_name,
            last_name=schema.last_name,
            email=schema.email,
            password_hash=hash_password(plain_pw),
            status="initial",
        )
        created = self._dao.create(user)

        if send_mail:
            try:
                # Im Mock-Modus wird diese Mail nur in mail.log geschrieben.
                self._mail.send_welcome_email(
                    to_email=created.email,
                    full_name=f"{created.first_name} {created.last_name}",
                    plain_password=plain_pw,
                    user_id=created.user_id,
                )
            except Exception as e:
                print(f"Mail-Fehler (User {created.email}): {e}")
        return created, plain_pw

    def import_from_csv(self, csv_content: str, base_url: str = "http://localhost:8080") -> dict:
        """
        Importiert Benutzer aus CSV-Inhalt.
        Erwartet: email, first_name, last_name, role, [class_group_id]
        """
        created_users: list[User] = []
        errors: list[str] = []

        reader = csv.DictReader(StringIO(csv_content))
        for i, row in enumerate(reader, start=2):
            try:
                # start=2, weil Zeile 1 die CSV-Kopfzeile ist.
                user, err = self._import_record(row, f"Zeile {i}", base_url)
                if user:
                    created_users.append(user)
                elif err:
                    errors.append(err)
            except (ValidationError, ValueError, KeyError) as e:
                errors.append(f"Zeile {i}: {e}")

        return {"created": created_users, "errors": errors}

    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        user = self._dao.get_by_id(user_id)
        if not user:
            return None
        for key, val in kwargs.items():
            if val is not None and hasattr(user, key):
                setattr(user, key, val)
        return self._dao.update(user)

    def deactivate_user(self, user_id: int) -> bool:
        user = self._dao.get_by_id(user_id)
        if not user:
            return False
        user.status = "inactive"
        self._dao.update(user)
        return True

    def delete_user(self, user_id: int) -> bool:
        user = self._dao.get_by_id(user_id)
        if not user:
            return False

        # Abhängige Daten zuerst löschen, damit keine Foreign-Key-Konflikte entstehen.
        for g in list(user.grades):
            self._dao.session.delete(g)
        for t in list(user.tasks):
            self._dao.session.delete(t)
        for d in list(user.dozent_assignments):
            self._dao.session.delete(d)
        self._dao.session.commit()

        self._dao.delete(user)
        return True
