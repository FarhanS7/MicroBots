from fastapi import FastAPI

app = FastAPI(
    title="MicroBots Execution Broker",
    version="0.1.0",
    description="Privileged sandbox execution broker for tool and browser actions",
)

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "microbots-executor", "version": "0.1.0"}
