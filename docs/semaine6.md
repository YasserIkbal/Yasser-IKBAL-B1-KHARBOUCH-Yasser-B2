# TP6 — Packaging de l'application

## Réponse 1 — que contient la roue ?

La roue contient le code réutilisable de l'application : `sentiment_app`, `api` et
`ui`, ainsi que la commande `sentiment`. Elle ne contient ni les tests, ni les jeux
de données, ni le modèle `sentiment.joblib`. Le modèle est un artefact séparé,
réentraînable indépendamment du code.

## Réponse 2 — pourquoi `SENTIMENT_MODELE` ?

Une roue installée ne peut pas deviner l'emplacement du modèle propre à chaque
machine. `SENTIMENT_MODELE` fournit donc un chemin explicite vers le fichier
`.joblib`. Cette séparation permet de publier le code sans publier un artefact
lourd ou potentiellement sensible.

## Réponse 3 — pourquoi garder `src/predict.py` ?

Les anciens scripts et tests du TP2 importent encore `predict` depuis `src`.
Le fichier conservé dans `src` est donc une façade de compatibilité qui réexporte
la nouvelle implémentation de `sentiment_app.predict`. Le code principal de l'API
importe désormais directement le paquet installable.

## Vérification

```text
python -m build --wheel
python -m venv .venv-wheel
.venv-wheel\Scripts\pip install dist\sentiment_app-0.6.0-py3-none-any.whl
$env:SENTIMENT_MODELE = (Resolve-Path models\sentiment.joblib).Path
sentiment --version
sentiment predict "Livraison rapide, très satisfait"
```

