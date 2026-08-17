from fastapi import FastAPI, Request
from sql_connection import engine, Base
from routers import router
import logging

# Create all tables defined in Base
# (If they don't exist)
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Custom API")

# Include router with all endpoints
app.include_router(router)

logging.basicConfig(
    filename=r"C:\Users\aniruddh.singh\OneDrive - Prodapt Solutions Private Limited\Documents\Project_prac\Churn.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

@app.middleware("http")
async def log_requests(request: Request, call_next):

    response = await call_next(request)

    logging.info(
        f"path={request.url.path} "
        f"method={request.method} "
        f"status={response.status_code}"
    )

    return response