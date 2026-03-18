from fastapi import FastAPI

from resume2job.api.routes import evaluation, health, match, parse

app = FastAPI(
    title="Resume2Job",
    description="Resume-to-job matching engine",
    version="0.1.0",
)

app.include_router(health.router)
app.include_router(parse.router)
app.include_router(match.router)
app.include_router(evaluation.router)
