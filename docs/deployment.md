# Deployment Guide (Render + Neon + Vercel)

This project deploys the FastAPI backend to Render (free tier), the PostgreSQL database to Neon, and the Next.js frontend to Vercel. GitHub is the single source of truth; both Render and Vercel should be connected to the repo for automatic deployments.

## Environment variables

### Backend (`backend/.env.example`)
- `CDSS_APP_NAME` — display name for FastAPI docs (optional).
- `CDSS_DEBUG` — set to `False` in production.
- `DATABASE_URL` — SQLAlchemy DSN, e.g. `postgresql+psycopg2://<user>:<password>@<host>/<database>?sslmode=require` (Neon provides this in the dashboard).

### Frontend (`frontend/.env.example`)
- `NEXT_PUBLIC_API_BASE_URL` — public URL of the Render backend, e.g. `https://cdss-backend.onrender.com`.
- `NEXT_PUBLIC_REDIS_REST_URL` — optional Upstash Redis REST endpoint for shared cache (leave blank to fall back to memory/localStorage).
- `NEXT_PUBLIC_REDIS_REST_TOKEN` — bearer token paired with the Redis REST URL.

## Provision Neon (PostgreSQL)
1) Create a Neon project and database.
2) Create a role/password for the app.
3) Copy the **Pooled connection string** and append `?sslmode=require` if not already present.
4) Keep this string for `DATABASE_URL` in Render (and locally if needed).

## Deploy backend to Render (free web service)
1) Create a new **Web Service** from the GitHub repo and choose the `backend` directory as the root.
2) Environment: `Python 3.11` (or 3.10+). Region: choose nearest.
3) Build command: `pip install -r requirements.txt && alembic upgrade head`
4) Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5) Environment variables:
   - `DATABASE_URL` = Neon pooled URL
   - `CDSS_APP_NAME` = `CDSS Backend` (optional)
   - `CDSS_DEBUG` = `False`
6) After first deploy, visit the Render URL (e.g. `https://cdss-backend.onrender.com/docs`) to verify.

## Deploy frontend to Vercel
1) Create a new Vercel project, import the GitHub repo, and set **Root Directory** to `frontend`.
2) Framework preset: Next.js. Build command: default (`npm run build`); Output directory: `.next`.
3) Environment variables:
   - `NEXT_PUBLIC_API_BASE_URL` = Render backend URL
   - `NEXT_PUBLIC_REDIS_REST_URL` (optional)
   - `NEXT_PUBLIC_REDIS_REST_TOKEN` (optional)
4) Trigger deploy; once live, confirm pages hit the backend without CORS issues (backend currently allows `*`).

## Local development
1) Copy `.env.example` to `.env` in `backend/` and `.env.example` to `.env.local` in `frontend/`.
2) Start backend: `cd backend && uvicorn app.main:app --reload`.
3) Start frontend: `cd frontend && npm install && npm run dev`.

Notes
- Render free tier sleeps after inactivity; expect a cold start on first request.
- If Alembic needs a URL during migrations, it picks up `DATABASE_URL` from the environment; override `sqlalchemy.url` in `alembic.ini` if necessary.
