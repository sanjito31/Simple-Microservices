from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.health import Health
from models.product import ProductCreate, ProductRead, ProductUpdate
from models.company import CompanyCreate, CompanyRead, CompanyUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
products: Dict[UUID, ProductRead] = {}
companies: Dict[UUID, CompanyRead] = {}

app = FastAPI(
    title="Product/Company API",
    description="Demo FastAPI app using Pydantic v2 models for Product and Company",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)


# -----------------------------------------------------------------------------
# Product endpoints
# -----------------------------------------------------------------------------
@app.post("/product", response_model=ProductCreate, status_code=201)
def create_product(product: ProductCreate):
    if product.id in products:
        raise HTTPException(status_code=400, detail="Product with this ID already exists")
    products[product.id] = ProductRead(**product.model_dump())
    return products[product.id]

@app.get("/product", response_model=List[ProductRead])
def list_products(
    name: Optional[str] = Query(None, description="Filter by name."),
    description: Optional[str] = Query(None, description="Filter by product description."),
    price: Optional[float] = Query(None, description="Filter by price of item in USD."),
    quantity: Optional[int] = Query(None, description="Filter by quantity of item in stock.")
):
    results = list(products.values())

    if name is not None:
        results = [a for a in results if a.name == name]
    if description is not None:
        results = [a for a in results if a.description == description]
    if price is not None:
        results = [a for a in results if a.price == price]
    if quantity is not None:
        results = [a for a in results if a.quantity == quantity]

    return results

@app.get("/products/{product_id}", response_model=ProductRead)
def get_products(product_id: UUID):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]

@app.patch("/products/{product_id}", response_model=ProductRead)
def update_product(product_id: UUID, update: ProductUpdate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    stored = products[product_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    products[product_id] = ProductRead(**stored)
    return products[product_id]

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: UUID):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found.")
    del products[product_id]


# -----------------------------------------------------------------------------
# Company endpoints
# -----------------------------------------------------------------------------
@app.post("/company", response_model=CompanyCreate, status_code=201)
def create_company(company: CompanyCreate):
    if company.id in companies:
        raise HTTPException(status_code=400, detail="Company with this ID already exists")
    companies[company.id] = CompanyRead(**company.model_dump())
    return companies[company.id]

@app.get("/company", response_model=List[CompanyRead])
def list_companies(
    name: Optional[str] = Query(None, description="Filter by name."),
    industry: Optional[str] = Query(None, description="Filter by industry."),
    employees: Optional[int] = Query(None, description="Filter by number of employees."),
    phone: Optional[str] = Query(None, description="Filter by phone number."),
    state: Optional[str] = Query(None, description="Filter by company home state.")
):
    results = list(companies.values())

    if name is not None:
        results = [a for a in results if a.name == name]
    if industry is not None:
        results = [a for a in results if a.industry == industry]
    if employees is not None:
        results = [a for a in results if a.employees == employees]
    if phone is not None:
        results = [a for a in results if a.phone == phone]
    if state is not None:
        results = [a for a in results if a.state == state]

    return results

@app.get("/companies/{company_id}", response_model=CompanyRead)
def get_companies(company_id: UUID):
    if company_id not in companies:
        raise HTTPException(status_code=404, detail="Company not found")
    return companies[company_id]

@app.patch("/companies/{company_id}", response_model=CompanyRead)
def update_company(company_id: UUID, update: CompanyUpdate):
    if company_id not in companies:
        raise HTTPException(status_code=404, detail="Company not found")
    stored = companies[company_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    companies[company_id] = CompanyUpdate(**stored)
    return companies[company_id]

@app.delete("/companies/{company_id}", status_code=204)
def delete_company(company_id: UUID):
    if company_id not in companies:
        raise HTTPException(status_code=404, detail="Company not found")
    del companies[company_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Product/Company API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
