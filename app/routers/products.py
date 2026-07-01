from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

def error_response(code: str, message: str):
    return {"error": {"code": code, "message": message}}

@router.get("/", response_model=list[schemas.ProductResponse], status_code=status.HTTP_200_OK)
def list_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@router.get("/{product_id}", response_model=schemas.ProductResponse, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response("PRODUCT_NOT_FOUND", "El producto solicitado no existe")
        )
    return product

@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    existing = crud.get_product_by_name(db, product.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error_response("PRODUCT_ALREADY_EXISTS", "Ya existe un producto con ese nombre")
        )
    return crud.create_product(db, product)

@router.put("/{product_id}", response_model=schemas.ProductResponse, status_code=status.HTTP_200_OK)
def update_product(product_id: int, product_data: schemas.ProductUpdate, db: Session = Depends(get_db)):
    update_data = product_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response("EMPTY_UPDATE_BODY", "Debe enviar al menos un campo para actualizar")
        )
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response("PRODUCT_NOT_FOUND", "El producto solicitado no existe")
        )
    if "name" in update_data:
        existing = crud.get_product_by_name(db, update_data["name"])
        if existing and existing.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_response("PRODUCT_ALREADY_EXISTS", "Ya existe un producto con ese nombre")
            )
    return crud.update_product(db, product_id, update_data)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response("PRODUCT_NOT_FOUND", "El producto solicitado no existe")
        )
    crud.delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)