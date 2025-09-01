from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model.model import get_prediction, __version__, model, MODEL_PATH
from datetime import datetime, timezone
import torch
import os
from typing import Dict, Any

app = FastAPI()

# List of allowed origins
origins = [
    "http://localhost:3000",  # for local testing
    "https://playing-card-classifier.vercel.app",  # for prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


class PredictionOut(BaseModel):
    card: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    model_loaded: bool
    model_path: str
    device: str
    dependencies: Dict[str, Any]


@app.get("/")
def home():
    """
    Home endpoint.
    """
    return {
        "model": "pytorch_playing_cards_model",
        "version": __version__,
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Comprehensive health check endpoint following best practices.

    Returns:
        HealthResponse: Detailed health status including:
        - Overall service status
        - Timestamp
        - Model version
        - Model loading status
        - Model file path
        - Device (CPU/GPU)
        - Dependency status
    """
    try:
        # Check if model file exists
        model_file_exists = os.path.exists(MODEL_PATH)

        # Check if model is properly loaded and can perform inference
        model_loaded = False
        if model_file_exists and model is not None:
            try:
                # Test model with a dummy tensor to ensure it's working
                dummy_input = torch.randn(1, 3, 128, 128)
                with torch.no_grad():
                    _ = model(dummy_input)
                model_loaded = True
            except Exception as e:
                model_loaded = False

        # Check critical dependencies
        dependencies = {
            "torch": {
                "available": True,
                "version": torch.__version__,
                "cuda_available": torch.cuda.is_available(),
            },
            "model_file": {"exists": model_file_exists, "path": MODEL_PATH},
        }

        # Determine overall health status
        overall_status = "healthy" if model_loaded and model_file_exists else "degraded"

        # If critical components are missing, return 503
        if not model_file_exists:
            raise HTTPException(status_code=503, detail="Model file not found")

        if not model_loaded:
            raise HTTPException(
                status_code=503, detail="Model failed to load or perform inference"
            )

        return HealthResponse(
            status=overall_status,
            timestamp=datetime.now(timezone.utc).isoformat(),
            version=__version__,
            model_loaded=model_loaded,
            model_path=MODEL_PATH,
            device=str(torch.device("cuda" if torch.cuda.is_available() else "cpu")),
            dependencies=dependencies,
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error and return 503 for any unexpected errors
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@app.get("/health/ready")
def readiness_check():
    """
    Readiness probe endpoint for Kubernetes/container orchestration.
    This endpoint checks if the service is ready to receive traffic.
    """
    try:
        # Check if model file exists and model is loaded
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(status_code=503, detail="Model file not found")

        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")

        # Test model inference
        dummy_input = torch.randn(1, 3, 128, 128)
        with torch.no_grad():
            _ = model(dummy_input)

        return {"status": "ready"}

    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service not ready: {str(e)}")


@app.get("/health/live")
def liveness_check():
    """
    Liveness probe endpoint for Kubernetes/container orchestration.
    This endpoint checks if the service is alive and responding.
    """
    return {"status": "alive"}


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Predict the card type from the uploaded image.
    """

    # Check file is an image

    image_bytes = await file.read()
    prediction, probability = get_prediction(image_bytes)

    return {
        "filename": file.filename,
        "prediction": prediction,
        "probability": probability,
    }
