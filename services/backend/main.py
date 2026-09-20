from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MicroBots API",
    version="0.1.0",
    description="Backend API and Agent Control Service for MicroBots",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "microbots-backend", "version": "0.1.0"}
