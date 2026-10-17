import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import jobs
from app.api import analyze, status

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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SOVA API",
    description="AI Video Compliance Analyzer",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "SOVA Backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "sova-backend",
    }
