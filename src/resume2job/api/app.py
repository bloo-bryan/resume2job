from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from resume2job.api.routes import evaluation, health, match, parse

app = FastAPI(
    title="Resume2Job",
    description="Resume-to-job matching engine",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(health.router)
app.include_router(parse.router)
app.include_router(match.router)
app.include_router(evaluation.router)
