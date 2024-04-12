from fastapi import APIRouter, HTTPException, Path, Body
from typing import List
from uuid import UUID

from api.v1.costumers.schemas import CustomerCreate, Customer, CustomerUpdate, CustomerResponse
from db.models import Customer as DBCustomer
from db.session import DatabaseSessionManager, engine, get_session

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/create_customer", response_model=CustomerResponse)
def create_customer(customer_data: CustomerCreate):
    with DatabaseSessionManager(engine) as db:
        try:
            customer = DBCustomer(full_name=customer_data.full_name, email=customer_data.email)
            db.add(customer)
            db.commit()
            db.refresh(customer)
            return CustomerResponse(id=customer.id, full_name=customer.full_name, email=customer.email)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_customers", response_model=List[Customer])
def read_customers():
    with DatabaseSessionManager(engine) as db:
        try:
            customers = db.query(DBCustomer).all()
            return customers
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve customers: {str(e)}")


@router.get("/get_customer/{customer_id}", response_model=Customer)
def get_customer_details(customer_id: UUID = Path(..., description="The UUID of the customer to retrieve")):
    with DatabaseSessionManager(engine) as db:
        customer = db.query(DBCustomer).filter(DBCustomer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer


@router.put("/update_customer/{customer_id}", response_model=Customer)
def update_customer(customer_id: UUID = Path(..., description="The UUID of the customer to update"),
                    update_data: CustomerUpdate = Body(..., description="The data to update for the customer")):
    with DatabaseSessionManager(engine) as db:
        customer = db.query(DBCustomer).filter(DBCustomer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        if update_data.full_name is not None:
            customer.full_name = update_data.full_name
        if update_data.email is not None:
            customer.email = update_data.email

        db.commit()
        db.refresh(customer)
        return customer


@router.delete("/delete_customer/{customer_id}", status_code=204)
def delete_customer(customer_id: UUID = Path(..., description="The UUID of the customer to delete")):
    with DatabaseSessionManager(engine) as db:
        customer = db.query(DBCustomer).filter(DBCustomer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        db.delete(customer)
        db.commit()
        return {"message": "Customer successfully deleted"}


