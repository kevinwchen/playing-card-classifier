from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from model.model import get_prediction, __version__

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


@app.get("/")
def home():
    return {
        "model": "pytorch_playing_cards_model",
        "version": __version__,
    }


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):

    # Check file is an image

    image_bytes = await file.read()
    prediction, probability = get_prediction(image_bytes)

    return {
        "filename": file.filename,
        "prediction": prediction,
        "probability": probability,
    }
