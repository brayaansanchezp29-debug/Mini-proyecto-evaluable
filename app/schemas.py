from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category: str = Field(..., min_length=3)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True