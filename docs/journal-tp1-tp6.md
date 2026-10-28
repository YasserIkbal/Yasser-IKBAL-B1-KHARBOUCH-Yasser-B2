# Journal de bord du binôme : TP1 à TP6

**Module** : Développement et déploiement d'applications intelligentes  
**Binôme** : Yasser IKBAL et Yasser KHARBOUCH  
**Dépôt** : https://github.com/YasserIkbal/Yasser-IKBAL-B1-KHARBOUCH-Yasser-B2.git  
**Date de vérification** : 28/10/2026

## État global

| TP | Contrôles | État | Justification |
|---|---|---|---|
| TP1 | T0–T7 | Réalisé | structure, cadrage, environnement et historique Git présents |
| TP2 | C1–C5 | Réalisé | entraînement, métriques et analyse du modèle présentes |
| TP3 | T14–T20 | Réalisé | API FastAPI, CI d'entraînement et tests API présents |
| TP4 | T21–T27 | Réalisé | limites, Hypothesis, abstention, intégration et qualité statique |
| TP5 | T28–T34 | Réalisé | client HTTP, Streamlit, tests et compte rendu présents |
| TP6 | T35–T41 | Non réalisé | aucun paquet Python, roue ou commande `sentiment` n'est présent |

Les résultats ci-dessous proviennent du projet et des exécutions vérifiées. Les
fichiers `.venv/`, les caches et `models/sentiment.joblib` restent ignorés par Git.

## Préparation et TP1

Le projet contient les dossiers `api`, `data`, `docs`, `models`, `scripts`,
`src`, `tests` et `ui`, ainsi que les fiches de cadrage dans `docs/cadrage/`.

Le cas retenu est la priorisation des avis négatifs pour le service client.
L'approche choisie est TF-IDF + régression logistique : elle est rapide, peu
coûteuse et adaptée à un grand nombre d'avis étiquetés. Les règles manuelles et
un modèle génératif seul ont été écartés.

Les contrôles d'environnement et de cadrage sont automatisés dans
`tests/test_environment.py` et `tests/test_cadrage.py`. Le dépôt GitHub utilisé
est celui du binôme indiqué en en-tête.

![TP1 : structure du projet et cadrage](captures/tp1-structure-cadrage.png)

## TP2 — Entraîner et évaluer le modèle

`src/make_demo.py` produit 290 avis, répartis en 145 positifs et 145 négatifs.
Le pipeline utilise TF-IDF avec unigrammes/bigrammes et une régression logistique.
Le vocabulaire contient 316 termes.

Résultats du jeu de test de 58 avis :

```text
F1 macro : 0.879
Exactitude : 0.8793
Rappel négatif : 0.931
```

Matrice de confusion :

| vérité / prédiction | negative | positive |
|---|---:|---:|
| negative | 27 | 2 |
| positive | 5 | 24 |

Les sept erreurs concernent principalement des avis mitigés. Le modèle TF-IDF
compte les mots, mais ne comprend pas toujours qu'une seconde partie de phrase
annule la première.

`models/metrics.json` est versionné car il est léger et contrôle le F1. Le modèle
`.joblib`, lourd et reconstructible, n'est pas versionné.

![TP2 : entraînement et matrice de confusion](captures/tp2-entrainement-matrice.png)

## TP3 — Exposer le modèle par une API

L'API est répartie entre `api/schemas.py`, `api/model.py` et `api/main.py`.
Le modèle est chargé une seule fois au démarrage dans le `lifespan`.

Contrôles vérifiés :

```text
GET /health                         200
POST /predict avis positif          200, POSITIVE
POST /predict avis négatif          200, NEGATIVE
POST /predict texte vide            422
POST /predict champ absent          422
POST /predict mauvais type          422
```

Le fichier `tests/test_api.py` contient les tests dédiés du TP3 : **7 passed**.
Sans `models/sentiment.joblib`, le démarrage lève `FileNotFoundError` et refuse
de lancer l'application. La CI exécute `make_demo.py` puis `train.py` avant les tests.

![TP3 : API, prédictions et erreurs 422](captures/tp3-api-predictions.png)

## TP4 — Tests approfondis et qualité

Le schéma refuse aussi les textes composés uniquement d'espaces. Les propriétés
Hypothesis vérifient les textes valides et invalides sur des générations aléatoires.

Le seuil d'abstention choisi est `0.60` :

| Seuil | Part répondue | Exactitude des réponses |
|---:|---:|---:|
| 0.50 | 100 % | 0.879 |
| 0.60 | 72 % | 0.952 |
| 0.70 | 64 % | 1.000 |

Sous le seuil, l'API renvoie `INDETERMINE` avec le score. Les tests couvrent le
démarrage réel, le modèle absent, le modèle non chargé, les pannes du modèle et
les classes inattendues.

Résultats de qualité :

```text
Couverture API : 98.51 %
Ruff : All checks passed!
Mypy : Success: no issues found in 4 source files
```

Une panne interne répond `500`, tandis qu'une requête invalide répond `422`.

![TP4 : tests, couverture, Ruff et Mypy](captures/tp4-qualite.png)

## TP5 — Interface Streamlit

`ui/app.py` ne charge plus le modèle local. Il utilise `ui/client.py` pour appeler
`POST /predict`, ce qui sépare clairement l'interface du modèle.

Le client traduit les erreurs `422`, `503`, `500` et l'API injoignable. Le verdict
`INDETERMINE` devient : **« Je ne sais pas : à faire vérifier par un humain »**.

L'interface permet d'analyser un avis, de charger `data/avis_exemple.csv`,
d'afficher un tableau et de télécharger `resultats.csv`.

Résultats vérifiés :

```text
Tests TP5 ciblés : 12 passed
Suite complète avant l'ajout des tests API TP3 : 89 passed, 3 xfailed
```

![TP5 : interface Streamlit, abstention et analyse CSV](captures/tp5-interface-csv.png)

## TP6 — Packaging

Le TP6 n'est pas encore réalisé. Il reste à :

- créer le paquet `sentiment_app` ;
- ajouter la version `0.6.0` et la commande `sentiment` ;
- construire une roue avec `python -m build` ;
- tester l'installation hors du dépôt ;
- créer et pousser le tag `v0.6.0`.

Les contrôles T35 à T41 sont donc **non réalisés**, afin de ne pas inventer de
résultats.

## Difficultés et solutions

| Difficulté | Cause | Solution |
|---|---|---|
| `ui/app.py` introuvable | commande lancée depuis le dossier parent | se placer dans le sous-dossier du projet |
| `No module named api` | Uvicorn lancé hors de la racine du projet | lancer Uvicorn dans le dossier contenant `api/` |
| modèle absent | modèle exclu de Git | exécuter `python src/make_demo.py` puis `python src/train.py` |
| API injoignable depuis Streamlit | serveur non démarré | lancer Uvicorn dans un terminal séparé |

## Répartition du travail

| Membre | Contribution |
|---|---|
| Yasser IKBAL | dépôt GitHub, entraînement, métriques, API et qualité |
| Yasser KHARBOUCH | cadrage, évaluation, interface et documentation |

## Bilan

Les TP1 à TP5 sont intégrés et vérifiés dans le dépôt. Le système possède un
modèle entraîné, une API HTTP, un mécanisme d'abstention et une interface
Streamlit découplée du modèle. Le prochain objectif est le TP6 : rendre le
projet installable comme paquet Python et vérifier la roue hors du dépôt.
