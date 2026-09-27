from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import CustomerAddress
from app.schemas import (
    CustomerAddressCreate,
    CustomerAddressUpdate,
    CustomerAddressRead,
)

router = APIRouter(prefix="/users/{user_id}/addresses", tags=["Customer Addresses"])


@router.post("", response_model=CustomerAddressRead, status_code=status.HTTP_201_CREATED)
def create_customer_address(user_id: int, payload: CustomerAddressCreate, db: Session = Depends(get_db)):
    address = CustomerAddress(**payload.model_dump(), user_id=user_id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.get("", response_model=list[CustomerAddressRead])
def list_customer_addresses(user_id: int, db: Session = Depends(get_db)):
    return db.query(CustomerAddress).filter(CustomerAddress.user_id == user_id).all()


@router.get("/{address_id}", response_model=CustomerAddressRead)
def get_customer_address(user_id: int, address_id: int, db: Session = Depends(get_db)):
    address = (
        db.query(CustomerAddress)
        .filter(CustomerAddress.id == address_id, CustomerAddress.user_id == user_id)
        .first()
    )
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer address not found")
    return address


@router.patch("/{address_id}", response_model=CustomerAddressRead)
def update_customer_address(
    user_id: int, address_id: int, payload: CustomerAddressUpdate, db: Session = Depends(get_db)
):
    address = (
        db.query(CustomerAddress)
        .filter(CustomerAddress.id == address_id, CustomerAddress.user_id == user_id)
        .first()
    )
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer address not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_address(user_id: int, address_id: int, db: Session = Depends(get_db)):
    address = (
        db.query(CustomerAddress)
        .filter(CustomerAddress.id == address_id, CustomerAddress.user_id == user_id)
        .first()
    )
    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer address not found")

    db.delete(address)
    db.commit()