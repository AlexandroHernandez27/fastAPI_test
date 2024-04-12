from pydantic import BaseModel, EmailStr, UUID4, Field


class CustomerCreate(BaseModel):
    full_name: str
    email: EmailStr


class CustomerResponse(BaseModel):
    id: UUID4
    full_name: str
    email: EmailStr


class Customer(BaseModel):
    id: UUID4
    full_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class CustomerUpdate(BaseModel):
    full_name: str = Field(None, example="Jane Doe")
    email: EmailStr = Field(None, example="jane@example.com")
