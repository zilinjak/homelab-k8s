import asyncio
import logging
import random
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from opentelemetry import trace

from db import init_db, save_result, get_all_results


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (nothing to do)


app = FastAPI(lifespan=lifespan)

# Get tracer for manual instrumentation
tracer = trace.get_tracer(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/random-request")
async def random_request():
    """
    Endpoint that takes random time to complete, makes HTTP request to httpbin,
    and stores results in SQLite. Randomly fails ~20% of the time.
    """
    logging.getLogger(__name__).info("Foo")
    # Random delay between 0.5 and 3 seconds
    delay = random.uniform(0.5, 3.0)

    with tracer.start_as_current_span("random_delay") as span:
        span.set_attribute("delay.seconds", delay)
        await asyncio.sleep(delay)

    # Randomly fail ~20% of the time
    if random.random() < 0.2:
        raise HTTPException(status_code=500, detail="Random failure occurred")

    # Choose a random httpbin endpoint
    httpbin_endpoints = [
        "/get",
        "/ip",
        "/user-agent",
        "/headers",
        "/uuid",
    ]
    endpoint = random.choice(httpbin_endpoints)
    url = f"https://httpbin.zilinek.cloud{endpoint}"

    # Make HTTP request (automatically instrumented by opentelemetry-instrumentation-httpx)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    # Save result to database
    result_id = save_result(
        endpoint=endpoint,
        status_code=response.status_code,
        response_size=len(response.content),
        delay=delay
    )

    return {
        "delay_seconds": round(delay, 2),
        "httpbin_endpoint": endpoint,
        "status_code": response.status_code,
        "response_size": len(response.content),
        "db_record_id": result_id,
        "response_data": response.json()
    }


@app.get("/results")
async def get_results_endpoint():
    """Get all stored results from the database."""
    results = get_all_results()
    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

