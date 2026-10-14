# Seuil d incertitude et interface — Semaine 3

## Seuil retenu : 0.60

Nous retenons le seuil par defaut de **0.60** (60 % de confiance). En dessous de ce seuil,
l interface affiche « A verifier par un agent » plutot que de trancher.

## Nombres d avis sous chaque seuil (sur 290 avis de demo_reviews.csv)

| Seuil | Avis sous le seuil | Pourcentage du fichier |
|------:|-------------------:|-----------------------:|
|  0.50 |                  0 |                   0.0 % |
|  0.60 |                 69 |                  23.8 % |
|  0.75 |                137 |                  47.2 % |

## Justification du choix

Avec un seuil a 0.60, **69 avis sur 290 (23,8 %)** sont envoyes vers un agent humain.
Ce compromis est raisonnable : le modele prend en charge 76 % des avis de facon autonome
et concentre l effort humain sur le quart le plus ambigu, la ou le risque d erreur est
le plus eleve. Un seuil a 0.50 ne renvoie aucun avis vers l agent, ce qui est trop
confiant ; un seuil a 0.75 enverrait pres de la moitie des avis, ce qui annulerait
l interet du modele.

Le seuil d incertitude est avant tout une **decision metier**, pas un reglage purement
technique : c est l equipe relation client qui arbitre entre le cout d un avis mal classe
automatiquement et le cout d un agent qui traite un avis que le modele aurait pu gerer.
Le choix de 0.60 peut etre revu a la hausse si les agents signalent trop d erreurs,
ou a la baisse si la charge de relecture devient insupportable.
