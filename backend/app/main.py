from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api import drug_routes, clinical_routes, admin_routes, sync_routes, auth_routes
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="1.0", debug=settings.debug)

    origins = [os.getenv("CDSS_FRONTEND_ORIGIN", "http://localhost:3000")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(drug_routes.router)
    app.include_router(clinical_routes.router)
    app.include_router(admin_routes.router)
    app.include_router(sync_routes.router)
    app.include_router(auth_routes.router)

    @app.get("/", tags=["meta"])
    def root():
        return {
            "message": "CDSS Backend API",
            "docs": "/docs",
            "redoc": "/redoc",
            "endpoints": {
                "search_drugs": "/drugs/search",
                "drug_detail": "/drugs/{id}",
                "clinical": {
                    "drugs_by_side_effect": "/clinical/drugs-by-side-effect?name=",
                    "drugs_by_disease": "/clinical/drugs-by-disease?name=",
                    "drug_contraindications": "/clinical/drug-contraindications?condition=",
                    "drug_interactions": "/clinical/drug-interactions?drug=",
                    "drugs_by_ecg_effect": "/clinical/drugs-by-ecg-effect?effect=",
                },
            },
        }

    return app


app = create_app()
