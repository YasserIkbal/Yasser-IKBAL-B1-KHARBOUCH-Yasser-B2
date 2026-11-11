# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Signaler au pharmacien toute ordonnance à laquelle il manque un champ obligatoire (patient, prescripteur, posologie, date).

## Utilisateur final (obligatoire)
Le pharmacien d'officine, qui contrôle l'ordonnance au comptoir avant la délivrance.

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
(a) Aucune ordonnance étiquetée n'existe au départ. (b) Le pharmacien doit pouvoir expliquer le refus au patient, et chaque règle est lisible. (d) Une ordonnance validée à tort a une conséquence grave pour la santé du patient.

## Données nécessaires et leur origine (obligatoire)

La liste des champs obligatoires d'une ordonnance, fournie par la réglementation et par le pharmacien responsable. Les ordonnances réelles scannées ou saisies à l'officine, utilisées seulement pour tester les règles.
## Métrique de succès et seuil d'acceptation (obligatoire)
Rappel d'au moins 0,95 sur les ordonnances incomplètes, mesuré sur un jeu de 200 ordonnances relues par un pharmacien.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une ordonnance incomplète validée à tort peut mener à une mauvaise délivrance. Le pharmacien valide toujours avant la délivrance : l'outil signale, il ne décide pas.

## Risques éthiques ou de confidentialité (obligatoire)
Les ordonnances sont des données de santé personnelles : accès restreint, aucune copie hors de l'officine, et anonymisation des exemples utilisés pour les tests.

## Approche écartée et pourquoi (facultatif)
Machine learning : écarté faute d'ordonnances étiquetées. Possible plus tard, à condition de constituer un jeu étiqueté et de garder la validation du pharmacien.
