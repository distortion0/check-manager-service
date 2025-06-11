from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models.user_model import User
from schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user from the database by their username.

    Args:
        db (Session): Database session.
        username (str): Username to search for.

    Returns:
        User | None: User object if found, else None.
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    """
    Create a new user with a hashed password and save to the database.

    Args:
        db (Session): Database session.
        user (UserCreate): User data including plain password.

    Returns:
        User: Created User object.
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_password(plain_password, hashed_password):
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): Plain text password.
        hashed_password (str): Hashed password stored in the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
