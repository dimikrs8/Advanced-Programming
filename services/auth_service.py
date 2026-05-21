"""
auth_service.py – Login-Logik, Passwort-Hashing, Reset-Tokens.
Verwendet bcrypt direkt (passlib inkompatibel mit Python 3.14 + bcrypt 5.x).
"""
from __future__ import annotations
import secrets
from datetime import timedelta
from typing import Optional

import bcrypt
from sqlmodel import Session

from data_access.user_dao import UserDAO
from domain.datetime_utils import utc_now
from domain.models import User

RESET_TOKEN_TTL_HOURS = 24


def hash_password(plain: str) -> str:
    # Passwörter werden nie im Klartext gespeichert, sondern nur als bcrypt-Hash.
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        # bcrypt vergleicht das eingegebene Passwort mit dem gespeicherten Hash.
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


class AuthService:
    def __init__(self, session: Session):
        self._dao = UserDAO(session)

    def login(self, identifier: str, password: str) -> Optional[dict]:
        """
        Identifier kann E-Mail oder Student-ID (int als String) sein.
        Gibt ein dict mit User-Daten zurück oder None bei Fehler.
        Alle Daten werden innerhalb der Session ausgelesen.
        """
        user: Optional[User] = None

        # Login ist bewusst flexibel: Entweder mit numerischer User-ID oder mit E-Mail.
        if identifier.strip().isdigit():
            user = self._dao.get_by_id(int(identifier.strip()))
        else:
            user = self._dao.get_by_email(identifier)

        # Inaktive User dürfen sich nicht anmelden; initiale User müssen später ihr Passwort ändern.
        if not user:
            return None
        if user.status not in ["active", "initial"]:
            return None
        if not verify_password(password, user.password_hash):
            return None

        # Rolle direkt laden, damit die UI nach dem Schließen der DB-Session noch Daten hat.
        role = self._dao.get_role_by_id(user.role_id)
        role_name = role.name if role else "student"

        return {
            "user_id": user.user_id,
            "role": role_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "class_group_id": user.class_group_id,
            "status": user.status,
        }

    def request_password_reset(self, email: str) -> Optional[str]:
        """
        Erstellt einen Reset-Token und speichert ihn in der DB.
        Gibt den Token zurück (für Mail-Versand). None = User nicht gefunden.
        """
        user = self._dao.get_by_email(email)
        if not user:
            return None

        # Der Token ist zufällig und nur zeitlich begrenzt gültig.
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expires = utc_now() + timedelta(hours=RESET_TOKEN_TTL_HOURS)
        self._dao.update(user)
        return token

    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Setzt das Passwort zurück. Gibt True bei Erfolg zurück.
        """
        user = self._dao.get_by_reset_token(token)
        if not user:
            return False
        if not user.reset_token_expires:
            return False
        if utc_now() > user.reset_token_expires:
            return False

        # Nach erfolgreichem Reset wird der Token gelöscht, damit er nicht erneut benutzt werden kann.
        user.password_hash = hash_password(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        
        # Initiale Accounts werden durch das erste gesetzte Passwort aktiviert.
        if user.status == "initial":
            user.status = "active"
            
        self._dao.update(user)
        return True

    def change_password(self, user_id: int, new_password: str) -> bool:
        user = self._dao.get_by_id(user_id)
        if not user:
            return False
        user.password_hash = hash_password(new_password)
        self._dao.update(user)
        return True
