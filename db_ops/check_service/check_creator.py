from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.check_model import Check, CheckProduct
from schemas.check_schema import CheckCreate


class CheckCreator:
    """
   Handles creation of a check with products and payment validation.
   """

    def __init__(self, db: Session, user_id: int, check_data: CheckCreate):
        """
        Initialize CheckCreator.

        Args:
            db (Session): SQLAlchemy DB session.
            user_id (int): ID of the user creating the check.
            check_data (CheckCreate): Input data for the check.
        """
        self.db = db
        self.user_id = user_id
        self.check_data = check_data
        self.check_obj = None
        self.products_data = []

    def create_check(self) -> dict:
        """
        Create the check with products, calculate totals and rest.

        Raises:
            HTTPException: If payment amount is less than total amount due.

        Returns:
            dict: Created check data including products, totals, and payment info.
        """
        self._create_check_object()
        self._add_products()
        try:
            self._finalize_check()
        except ValueError as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        return self._build_response()

    def _create_check_object(self) -> None:
        """
        Create and add Check object to the DB session.
        """
        self.check_obj = Check(
            user_id=self.user_id,
            payment_type=self.check_data.payment.type,
            payment_amount=self.check_data.payment.amount,
            additional_data=self.check_data.additional_data,
        )
        self.db.add(self.check_obj)
        self.db.flush()

    def _add_products(self) -> None:
        """
        Create CheckProduct objects for each product in input and add to DB.
        """
        for product in self.check_data.products:
            product_obj = CheckProduct(
                check_id=self.check_obj.id,
                name=product.name,
                price=product.price,
                quantity=product.quantity,
            )
            product_obj.calculate_total()
            self.db.add(product_obj)
            self.products_data.append({
                "name": product_obj.name,
                "price": product_obj.price,
                "quantity": product_obj.quantity,
                "total": product_obj.total,
            })

    def _finalize_check(self) -> None:
        """
        Calculate totals and rest, commit transaction, refresh check object.

        Raises:
            ValueError: If payment amount is less than total amount due.
        """
        self.db.flush()
        self.db.refresh(self.check_obj)

        self.check_obj.calculate_total()
        self.check_obj.calculate_rest()

        self.db.commit()
        self.db.refresh(self.check_obj)

    def _build_response(self) -> dict:
        """
        Build response dictionary with check and products info.

        Returns:
            dict: Check details ready to return to client.
        """
        return {
            "id": self.check_obj.id,
            "products": self.products_data,
            "payment": {
                "type": self.check_data.payment.type,
                "amount": self.check_data.payment.amount,
            },
            "total": self.check_obj.total,
            "rest": self.check_obj.rest,
            "created_at": self.check_obj.created_at,
            "additional_data": self.check_obj.additional_data,
        }
