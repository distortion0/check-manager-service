from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from db_ops.check_service.check_creator import CheckCreator
from db_ops.check_service.check_queries import get_checks, get_check_by_id
from db_utils.session import get_db
from deps.auth_dependancy import get_current_user
from models.check_model import Check
from models.user_model import User
from schemas.check_schema import CheckCreate, CheckResponse, CheckFilter
from utils.formatter import format_check_text

router = APIRouter()


@router.post("/", response_model=CheckResponse)
def create_check(check: CheckCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new check for the authenticated user.

    Args:
        check (CheckCreate): Check creation data.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        CheckResponse: The created check data.
    """
    creator = CheckCreator(db=db, user_id=current_user.id, check_data=check)
    return creator.create_check()


@router.get("/", response_model=List[CheckResponse])
def read_checks(
        filters: CheckFilter = Depends(),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Retrieve a list of checks for the authenticated user, with optional filters.

    Args:
        filters (CheckFilter): Filter parameters for checks.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        List[CheckResponse]: List of checks matching the filters.
    """
    checks = get_checks(db=db, current_user_id=current_user.id, filters=filters)
    return [CheckResponse(**check.to_dict()) for check in checks]


@router.get("/{check_id}", response_model=CheckResponse)
def read_check(check_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get a single check by ID for the authenticated user.

    Args:
        check_id (int): ID of the check.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Raises:
        HTTPException: If check not found or unauthorized.

    Returns:
        CheckResponse: Check data.
    """
    db_check = get_check_by_id(db=db, current_user_id=current_user.id, check_id=check_id)
    if db_check is None or db_check.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Check not found")
    return db_check


@router.get("/public/{token}", response_class=Response, include_in_schema=False)
def public_check_view(token: str, line_width: int = Query(32, gt=10, le=80), db: Session = Depends(get_db)):
    """
    Public endpoint to view a check by its public token, formatted as plain text.

    Args:
        token (str): Public token of the check.
        line_width (int): Formatting line width (default 32).
        db (Session): Database session.

    Raises:
        HTTPException: If check not found.

    Returns:
        Response: Plain text formatted check.
    """
    check = db.query(Check).filter(Check.public_token == token).first()
    if not check:
        raise HTTPException(status_code=404, detail="Check not found")

    formatted = format_check_text(check, line_width)
    return Response(content=formatted, media_type="text/plain")
