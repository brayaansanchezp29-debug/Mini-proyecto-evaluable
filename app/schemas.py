from pydantic import BaseModel, Field, field_validator
from typing import Optional

NOMBRES_NO_PERMITIDOS = ["test", "prueba", "producto"]

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0, le=10000000)
    stock: int = Field(..., ge=0, le=10000)
    category: str = Field(..., min_length=3)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        name = value.strip()
        if not name:
            raise ValueError("El nombre no puede estar vacío o contener solo espacios")
        if name.lower() in NOMBRES_NO_PERMITIDOS:
            raise ValueError("El nombre del producto no está permitido")
        return name

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    price: Optional[float] = Field(None, gt=0, le=10000000)
    stock: Optional[int] = Field(None, ge=0, le=10000)
    category: Optional[str] = Field(None, min_length=3)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if value is None:
            return value
        name = value.strip()
        if not name:
            raise ValueError("El nombre no puede estar vacío o contener solo espacios")
        if name.lower() in NOMBRES_NO_PERMITIDOS:
            raise ValueError("El nombre del producto no está permitido")
        return name

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True