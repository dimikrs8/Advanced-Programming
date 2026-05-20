"""
enums.py – Enum-Klassen für typsichere Felder im Domain-Model.
"""
from enum import Enum


class RoleType(str, Enum):
    admin = "admin"
    student = "student"
    dozent = "dozent"


class GradeSource(str, Enum):
    personal = "personal"
    official = "official"


class TaskType(str, Enum):
    personal = "personal"
    class_ = "class"
    exam = "exam"
    submission = "submission"
    reminder = "reminder"
    learning = "learning"
    other = "other"


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
