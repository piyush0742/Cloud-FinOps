import random
import time
from fastapi import FastAPI, HTTPException
from app.telemetry import setup_telemetry
from opentelemetry import trace
from prometheus_fastapi_instrumentator import Instrumentator

setup_telemetry("auth-service")
tracer = trace.get_tracer(__name__)

app = FastAPI()
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/login")
def login():
    with tracer.start_as_current_span("auth-login"):
        delay = random.uniform(0.05, 0.2)
        time.sleep(delay)
        return {"message": "login successful", "latency": delay}

@app.get("/error")
def error():
    with tracer.start_as_current_span("auth-error"):
        if random.random() < 0.3:
            raise HTTPException(status_code=500, detail="Auth failure")
        return {"message": "ok"}
