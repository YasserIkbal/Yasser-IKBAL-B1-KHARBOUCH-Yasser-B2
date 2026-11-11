"""Tests dédiés au contrat de l'API du TP3."""
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
MODELE = RACINE / "models" / "sentiment.joblib"


@pytest.fixture(scope="module")
def client():
    if not MODELE.exists():
        pytest.skip("modèle non produit : python src/train.py")
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as test_client:
        yield test_client


def test_health_indique_que_le_service_est_pret(client):
    reponse = client.get("/health")

    assert reponse.status_code == 200
    assert reponse.json()["status"] == "ok"
    assert "sentiment.joblib" in reponse.json()["model"]


@pytest.mark.parametrize(
    ("texte", "etiquette"),
    [
        ("Service impeccable, livraison rapide, je recommande", "POSITIVE"),
        ("Produit cassé et service client injoignable", "NEGATIVE"),
    ],
)
def test_predict_classe_les_avis_evidents(client, texte, etiquette):
    reponse = client.post("/predict", json={"text": texte})

    assert reponse.status_code == 200
    assert reponse.json()["label"] == etiquette
    assert 0 <= reponse.json()["score"] <= 1


@pytest.mark.parametrize(
    "corps",
    [
        {"text": ""},
        {},
        {"text": 42},
    ],
    ids=["texte-vide", "champ-absent", "mauvais-type"],
)
def test_predict_refuse_les_requetes_invalides(client, corps):
    reponse = client.post("/predict", json=corps)

    assert reponse.status_code == 422
    assert isinstance(reponse.json()["detail"], list)


def test_api_refuse_de_demarrer_sans_modele(monkeypatch):
    from fastapi.testclient import TestClient

    import api.main as main
    import src.predict as predict_module

    monkeypatch.setattr(predict_module, "MODELE", Path("modele-tp3-inexistant.joblib"))
    main.charger_modele.cache_clear()
    try:
        with pytest.raises(FileNotFoundError), TestClient(main.app):
            pass
    finally:
        main.charger_modele.cache_clear()
