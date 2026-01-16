import random
import asyncio
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from prometheus_fastapi_instrumentator import Instrumentator
from app.telemetry import setup_telemetry

# Telemetry setup
setup_telemetry("order-service")
tracer = trace.get_tracer(__name__)

# FastAPI app
app = FastAPI(title="Order Service")

# Prometheus metrics
Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False
)

@app.get("/health")
async def root_health():
    return {"status": "ok"}

@app.get("/order/health")
async def health():
    return {"status": "ok"}

@app.get("/order/orders")
async def get_orders():
    with tracer.start_as_current_span("get-orders"):
        latency = random.uniform(0.05, 0.3)
        await asyncio.sleep(latency)

        return {
            "orders": [
                {"order_id": 1, "item": "Laptop", "status": "PLACED"},
                {"order_id": 2, "item": "Phone", "status": "SHIPPED"}
            ],
            "latency": latency
        }

@app.post("/order/orders")
async def create_order():
    with tracer.start_as_current_span("create-order"):
        latency = random.uniform(0.1, 0.4)
        await asyncio.sleep(latency)

        return {
            "message": "Order created successfully",
            "order_id": random.randint(1000, 9999),
            "latency": latency
        }

@app.get("/order/error")
async def error():
    with tracer.start_as_current_span("order-error"):
        if random.random() < 0.25:
            raise HTTPException(status_code=500, detail="Order processing failed")
        return {"message": "ok"}
