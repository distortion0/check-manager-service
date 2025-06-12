from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.orm import Session

from config import config
from db_ops.user_service.user_queries import get_user_by_username, verify_password, create_user
from db_utils.session import get_db
from schemas.user_schema import UserCreate

router = APIRouter()


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token with an optional expiry.
    Args:
        data (dict): Data to encode in the token.
        expires_delta (timedelta, optional): Token expiration time.
    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user if username is not taken.
    Args:
        user (UserCreate): User registration data.
        db (Session): DB session.
    Returns:
        User: Created user object.
    Raises:
        HTTPException: If username exists.
    """
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    Args:
        form_data (OAuth2PasswordRequestForm): Login credentials.
        db (Session): DB session.
    Returns:
        dict: Access token and type.
    Raises:
        HTTPException: If credentials invalid.
    """
    db_user = get_user_by_username(db, username=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
