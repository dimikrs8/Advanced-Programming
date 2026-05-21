"""
user_dao.py – Data Access Object für User & Role.
Alle User-Queries nutzen joinedload() für role und class_group,
um DetachedInstanceError ausserhalb der Session zu vermeiden.
"""
from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from domain.models import Role, User


class UserDAO:
    def __init__(self, session: Session):
        # DAO bekommt die Session von außen, damit Service-Methoden mehrere DAO-Aufrufe bündeln können.
        self.session = session

    # ── Role ──────────────────────────────────────────────────────────────

    def get_role_by_name(self, name: str) -> Optional[Role]:
        return self.session.exec(
            select(Role).where(Role.name == name)
        ).first()

    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        return self.session.get(Role, role_id)

    def get_all_roles(self) -> list[Role]:
        return list(self.session.exec(select(Role)).all())

    # ── User ──────────────────────────────────────────────────────────────

    def _user_stmt(self):
        """Basis-Select mit Eager Loading für role und class_group."""
        # joinedload lädt Rolle und Klasse direkt mit, bevor die Session geschlossen wird.
        return select(User).options(
            joinedload(User.role),         # type: ignore[arg-type]
            joinedload(User.class_group),  # type: ignore[arg-type]
        )

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.exec(
            self._user_stmt().where(User.user_id == user_id)
        ).first()

    def get_by_email(self, email: str) -> Optional[User]:
        # E-Mails werden normalisiert, damit Groß-/Kleinschreibung keine Rolle spielt.
        return self.session.exec(
            self._user_stmt().where(User.email == email.lower().strip())
        ).first()

    def get_by_reset_token(self, token: str) -> Optional[User]:
        return self.session.exec(
            self._user_stmt().where(User.reset_token == token)
        ).first()

    def get_all(self) -> list[User]:
        return list(self.session.exec(self._user_stmt()).unique().all())

    def get_by_class_group(self, class_group_id: int) -> list[User]:
        return list(self.session.exec(
            self._user_stmt().where(User.class_group_id == class_group_id)
        ).unique().all())

    def get_by_role(self, role_name: str) -> list[User]:
        # Erst wird die Rolle gesucht, danach alle User mit dieser role_id.
        role = self.get_role_by_name(role_name)
        if not role:
            return []
        return list(self.session.exec(
            self._user_stmt().where(User.role_id == role.role_id)
        ).unique().all())

    def create(self, user: User) -> User:
        # Nach commit + refresh enthält das Objekt auch die automatisch vergebene user_id.
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        # SQLModel erkennt geänderte Felder am bestehenden ORM-Objekt.
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()

    def email_exists(self, email: str) -> bool:
        # Kleine Hilfsmethode für die Validierung beim Anlegen neuer User.
        return self.get_by_email(email) is not None
