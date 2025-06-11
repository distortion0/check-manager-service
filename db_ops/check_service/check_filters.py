from models.check_model import Check
from schemas.check_schema import CheckFilter


def apply_check_filters(query, filters: CheckFilter):
    """
    Apply filters to a SQLAlchemy Check query based on provided filter criteria.

    Args:
        query: SQLAlchemy query object for Check model.
        filters (CheckFilter): Filter criteria including date range, minimum total, and payment type.

    Returns:
        The filtered SQLAlchemy query object.
    """
    if filters.date_from:
        query = query.filter(Check.created_at >= filters.date_from)
    if filters.date_to:
        query = query.filter(Check.created_at <= filters.date_to)
    if filters.min_total:
        query = query.filter(Check.total >= filters.min_total)
    if filters.payment_type:
        query = query.filter(Check.payment_type == filters.payment_type)
    return query
