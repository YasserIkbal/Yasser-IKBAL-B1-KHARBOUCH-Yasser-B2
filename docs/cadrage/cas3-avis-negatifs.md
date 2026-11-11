# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Faire remonter en tête de file les avis clients négatifs, pour que l'équipe relation client réponde d'abord aux clients mécontents.
## Utilisateur final (obligatoire)

L'agent de la relation client, qui traite des milliers d'avis par jour et doit voir les plus urgents en premier.
## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [x] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
(a) Les étiquettes sont disponibles presque gratuitement grâce à la note laissée par le client. (c) Avec des milliers d'avis par jour, il faut un coût par requête très faible, ce que permet un petit modèle. (d) Un avis mal classé a une conséquence limitée : il est traité plus tard, sans danger pour le client.
## Données nécessaires et leur origine (obligatoire)
Des avis clients en français, avec leur note, fournis par l'entreprise. La note sert d'étiquette : avis négatif en dessous de 3 sur 5, positif au-dessus.

## Métrique de succès et seuil d'acceptation (obligatoire)

Rappel d'au moins 0,90 sur la classe négative, mesuré sur un jeu de test de 1 000 avis non utilisés à l'entraînement.
## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Un avis négatif manqué est traité avec retard, et un avis positif classé négatif fait perdre un peu de temps à l'agent. L'agent garde la main : l'outil trie la file, il ne répond pas au client.

## Risques éthiques ou de confidentialité (obligatoire)
Les avis peuvent contenir des noms ou des coordonnées de clients : les anonymiser avant l'entraînement. La note n'est pas toujours cohérente avec le texte, donc un échantillon est relu à la main.

## Approche écartée et pourquoi (facultatif)

Génératif seul : écarté car trop coûteux pour des milliers d'avis par jour, et moins vérifiable qu'un classifieur mesuré.