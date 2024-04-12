from fastapi import APIRouter, HTTPException, Depends, Path, Body
from typing import List
from uuid import UUID

from db.session import DatabaseSessionManager, engine, get_session
from db.models.models import Loan as DBLoan, Customer as DBCustomer
from api.v1.loans.schemas import Loan, LoanCreate, LoanUpdate, LoanInDBBase

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/create_loan", response_model=Loan, status_code=201)
def create_loan(loan: LoanCreate):
    with DatabaseSessionManager(engine) as db:
        if not db.query(DBCustomer).filter(DBCustomer.id == loan.customer_id).first():
            raise HTTPException(status_code=404, detail="Customer not found")
        new_loan = DBLoan(amount=loan.amount, customer_id=loan.customer_id)
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return new_loan


@router.get("/get_loans", response_model=List[Loan])
def get_loans():
    with DatabaseSessionManager(engine) as db:
        loans = db.query(DBLoan).all()
        return loans


@router.get("/get_loan/{loan_id}", response_model=Loan)
def get_loan(loan_id: UUID = Path(...)):
    with DatabaseSessionManager(engine) as db:
        loan = db.query(DBLoan).filter(DBLoan.id == loan_id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        return loan


@router.put("/update_loan/{loan_id}", response_model=Loan)
def update_loan(loan_id: UUID = Path(...), loan_data: LoanUpdate = Body(...)):
    with DatabaseSessionManager(engine) as db:
        loan = db.query(DBLoan).filter(DBLoan.id == loan_id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        if loan_data.amount is not None:
            loan.amount = loan_data.amount
        db.commit()
        return loan


@router.delete("/delete_loan/{loan_id}", status_code=204)
def delete_loan(loan_id: UUID = Path(...)):
    with DatabaseSessionManager(engine) as db:
        loan = db.query(DBLoan).filter(DBLoan.id == loan_id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        db.delete(loan)
        db.commit()
        return {"message": "Loan successfully deleted"}
