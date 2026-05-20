"""
models.py – SQLModel-Datenbankentitäten (ORM).
Kompatibel mit SQLModel 0.0.21+ und Python 3.14.
"""
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from domain.datetime_utils import utc_now


# ─────────────────────────────────────────────
# Role
# ─────────────────────────────────────────────
class Role(SQLModel, table=True):
    __tablename__ = "role"

    # Jede Rolle wird in einer eigenen Tabelle gespeichert, damit User nur auf role_id verweisen.
    role_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True)

    users: List["User"] = Relationship(back_populates="role")


# ─────────────────────────────────────────────
# ClassGroup
# ─────────────────────────────────────────────
class ClassGroup(SQLModel, table=True):
    __tablename__ = "class_group"

    # Eine ClassGroup entspricht einer Klasse/Studiengruppe, z. B. INF2a.
    class_group_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

    # Relationships bilden die Verbindungen zwischen Tabellen als Python-Objekte ab.
    users: List["User"] = Relationship(back_populates="class_group")
    class_group_courses: List["ClassGroupCourse"] = Relationship(
        back_populates="class_group",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    dozent_assignments: List["DozentClass"] = Relationship(
        back_populates="class_group",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# ─────────────────────────────────────────────
# User
# ─────────────────────────────────────────────
class User(SQLModel, table=True):
    __tablename__ = "user"

    # User sind Studenten, Dozenten oder Admins; die konkrete Rolle kommt über role_id.
    user_id: Optional[int] = Field(default=None, primary_key=True)
    role_id: int = Field(foreign_key="role.role_id")
    class_group_id: Optional[int] = Field(default=None, foreign_key="class_group.class_group_id")
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str = Field(max_length=255, unique=True)
    status: str = Field(default="active", max_length=20)
    password_hash: str
    registration_date: datetime = Field(default_factory=utc_now)
    reset_token: Optional[str] = Field(default=None)
    reset_token_expires: Optional[datetime] = Field(default=None)
    class_assigned_at: Optional[datetime] = Field(default=None)

    # Über diese Relationships kann man später z. B. user.role.name oder user.class_group.name lesen.
    role: Optional[Role] = Relationship(back_populates="users")
    class_group: Optional[ClassGroup] = Relationship(back_populates="users")
    grades: List["Grade"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    tasks: List["Task"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    dozent_assignments: List["DozentCourse"] = Relationship(
        back_populates="dozent",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    dozent_classes: List["DozentClass"] = Relationship(
        back_populates="dozent",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# ─────────────────────────────────────────────
# Course
# ─────────────────────────────────────────────
class Course(SQLModel, table=True):
    __tablename__ = "course"

    # Ein Course ist ein Modul/Fach; code ist eindeutig, damit es keine doppelten Modulkürzel gibt.
    course_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    code: str = Field(max_length=50, unique=True)
    default_semester: Optional[int] = Field(default=None)
    credits: Optional[float] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

    grades: List["Grade"] = Relationship(
        back_populates="course",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    class_group_courses: List["ClassGroupCourse"] = Relationship(
        back_populates="course",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# ─────────────────────────────────────────────
# ClassGroupCourse
# ─────────────────────────────────────────────
class ClassGroupCourse(SQLModel, table=True):
    __tablename__ = "class_group_course"

    # Verbindungstabelle: Eine Klasse kann viele Module haben, ein Modul kann in vielen Klassen vorkommen.
    class_group_course_id: Optional[int] = Field(default=None, primary_key=True)
    class_group_id: int = Field(foreign_key="class_group.class_group_id")
    course_id: int = Field(foreign_key="course.course_id")
    semester: int

    class_group: Optional[ClassGroup] = Relationship(back_populates="class_group_courses")
    course: Optional[Course] = Relationship(back_populates="class_group_courses")
    lectures: List["Lecture"] = Relationship(
        back_populates="class_group_course",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    tasks: List["Task"] = Relationship(
        back_populates="class_group_course",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    dozent_assignments: List["DozentCourse"] = Relationship(
        back_populates="class_group_course",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# ─────────────────────────────────────────────
# DozentCourse
# ─────────────────────────────────────────────
class DozentCourse(SQLModel, table=True):
    __tablename__ = "dozent_course"

    # Spezifische Zuweisung: Dozent X unterrichtet genau dieses Modul in genau dieser Klasse.
    id: Optional[int] = Field(default=None, primary_key=True)
    dozent_id: int = Field(foreign_key="user.user_id")
    class_group_course_id: int = Field(foreign_key="class_group_course.class_group_course_id")

    dozent: Optional[User] = Relationship(back_populates="dozent_assignments")
    class_group_course: Optional[ClassGroupCourse] = Relationship(back_populates="dozent_assignments")


# ─────────────────────────────────────────────
# DozentClass (Dozent ↔ Klasse)
# ─────────────────────────────────────────────
class DozentClass(SQLModel, table=True):
    __tablename__ = "dozent_class"

    # Breitere Zuweisung: Ein Dozent gehört zu einer ganzen Klasse und sieht deren Module.
    id: Optional[int] = Field(default=None, primary_key=True)
    dozent_id: int = Field(foreign_key="user.user_id")
    class_group_id: int = Field(foreign_key="class_group.class_group_id")

    dozent: Optional[User] = Relationship(back_populates="dozent_classes")
    class_group: Optional[ClassGroup] = Relationship(back_populates="dozent_assignments")


# ─────────────────────────────────────────────
# Lecture
# ─────────────────────────────────────────────
class Lecture(SQLModel, table=True):
    __tablename__ = "lecture"

    # Eine Vorlesung hängt immer an einer Klassen-Modul-Zuweisung.
    lecture_id: Optional[int] = Field(default=None, primary_key=True)
    class_group_course_id: int = Field(foreign_key="class_group_course.class_group_course_id")
    start_time: datetime
    end_time: datetime
    location: str = Field(max_length=200)
    notes: Optional[str] = Field(default=None)

    class_group_course: Optional[ClassGroupCourse] = Relationship(back_populates="lectures")


# ─────────────────────────────────────────────
# Task (= Deadline / Prüfung)
# ─────────────────────────────────────────────
class Task(SQLModel, table=True):
    __tablename__ = "task"

    # Tasks können persönlich, für ein Modul oder für eine ganze Klasse sein.
    task_id: Optional[int] = Field(default=None, primary_key=True)
    creator_id: int = Field(foreign_key="user.user_id")
    class_group_course_id: Optional[int] = Field(
        default=None, foreign_key="class_group_course.class_group_course_id"
    )
    class_group_id: Optional[int] = Field(
        default=None, foreign_key="class_group.class_group_id"
    )
    title: str = Field(max_length=300)
    type: str = Field(max_length=20)          # z. B. "personal", "class", "exam", "submission"
    due_date: datetime
    notes: Optional[str] = Field(default=None)

    creator: Optional[User] = Relationship(back_populates="tasks")
    class_group_course: Optional[ClassGroupCourse] = Relationship(back_populates="tasks")
    class_group: Optional[ClassGroup] = Relationship()


# ─────────────────────────────────────────────
# Grade
# ─────────────────────────────────────────────
class Grade(SQLModel, table=True):
    __tablename__ = "grade"

    # Eine Note gehört zu einem User und einem Modul; source_type unterscheidet persönlich/offiziell.
    grade_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    semester: int
    grade_value: float
    weight: Optional[float] = Field(default=None)
    source_type: str = Field(max_length=20)
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=utc_now)

    user: Optional[User] = Relationship(back_populates="grades")
    course: Optional[Course] = Relationship(back_populates="grades")
