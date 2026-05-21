"""
session_helpers.py – Kurzformen für DB-Sessions in der UI-Schicht.

Vermeidet wiederholtes ``with get_session() as session: svc = XxxService(session)``.
Geschäftslogik bleibt in services/; hier nur technische Vereinfachung.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, TypeVar

from sqlmodel import Session

from data_access.db import get_session

if TYPE_CHECKING:
    from services.academic_service import AcademicService
    from services.ai_service import AIService
    from services.auth_service import AuthService
    from services.grade_service import GradeService
    from services.user_service import UserService

T = TypeVar("T")


def run_in_session(fn: Callable[[Session], T]) -> T:
    """Führt *fn* mit einer geöffneten DB-Session aus."""
    # fn ist eine kleine Callback-Funktion aus der UI, die mit der Session arbeiten darf.
    with get_session() as session:
        return fn(session)


def run_academic(fn: Callable[["AcademicService"], T]) -> T:
    # Import hier drin verhindert unnötige Import-Zyklen beim Start der App.
    from services.academic_service import AcademicService

    with get_session() as session:
        # Die UI bekommt nur den Service, nicht direkt die Datenbank-Session.
        return fn(AcademicService(session))


def run_grade(fn: Callable[["GradeService"], T]) -> T:
    # Kurzform für alle Noten-Operationen aus der UI.
    from services.grade_service import GradeService

    with get_session() as session:
        return fn(GradeService(session))


def run_auth(fn: Callable[["AuthService"], T]) -> T:
    # Kurzform für Login, Passwortwechsel und Reset.
    from services.auth_service import AuthService

    with get_session() as session:
        return fn(AuthService(session))


def run_user(fn: Callable[["UserService"], T]) -> T:
    # Kurzform für Benutzerverwaltung und Import.
    from services.user_service import UserService

    with get_session() as session:
        return fn(UserService(session))


def run_ai(fn: Callable[["AIService"], T]) -> T:
    # Kurzform für den KI-Assistenten, damit auch dieser DB-Kontext bekommt.
    from services.ai_service import AIService

    with get_session() as session:
        return fn(AIService(session))
