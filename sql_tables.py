from datetime import date
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# SQLAlchemy ORM Model
class staging_customer_raw(Base):
    __tablename__ = 'main1'
    customer_id = Column(Integer, primary_key=True,autoincrement=True)
    customerID = Column(String(20))
    gender = Column(String(1))
    SeniorCitizen = Column(Integer)
    Partner = Column(String(20))
    Dependents = Column(String(20))
    tenure = Column(Integer)
    PhoneService = Column(String(20))
    MultipleLines = Column(String(20))
    InternetService = Column(String(20))
    OnlineSecurity = Column(String(20))
    OnlineBackup = Column(String(20))
    DeviceProtection = Column(String(20))
    TechSupport = Column(String(20))
    StreamingTV = Column(String(20))
    StreamingMovies = Column(String(20))
    Contract = Column(String(20))
    PaperlessBilling = Column(String(20))
    PaymentMethod = Column(String(20))
    MonthlyCharges = Column(Float)
    TotalCharges = Column(Float)
    Churn = Column(String(20))
    
 

class CustomerValidator(BaseModel):
    customerID :str
    gender : str
    SeniorCitizen : int
    Partner : str
    Dependents : str
    tenure : int
    PhoneService : str
    MultipleLines : str
    InternetService : str
    OnlineSecurity : str
    OnlineBackup : str
    DeviceProtection : str
    TechSupport : str
    StreamingTV : str
    StreamingMovies : str
    Contract : str
    PaperlessBilling : str
    PaymentMethod : str
    MonthlyCharges : float
    TotalCharges : float
    Churn : str
    
    class Config:
        from_attributes = True

class CustomerUpdate(BaseModel):
    customerID :str | None = None
    gender : str | None = None
    SeniorCitizen : int | None = None
    Partner : str | None = None
    Dependents : str | None = None
    tenure : int | None = None
    PhoneService : str | None = None 
    MultipleLines : str | None = None
    InternetService : str | None = None
    OnlineSecurity : str | None = None
    OnlineBackup : str | None = None 
    DeviceProtection : str | None = None 
    TechSupport : str | None = None 
    StreamingTV : str | None = None 
    StreamingMovies : str | None = None 
    Contract : str | None = None 
    PaperlessBilling : str | None = None 
    PaymentMethod : str | None = None 
    MonthlyCharges : float | None = None 
    TotalCharges : float | None = None 
    Churn : str | None = None 
    
    class Config:
        from_attributes = True

# Response model (includes id)
class CustomerResponse(BaseModel):
    customer_id : int
    customerID :str
    gender : str
    SeniorCitizen : int
    Partner : str
    Dependents : str
    tenure : int
    PhoneService : str
    MultipleLines : str
    InternetService : str
    OnlineSecurity : str
    OnlineBackup : str
    DeviceProtection : str
    TechSupport : str
    StreamingTV : str
    StreamingMovies : str
    Contract : str
    PaperlessBilling : str
    PaymentMethod : str
    MonthlyCharges : float
    TotalCharges : float
    Churn : str

    class Config:
        from_attributes = True

class HighRiskCustomerResponse(BaseModel):
    customerID :str
    tenure : int
    Contract : str
    MonthlyCharges : float
    Churn : str

    class Config:
        from_attributes = True


class CustomerFeatures(Base):
    __tablename__ = 'customer_features'
    id = Column(Integer, primary_key=True,autoincrement=True)
    customerID = Column(String(20))
    gender = Column(String(1))
    SeniorCitizen = Column(Integer)
    Partner = Column(String(20))
    Dependents = Column(String(20))
    tenure = Column(Integer)
    PhoneService = Column(String(20))
    MultipleLines = Column(String(20))
    InternetService = Column(String(20))
    OnlineSecurity = Column(String(20))
    OnlineBackup = Column(String(20))
    DeviceProtection = Column(String(20))
    TechSupport = Column(String(20))
    StreamingTV = Column(String(20))
    StreamingMovies = Column(String(20))
    Contract = Column(String(20))
    PaperlessBilling = Column(String(20))
    PaymentMethod = Column(String(20))
    MonthlyCharges = Column(Float)
    TotalCharges = Column(Float)
    Churn = Column(String(20))
    churn_flag = Column(Integer)
    tenure_bucket = Column(String(10))
    tenure_bucket_code = Column(Integer)
    high_charge_flag = Column(Integer)
    OnlineSecurity_flag = Column(Integer)
    OnlineBackup_flag = Column(Integer)
    DeviceProtection_flag = Column(Integer)
    TechSupport_flag = Column(Integer)
    StreamingTV_flag = Column(Integer)
    StreamingMovies_flag = Column(Integer)
    service_count = Column(Integer)
    is_long_term_customer = Column(Integer)
    has_streaming_bundle = Column(Integer)
    auto_pay_flag = Column(Integer)


class CustomerFeaturesResponse(BaseModel):
    service_count : int
    tenure_bucket : str
    high_charge_flag : int
    is_long_term_customer : int
    has_streaming_bundle : int
    auto_pay_flag : int
    MonthlyCharges : float
    TotalCharges : float

class ChurnPredictionRequest(BaseModel):
    tenure : int
    monthly_charges : float
    contract : str
    service_count : int
