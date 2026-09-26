from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models import ProductInventory
from app.schemas import (
    ProductInventoryCreate,
    ProductInventoryUpdate,
    ProductInventoryRead,
)

router = APIRouter(prefix="/product-inventory", tags=["Product Inventory"])


@router.post("", response_model=ProductInventoryRead, status_code=status.HTTP_201_CREATED)
def create_product_inventory(payload: ProductInventoryCreate, db: Session = Depends(get_db)):
    inventory = ProductInventory(**payload.model_dump())
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


@router.get("", response_model=list[ProductInventoryRead])
def list_product_inventory(db: Session = Depends(get_db)):
    return db.query(ProductInventory).all()


@router.get("/{inventory_id}", response_model=ProductInventoryRead)
def get_product_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(ProductInventory).filter(ProductInventory.id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product inventory not found")
    return inventory


@router.patch("/{inventory_id}", response_model=ProductInventoryRead)
def update_product_inventory(
    inventory_id: int, payload: ProductInventoryUpdate, db: Session = Depends(get_db)
):
    inventory = db.query(ProductInventory).filter(ProductInventory.id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product inventory not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(inventory, field, value)

    db.commit()
    db.refresh(inventory)
    return inventory


@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = db.query(ProductInventory).filter(ProductInventory.id == inventory_id).first()
    if inventory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product inventory not found")

    db.delete(inventory)
    db.commit()