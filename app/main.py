from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from routers import client_routes, rate_limit_routes, log_routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rate Limiter Service",
    description="A service to manage rate limiting for API clients using token bucket algorithm",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(client_routes.router)
app.include_router(rate_limit_routes.router)
app.include_router(log_routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Rate Limiter Service", "version": "1.0.0"}

