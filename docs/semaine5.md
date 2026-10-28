# Semaine 5 : interface Streamlit

## 1. Pourquoi l'interface ne charge-t-elle plus le modèle ?

L'interface appelle uniquement `POST /predict` via [ui/client.py](../ui/client.py).
Le fichier `.joblib` et `predict()` restent côté serveur. Un changement de modèle
ne demande donc pas de modifier Streamlit.

## 2. Que voit l'utilisateur quand le modèle s'abstient ?

La réponse `INDETERMINE` devient « Je ne sais pas : à faire vérifier par un humain ».
La confiance et le verdict API restent visibles dans le résultat.

## 3. Comment les erreurs sont-elles traitées ?

Une erreur `422` devient un message de saisie invalide, une erreur `503` un message
de service momentanément indisponible et une API arrêtée un message « API injoignable ».
Les détails internes du serveur ne sont pas affichés.
