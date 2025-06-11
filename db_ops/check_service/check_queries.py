from typing import List

from sqlalchemy.orm import Session, joinedload

from db_ops.check_service.check_filters import apply_check_filters
from models.check_model import Check
from schemas.check_schema import CheckFilter


def get_checks(db: Session, current_user_id: int, filters: CheckFilter) -> List[Check]:
    """
    Retrieve a list of checks for the current user applying given filters and pagination.

    Args:
        db (Session): Database session.
        current_user_id (int): ID of the current authenticated user.
        filters (CheckFilter): Filter and pagination parameters.

    Returns:
        List[Check]: List of Check objects matching the filters and user.
    """
    query = db.query(Check).filter(Check.user_id == current_user_id)
    query = apply_check_filters(query, filters)
    query = query.order_by(Check.created_at.desc()) \
        .offset(filters.offset) \
        .limit(filters.limit)
    return query.all()


def get_check_by_id(db: Session, current_user_id: int, check_id: int) -> Check | None:
    """
    Retrieve a single check by its ID for the current user, including related products.

    Args:
        db (Session): Database session.
        current_user_id (int): ID of the current authenticated user.
        check_id (int): ID of the check to retrieve.

    Returns:
        Optional[Check]: Check object if found, otherwise None.
    """
    return (
        db.query(Check)
        .options(joinedload(Check.products))
        .filter(Check.id == check_id, Check.user_id == current_user_id)
        .first()
    )
