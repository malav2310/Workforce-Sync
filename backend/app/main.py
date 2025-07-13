from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import scheduler

print("Starting Workforce Sync API...")

app = FastAPI(
    title="Workforce Sync API",
    description="API for scheduling employee shifts using bipartite matching",
    version="1.0.0"
)

# Add CORS middleware (optional, if needed for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the scheduler router
app.include_router(scheduler.router)

@app.get("/")
async def root():
    """Root endpoint for health check or API info."""
    return {"message": "Welcome to Workforce Sync API. Access /scheduler/assigned-schedules for schedules."}