from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime,UTC
from sql_connection import get_db
from sql_tables import staging_customer_raw, CustomerValidator, CustomerResponse, CustomerUpdate,HighRiskCustomerResponse,CustomerFeaturesResponse,CustomerFeatures, ChurnPredictionRequest

API_KEY = "Aniruddh"

async def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={
                "error": "UNAUTHORIZED",
                "message": "Invalid API Key",
                "status_code": 401,
                "timestamp": datetime.now(UTC).isoformat()
            }
        )

router = APIRouter(
    prefix="/customer",      # All routes start with /customer
    tags=["Customers"],
    dependencies = [Depends(verify_api_key)]
)


@router.get("/churn/summary")
def get_customer_churn_summary(db: Session = Depends(get_db)):
    churned_count = func.sum(
        case(
            (staging_customer_raw.Churn == "Yes",1),
            else_=0
        )
    )

    result = (
        db.query(
            func.count(staging_customer_raw.customer_id).label("total_customers"),
            churned_count.label("churned"),
            (
                churned_count * 100.0 / func.count(staging_customer_raw.customer_id)
            ).label("churn_rate")
        )
        .one()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No customer data found"
        )

    return {
        "total_customers": result.total_customers,
        "churned": result.churned or 0,
        "churn_rate": round(float(result.churn_rate or 0), 2),
    }

# CREATE endpoint
@router.post("/Create_customer/", response_model=CustomerResponse)
def create_customer(customer: CustomerValidator, db: Session = Depends(get_db)):
    
    # Step 1: Create SQLAlchemy object from Pydantic data
    
    new_customer = staging_customer_raw(**customer.model_dump())
    # Step 2: Add to session (marks for insertion)
    db.add(new_customer)
    
    # Step 3: Commit (actually save to database)
    db.commit()
    
    # Step 4: Refresh (reload from database to get ID)
    db.refresh(new_customer)

    return new_customer


@router.post("/predict_churn")
def predict_churn(request: ChurnPredictionRequest, db: Session = Depends(get_db)):
    return  {"customer_id": "N/A", "risk_score": 
    0.78, "prediction": "Likely to churn", "note": "stub — real model in ML4"} 

@router.get("/customers/high-risk", response_model=list[HighRiskCustomerResponse])
def get_high_risk_customers(min_tenure: int | None = None,max_tenure: int = 12, limit: int = 50, db: Session = Depends(get_db)):
    avg_monthly_charges = (
        db.query(func.avg(staging_customer_raw.MonthlyCharges))
        .scalar()
    )
    if min_tenure is None:
        customers = db.query(staging_customer_raw).filter(
            staging_customer_raw.tenure < max_tenure,
            staging_customer_raw.Contract == "Month-to-month",
            staging_customer_raw.MonthlyCharges >avg_monthly_charges
        ).limit(limit)
    else:
        customers = db.query(staging_customer_raw).filter(
            staging_customer_raw.tenure > min_tenure,
            staging_customer_raw.tenure <= max_tenure,
            staging_customer_raw.Contract == "Month-to-month",
            staging_customer_raw.MonthlyCharges>avg_monthly_charges
        ).limit(limit)
    return customers.all()


@router.get("/customer/{id}/features",response_model=CustomerFeaturesResponse)
def get_customer_features(id: int, db: Session = Depends(get_db)):
    customer = db.query(CustomerFeatures).filter(CustomerFeatures.id == id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )
    return customer



@router.get("/{id}", response_model=CustomerResponse)
def get_customer(id: int, db: Session = Depends(get_db)):
 
    customer = db.query(staging_customer_raw).filter(staging_customer_raw.customer_id == id).first()
    
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer



@router.patch("/{id}", response_model=CustomerResponse)
def update_customer(id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """Update a specific customer by ID"""
    
    # SQLAlchemy query
    existing_customer = db.query(staging_customer_raw).filter(staging_customer_raw.customer_id == id).first()
    
    if not existing_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    updated_customer=customer.model_dump(exclude_unset=True)

    for field, value in updated_customer.items():
        setattr(existing_customer, field, value)

    db.commit()
    db.refresh(existing_customer)

    return existing_customer


@router.delete("/{id}", response_model=CustomerResponse)
def delete_customer(id: int, db: Session = Depends(get_db)):

    deleted_customer = db.query(staging_customer_raw).filter(staging_customer_raw.customer_id == id).first()
    
    if not deleted_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(deleted_customer)
    db.commit()

    return deleted_customer 