# Analyse des erreurs du modèle — Semaine 2

## Matrice de confusion (jeu de démonstration, 58 avis)

|              | prédit negative | prédit positive |
|--------------|----------------:|----------------:|
| **vrai negative** |          27 |               2 |
| **vrai positive** |           5 |              24 |

F1 macro : **0.879** — Exactitude : **0.8793** — Rappel négatif : **0.931**

## Types d'erreurs observés

Sur 58 avis de test, le modèle commet **7 erreurs** : 2 avis négatifs classés positifs (faux positifs), et 5 avis positifs classés négatifs (faux négatifs). Les erreurs proviennent toutes d'avis mitigés dont la première moitié contredit la conclusion : par exemple *« Taille trop petite et retour payant au déballage, sauf que ensuite produit conforme à la description »* est étiqueté positif (la conclusion l'emporte) mais le modèle sac de mots compte les mots négatifs du début, ce qui l'induit en erreur.

## Mécanisme d'erreur et piste d'amélioration

Le vectoriseur TF-IDF traite chaque mot indépendamment et ignore l'ordre des phrases : il ne sait pas que la deuxième partie d'un avis mitigé annule la première. Pour corriger cela il faudrait utiliser des bigrammes de phrases ou un modèle de langue pré-entraîné sur le français (CamemBERT, par exemple) capable de comprendre la structure argumentative ; augmenter le jeu d'entraînement avec davantage d'avis mixtes correctement étiquetés aiderait également ; enfin, placer sous révision humaine tous les avis dont la confiance est inférieure à 60 % permettrait de limiter l'impact des cas ambigus en production.
