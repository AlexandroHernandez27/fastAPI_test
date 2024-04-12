from pydantic import BaseModel, UUID4
from decimal import Decimal


class LoanBase(BaseModel):
    amount: Decimal


class LoanCreate(LoanBase):
    customer_id: UUID4


class LoanUpdate(BaseModel):
    amount: Decimal = None


class LoanInDBBase(LoanBase):
    id: UUID4
    customer_id: UUID4

    class Config:
        orm_mode = True


class Loan(LoanInDBBase):
    pass
