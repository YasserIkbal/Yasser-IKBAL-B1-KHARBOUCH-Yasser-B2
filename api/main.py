from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from api.model import SentimentClassifier, verifier_classes
from api.schemas import PredictRequest, PredictResponse
from src.predict import charger_modele


@asynccontextmanager
async def lifespan(app: FastAPI):
    modele = charger_modele()
    verifier_classes(modele)
    app.state.model = SentimentClassifier(modele)
    yield
    app.state.model = None

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    if not hasattr(app.state, "model") or app.state.model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    return {"status": "ok", "model": "sentiment.joblib (TP2)"}

@app.post("/predict", response_model=PredictResponse)
def predict_sentiment(request: PredictRequest):
    if not hasattr(app.state, "model") or app.state.model is None:
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    try:
        result = app.state.model.predict(request.text)
        return PredictResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Erreur interne du modèle") from exc
