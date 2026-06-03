import os
from datetime import datetime, timezone

from fastapi import FastAPI


app = FastAPI(title="CloudOps API")


@app.get("/")
def read_root():
    return {
        "service": "cloudops-api",
        "status": "running",
        "message": "AWS ECS Fargate deployment lab",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


@app.get("/version")
def version():
    return {
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("APP_ENV", "dev"),
    }


@app.get("/metadata")
def metadata():
    return {
        "service": "cloudops-api",
        "runtime": "FastAPI",
        "containerized": True,
        "target_platform": "AWS ECS Fargate",
        "logs": "CloudWatch",
    }


@app.get("/error")
def intentional_error():
    raise Exception("Intentional test error for CloudWatch log validation")
