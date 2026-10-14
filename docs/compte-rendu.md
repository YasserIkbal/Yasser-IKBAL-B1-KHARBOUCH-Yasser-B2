# Compte rendu global des TP1 a TP3

**Binome :** Yasser IKBAL ([@YasserIkbal]) et Yasser KHARBOUCH ([@kharbouch-yasser])
**Depot :** https://github.com/YasserIkbal/Yasser-IKBAL-B1-KHARBOUCH-Yasser-B2.git
**Date :** 14/10/2026

---

## 1. Le besoin et son cadrage

Le projet consiste a prioriser automatiquement les avis clients negatifs pour une equipe
relation client qui traite des milliers d avis par jour. Nous avons retenu l approche
**machine learning** pour le cas 3 (priorisation des avis negatifs). Deux criteres
justifient ce choix : **(a) les etiquettes existent presque gratuitement** grace a la
note laissee par le client (note < 3/5 = negatif), et **(c) le cout par requete est
tres faible** avec un classifieur TF-IDF + regression logistique, ce qui est
indispensable pour un flux de milliers d avis par jour. Les approches ecartees sont le
generatif seul (trop couteux a grande echelle) et les regles metier (le sentiment ne
se reduit pas a une liste de mots).

## 2. L architecture du depot

| Dossier | Role |
|---------|------|
| src/ | Scripts d entrainement (train.py, make_demo.py), d evaluation (evaluate.py) et de prediction (predict.py) |
| ui/ | Interface Streamlit (app.py) et fonctions pures testables (helpers.py) |
| models/ | sentiment.joblib (non versionne, lourd) et metrics.json (versionne, leger) |
| data/ | demo_reviews.csv (genere, non versionne) et sample_reviews.csv (versionne) |
| tests/ | 45 tests couvrant cadrage, environnement, modele et interface |
| docs/ | Fiches de cadrage, analyses hebdomadaires, ce compte rendu |

models/metrics.json est versionne dans Git car c est un fichier texte leger (< 1 Ko)
qui permet a la CI de verifier que le F1 depasse le seuil sans avoir a recharger le
modele. models/sentiment.joblib n est pas versionne car il peut depasser 100 Mo et
changerait a chaque reentrainement, polluant l historique Git.

## 3. Le modele

Pipeline : TF-IDF avec bigrammes (ngram_range=(1,2), min_df=2, sublinear_tf=True)
suivi d une regression logistique (class_weight=balanced, max_iter=1000).
Decoupage 80/20 stratifie avec random_state=42.

| Jeu          | Avis  | Vocabulaire | F1 macro | Rappel negatif |
|--------------|------:|------------:|---------:|---------------:|
| Demo         |   290 |         316 |    0.879 |          0.931 |

Matrice de confusion sur le jeu de demonstration (58 avis de test) :

|                    | predit negative | predit positive |
|--------------------|----------------:|----------------:|
| **vrai negative**  |              27 |               2 |
| **vrai positive**  |               5 |              24 |

La ligne vrai negative : sur 29 avis reellement negatifs, 27 sont correctement
classes et 2 sont rates. La ligne vrai positive : sur 29 avis positifs, 5 sont
classes negatifs a tort et 24 sont corrects.

## 4. L analyse des erreurs

Sur 58 avis de test, 7 sont mal classes (2 faux positifs, 5 faux negatifs).
Tous les cas d erreur proviennent d avis mitiges dont la premiere partie contredit
la conclusion. Exemple reel observe : "Taille trop petite et retour payant au
deballage, sauf que ensuite produit conforme a la description" est etiquete positif
(la conclusion l emporte) mais le sac de mots compte les termes negatifs du debut
et vote negatif. Le mecanisme est clair : TF-IDF ignore l ordre des phrases et ne
voit pas qu une seconde proposition annule la premiere. Pour corriger cela il
faudrait un modele de langue pre-entraine sur le francais (CamemBERT) ou des
n-grammes de phrases, davantage d avis mixtes en entrainement, et une revue humaine
sous le seuil de confiance.

## 5. L interface et le seuil d incertitude

Nous retenons le seuil de 0.60 (60 % de confiance). Sur 290 avis du jeu de
demonstration, 69 avis (23,8 %) tombent sous ce seuil et sont envoyes vers un
agent avec le message "A verifier par un agent". Les 221 restants (76,2 %) sont
traites automatiquement par le modele.

Ce compromis est juste : un seuil a 0.50 n enverrait aucun avis vers l agent
(risque trop eleve d erreurs silencieuses) ; un seuil a 0.75 en enverrait 137 soit
47 %, ce qui rendrait le systeme inutile. Le seuil est un parametre metier autant
que technique : c est l equipe relation client qui arbitre entre le cout d une
erreur automatique et le cout d une relecture humaine.

## 6. Ce qui a echoue

Lors de la resolution du conflit entre la branche locale et origin/main, la commande
git rebase --abort n a pas abouti car le dossier .git/rebase-merge etait dans un
etat corrompu. Nous avons du supprimer manuellement ce dossier et reconstruire
l etat HEAD. Autre incident : requirements.txt contenait des marqueurs de conflit
Git (<<<<<<< HEAD) qui faisaient echouer le test test_requirements_pins_versions ;
nous avons resolu le conflit en conservant pyarrow==17.0.*. Enfin, les outils de
creation de fichiers de l IDE ecrivaient dans un repertoire virtuel sans persister
sur le disque physique, ce qui a necessite de copier les sources directement depuis
le kit de reference.

## 7. Ce que nous ferions autrement

Avec les moyens d une vraie equipe, nous entranerions le modele sur le jeu Allocine
complet (20 000 avis, F1 attendu ~0.92) plutot que sur 290 avis synthetiques. Nous
utiliserions CamemBERT pour mieux gerer les avis mitiges. Nous mettrions en place
un pipeline CI/CD qui reentrainerait le modele automatiquement des qu un lot d avis
corriges par les agents est disponible. Nous versionnerions les donnees avec DVC
pour garantir la reproductibilite complete.

## 8. Repartition du travail

| Membre            | Ce qu il a pris en charge |
|-------------------|---------------------------|
| Yasser IKBAL      | Creation du depot GitHub, mise en place du venv, redaction des fiches de cadrage cas1 et cas3, implementation de src/train.py et src/make_demo.py, redaction de docs/semaine2.md |
| Yasser KHARBOUCH  | Redaction de la fiche de cadrage cas2, implementation de src/evaluate.py et src/predict.py, creation de ui/helpers.py et ui/app.py, redaction de docs/semaine3.md et du compte rendu |

**Outils d aide a la redaction :** Assistant IA utilise pour structurer les commits
et generer les squelettes de code ; chaque sortie a ete verifiee en executant les
tests et en lisant les resultats chiffres directement dans le terminal.