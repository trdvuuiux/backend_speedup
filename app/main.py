from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn

from app.core.config import settings
from app.api.auth.auth_routes import router as auth_router
from app.api.content.content_routes import router as content_router
from app.api.admin.admin_routes import router as admin_router
from app.core.database import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FIX 1: Dùng lifespan thay cho on_event (deprecated) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the app (startup & shutdown)"""
    # Startup logic
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")
    
    yield
    
    # Shutdown logic (nếu cần clean up resource thì viết ở đây)
    logger.info("Shutting down...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="1.0.0",
    lifespan=lifespan  # Đăng ký lifespan tại đây
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(auth_router)
app.include_router(content_router)
app.include_router(admin_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "success": True,
        "message": "Welcome to Speed Up API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "status": "healthy"
    }

if __name__ == "__main__":
    # --- FIX 2: Sửa đường dẫn import cho uvicorn ---
    uvicorn.run(
        "app.main:app",  # Đã sửa từ "main:app" thành "app.main:app"
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )