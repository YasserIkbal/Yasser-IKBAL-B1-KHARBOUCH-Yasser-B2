from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from api.schemas import PredictRequest, PredictResponse
from api.model import SentimentClassifier
from src.predict import charger_modele

@asynccontextmanager
async def lifespan(app: FastAPI):
    charger_modele()
    app.state.model = SentimentClassifier()
    yield
    app.state.model = None

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "model": "sentiment.joblib"}

@app.post("/predict", response_model=PredictResponse)
def predict_sentiment(request: PredictRequest):
    if not hasattr(app.state, "model") or app.state.model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    try:
        result = app.state.model.predict(request.text)
        return PredictResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
