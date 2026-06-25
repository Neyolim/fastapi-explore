from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from models import Product
from database import session, engine
import database_models

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
database_models.Base.metadata.create_all(bind=engine)

# Sample data
products = [
    Product(
        id=1,
        name="Phone",
        description="A smartphone",
        price=699.99,
        quantity=50,
    ),
    Product(
        id=2,
        name="Laptop",
        description="A powerful laptop",
        price=999.99,
        quantity=30,
    ),
    Product(
        id=3,
        name="Pen",
        description="A blue ink pen",
        price=1.99,
        quantity=100,
    ),
    Product(
        id=4,
        name="Table",
        description="A wooden table",
        price=199.99,
        quantity=20,
    ),
]


# Database Dependency
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


# Seed Database
def init_db():
    db = session()

    try:
        count = db.query(database_models.Product).count()

        if count == 0:
            for product in products:
                db.add(
                    database_models.Product(
                        **product.model_dump()
                    )
                )

            db.commit()

    finally:
        db.close()


init_db()


@app.get("/")
def greet():
    return {"message": "Welcome to FastAPI Web Framework"}


# Get All Products
@app.get("/products")
def get_all_products(
    db: Session = Depends(get_db)
):
    return db.query(
        database_models.Product
    ).all()


# Get Product By ID
@app.get("/products/{id}")
def get_product_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    product = (
        db.query(database_models.Product)
        .filter(
            database_models.Product.id == id
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


# Add Product
@app.post("/products")
def add_product(
    product: Product,
    db: Session = Depends(get_db),
):
    existing_product = (
        db.query(database_models.Product)
        .filter(
            database_models.Product.id
            == product.id
        )
        .first()
    )

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product already exists",
        )

    new_product = database_models.Product(
        **product.model_dump()
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# Update Product
@app.put("/products/{id}")
def update_product(
    id: int,
    product: Product,
    db: Session = Depends(get_db),
):
    db_product = (
        db.query(database_models.Product)
        .filter(
            database_models.Product.id == id
        )
        .first()
    )

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity

    db.commit()
    db.refresh(db_product)

    return db_product


# Delete Product
@app.delete("/products/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db),
):
    db_product = (
        db.query(database_models.Product)
        .filter(
            database_models.Product.id == id
        )
        .first()
    )

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    db.delete(db_product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }
