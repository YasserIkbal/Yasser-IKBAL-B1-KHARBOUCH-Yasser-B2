"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D). À COMPLÉTER.

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_le_demarrage(monkeypatch):
    from fastapi.testclient import TestClient

    import api.main as main
    from src import predict as predict_module

    monkeypatch.setattr(predict_module, "MODELE", Path("fichier-inexistant.joblib"))
    main.charger_modele.cache_clear()
    with pytest.raises(FileNotFoundError), TestClient(main.app):
        pass
    main.charger_modele.cache_clear()


def test_modele_non_charge_repond_503():
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        app.state.model = None
        assert client.get("/health").status_code == 503
        assert client.post("/predict", json={"text": "bonjour"}).status_code == 503


@pytest.mark.parametrize("exception", [RuntimeError("panne"), ValueError("bug interne")])
def test_panne_du_modele_repond_500(monkeypatch, exception):
    from fastapi.testclient import TestClient

    from api.main import app

    class ModeleEnPanne:
        def predict(self, text):
            raise exception

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "model", ModeleEnPanne())
        reponse = client.post("/predict", json={"text": "bonjour"})
    assert reponse.status_code == 500
    assert "bug interne" not in reponse.text


def test_classes_inattendues_refusent_le_demarrage(monkeypatch):
    from fastapi.testclient import TestClient

    import api.main as main

    class MauvaisModele:
        classes_ = ["positive", "neutral"]

    monkeypatch.setattr(main, "charger_modele", lambda: MauvaisModele())
    with pytest.raises(ValueError, match="classes de modèle inattendues"), TestClient(main.app):
        pass


# À écrire (étape D) :
# D.2 modèle absent : chemin du modèle redirigé (monkeypatch), cache vidé
#     (charger_modele.cache_clear()), l'API refuse de démarrer (FileNotFoundError) ;
# D.3 modèle non chargé : l'API démarrée, modèle retiré de app.state, 503 sur /health et /predict ;
# D.4 modèle en panne : predict lève RuntimeError, puis ValueError("bug interne") :
#     500 dans les deux cas, sans le message interne dans la réponse.
# Utilisez monkeypatch.setattr pour toute modification : il restaure l'état à la fin du test.
