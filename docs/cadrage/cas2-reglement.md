# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)

Répondre aux questions des étudiants sur le règlement intérieur de l'école, en citant l'article qui fonde la réponse.
## Utilisateur final (obligatoire)

L'étudiant qui cherche une règle (absences, retards, examens), et l'administration qui reçoit moins de questions répétitives.
## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)

(b) La réponse doit être vérifiable : le système cite l'article du règlement dont elle provient. (a) Il n'existe aucun jeu de questions étiquetées, ce qui exclut le machine learning classique. (c) Le volume de questions est faible, donc le coût par requête reste acceptable.
## Données nécessaires et leur origine (obligatoire)

Le texte officiel du règlement intérieur, fourni par l'administration de l'école. Une trentaine de questions réelles d'étudiants, collectées pour tester les réponses.
## Métrique de succès et seuil d'acceptation (obligatoire)
Au moins 90 % de réponses correctes avec la bonne source citée, mesuré sur 30 questions relues par l'administration.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une mauvaise réponse peut conduire un étudiant à ignorer une règle et à être sanctionné. Chaque réponse affiche l'article cité, et l'administration reste la référence en cas de doute.

## Risques éthiques ou de confidentialité (obligatoire)
Les questions des étudiants peuvent contenir des données personnelles (situation, notes) : ne pas les conserver ni les envoyer à un service externe sans accord.

## Approche écartée et pourquoi (facultatif)

Génératif seul : écarté car il pourrait inventer une règle inexistante sans source vérifiable.