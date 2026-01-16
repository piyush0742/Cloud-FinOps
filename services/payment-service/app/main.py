import random
import asyncio
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from prometheus_fastapi_instrumentator import Instrumentator
from app.telemetry import setup_telemetry

# Telemetry setup
setup_telemetry("payment-service")
tracer = trace.get_tracer(__name__)

# FastAPI app
app = FastAPI(title="Payment Service")

# Prometheus metrics
Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False
)

@app.get("/health")
async def root_health():
    return {"status": "ok"}


@app.get("/payment/health")
async def health():
    return {"status": "ok"}

@app.post("/payment/payments")
async def process_payment():
    with tracer.start_as_current_span("process-payment"):
        latency = random.uniform(0.1, 0.5)
        await asyncio.sleep(latency)

        if random.random() < 0.2:
            raise HTTPException(status_code=402, detail="Payment failed")

        return {
            "message": "Payment processed successfully",
            "transaction_id": random.randint(10000, 99999),
            "latency": latency
        }

@app.get("/payment/payments/{payment_id}")
async def get_payment(payment_id: int):
    with tracer.start_as_current_span("get-payment"):
        latency = random.uniform(0.05, 0.2)
        await asyncio.sleep(latency)

        return {
            "payment_id": payment_id,
            "status": "SUCCESS",
            "latency": latency
        }

@app.get("/payment/error")
async def error():
    with tracer.start_as_current_span("payment-error"):
        if random.random() < 0.3:
            raise HTTPException(status_code=500, detail="Payment service error")
        return {"message": "ok"}
