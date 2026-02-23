"""
DataSentinel Backend API
FastAPI application for data validation
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import connectors, validation

# Create FastAPI app
app = FastAPI(
    title="DataSentinel API",
    description="API for data quality validation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(connectors.router, prefix="/api", tags=["connectors"])
app.include_router(validation.router, prefix="/api", tags=["validation"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DataSentinel API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
