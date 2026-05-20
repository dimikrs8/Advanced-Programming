"""
db.py – Datenbank-Engine, Session-Maker und create_db_and_tables().
expire_on_commit=False verhindert DetachedInstanceError in NiceGUI Pages,
da Objekte nach Session-Schluss noch lesbar bleiben.
"""
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session, create_engine
import config

engine = create_engine(
    config.DATABASE_URL,
    # SQLite erlaubt standardmäßig keinen Zugriff aus mehreren Threads.
    # NiceGUI kann aber mehrere Requests parallel bearbeiten, deshalb diese Option.
    connect_args={"check_same_thread": False},  # SQLite-spezifisch
    echo=False,
)

# expire_on_commit=False: Attribute bleiben nach session.close() lesbar.
# Das ist wichtig, weil UI-Code oft noch auf ORM-Objekte zugreift.
_SessionFactory = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


@contextmanager
def get_session():
    """
    Kontextmanager: öffnet eine Session, committed bei Erfolg,
    rollback bei Exception. Objekte bleiben nach __exit__ lesbar
    (expire_on_commit=False).
    """
    session = _SessionFactory()
    try:
        # Der aufrufende Code arbeitet innerhalb dieses Blocks mit derselben DB-Session.
        yield session
        session.commit()
    except Exception:
        # Bei Fehlern werden unfertige Änderungen verworfen.
        session.rollback()
        raise
    finally:
        # Sessions müssen geschlossen werden, damit DB-Verbindungen nicht offen bleiben.
        session.close()


def create_db_and_tables() -> None:
    """Erstellt alle Tabellen in der Datenbank (falls nicht vorhanden)."""
    # Der Import registriert alle SQLModel-Klassen in SQLModel.metadata.
    from domain import models  # noqa: F401
    SQLModel.metadata.create_all(engine)
