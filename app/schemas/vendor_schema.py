from pydantic import BaseModel, EmailStr, ConfigDict


class VendorCreate(BaseModel):
    vendor_name: str
    email: EmailStr
    phone: str
    address: str
    is_active: bool = True


class VendorUpdate(BaseModel):
    vendor_name: str
    email: EmailStr
    phone: str
    address: str
    is_active: bool


class VendorResponse(BaseModel):
    id: int
    vendor_name: str
    email: EmailStr
    phone: str
    address: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)