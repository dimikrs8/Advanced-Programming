"""
schemas.py – Pydantic-Schemata für Eingabevalidierung (DTOs).
Gültige Noten: 1.0 – 6.0 (Schweizer Notensystem).
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from domain.enums import GradeSource, RoleType, TaskType


# ─────────────────────────────────────────────
# Auth Schemas
# ─────────────────────────────────────────────
class LoginSchema(BaseModel):
    # Schema für das Login-Formular: identifier kann E-Mail oder User-ID sein.
    identifier: str          # E-Mail oder Student-ID (string, wird konvertiert)
    password: str

    @field_validator("identifier")
    @classmethod
    def identifier_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Identifier darf nicht leer sein.")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("Passwort darf nicht leer sein.")
        return v


class PasswordResetRequestSchema(BaseModel):
    # Wird verwendet, wenn ein User einen Reset-Link per E-Mail anfordert.
    email: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Ungültige E-Mail-Adresse.")
        return v


class PasswordResetSchema(BaseModel):
    # Token kommt aus dem Reset-Link, new_password ist das neue Passwort.
    token: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Passwort muss mindestens 8 Zeichen lang sein.")
        return v


# ─────────────────────────────────────────────
# User Schemas
# ─────────────────────────────────────────────
class UserCreateSchema(BaseModel):
    # Dieses Schema prüft Daten, bevor ein neuer User in der DB angelegt wird.
    email: str
    first_name: str
    last_name: str
    role: RoleType
    class_group_id: Optional[int] = None
    class_name: Optional[str] = None

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Ungültige E-Mail-Adresse.")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Dieses Feld darf nicht leer sein.")
        return v


class UserUpdateSchema(BaseModel):
    # Alle Felder sind optional, weil beim Bearbeiten nicht immer alles geändert wird.
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    class_group_id: Optional[int] = None
    status: Optional[str] = None


# ─────────────────────────────────────────────
# ClassGroup Schemas
# ─────────────────────────────────────────────
class ClassGroupCreateSchema(BaseModel):
    # Eingabe für das Erstellen einer Klasse.
    name: str
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Klassenname darf nicht leer sein.")
        return v


# ─────────────────────────────────────────────
# Course Schemas
# ─────────────────────────────────────────────
class CourseCreateSchema(BaseModel):
    # Eingabe für ein Modul; der code dient später als kurzes eindeutiges Kürzel.
    name: str
    code: str
    default_semester: Optional[int] = None
    credits: Optional[float] = None

    @field_validator("name", "code")
    @classmethod
    def not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Dieses Feld darf nicht leer sein.")
        return v

    @field_validator("code")
    @classmethod
    def code_format(cls, v: str) -> str:
        # Modul-Code muss aus genau vier Ziffern bestehen (kein Buchstabe, kein Sonderzeichen).
        if not v.isdigit() or len(v) != 4:
            raise ValueError("Modul-Code muss genau 4 Ziffern enthalten.")
        return v

    @field_validator("credits")
    @classmethod
    def credits_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("Credits müssen positiv sein.")
        return v


# ─────────────────────────────────────────────
# Lecture Schemas
# ─────────────────────────────────────────────
class LectureCreateSchema(BaseModel):
    # Eingabe für eine Vorlesung im Stundenplan.
    class_group_course_id: int
    start_time: datetime
    end_time: datetime
    location: str
    notes: Optional[str] = None

    @model_validator(mode="after")
    def end_after_start(self) -> "LectureCreateSchema":
        # Eine Vorlesung darf nicht enden, bevor sie angefangen hat.
        if self.end_time <= self.start_time:
            raise ValueError("Endzeit muss nach der Startzeit liegen.")
        return self

    @field_validator("location")
    @classmethod
    def location_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Ort darf nicht leer sein.")
        return v


# ─────────────────────────────────────────────
# Task (Deadline) Schemas
# ─────────────────────────────────────────────
class TaskCreateSchema(BaseModel):
    # Eingabe für Aufgaben/Deadlines, die an ein Modul gebunden sind.
    class_group_course_id: int
    title: str
    type: TaskType
    due_date: datetime
    notes: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Titel darf nicht leer sein.")
        return v


# ─────────────────────────────────────────────
# Grade Schemas
# ─────────────────────────────────────────────
class GradeCreateSchema(BaseModel):
    # Eingabe für Noten; source_type sagt, ob die Note persönlich oder offiziell ist.
    course_id: int
    semester: Optional[int] = None
    grade_value: float
    weight: Optional[float] = None
    source_type: GradeSource
    notes: Optional[str] = None

    @field_validator("grade_value")
    @classmethod
    def grade_in_range(cls, v: float) -> float:
        # Schweizer Notensystem: 1.0 ist schlecht, 6.0 ist sehr gut.
        if not (1.0 <= v <= 6.0):
            raise ValueError("Note muss zwischen 1.0 und 6.0 liegen.")
        return round(v, 2)

    @field_validator("semester")
    @classmethod
    def semester_positive(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 1:
            raise ValueError("Semester muss mindestens 1 sein.")
        return v
