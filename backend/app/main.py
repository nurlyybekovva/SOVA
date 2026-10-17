import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app import jobs
from backend.app.api import analyze, status

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    jobs.init_db()
    yield


app = FastAPI(title="SOVA API", lifespan=lifespan)

# lets the React dev server (participant #2) call the API
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(analyze.router, prefix="/api/v1")
app.include_router(status.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"ok": True}