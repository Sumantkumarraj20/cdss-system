from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    admin_routes,
    auth_routes,
    clinical_routes,
    drug_routes,
    sync_routes,
)

app = FastAPI(
    title="CDSS API",
    version="1.0",
    docs_url="/docs",
)

# CORS
origins = [
    "http://localhost:3000",
    "https://cdss-system.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTERS
app.include_router(auth_routes.router)
app.include_router(admin_routes.router)
app.include_router(drug_routes.router)
app.include_router(clinical_routes.router)
app.include_router(sync_routes.router)