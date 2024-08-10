from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from model.model import get_prediction, __version__

app = FastAPI()


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
    prediction = get_prediction(image_bytes)

    return {
        "filename": file.filename,
        "prediction": prediction,
    }
