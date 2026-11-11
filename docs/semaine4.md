# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.

## 1. Couverture

- Avant (étape A) : état TP3 non couvert par les tests d'intégration ; les branches
  « modèle absent », « modèle non chargé » et « panne » n'étaient pas exécutées.
- Après (étape D) : 98,51 % (67 lignes, 1 ligne manquante, soit 99 % arrondi).
  La ligne manquante est la protection du modèle sans attribut `classes` dans
  `verifier_classes`; le modèle réel fournit `classes_`. Aucune ligne n'est exclue
  par `pragma: no cover`.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| Les espaces seuls étaient acceptés comme texte | `test_tout_texte_blanc_est_refuse` | `field_validator` avec `strip()` dans `PredictRequest` |
| Une panne `ValueError` devenait 422 | `test_panne_du_modele_repond_500` | toute exception du modèle devient 500 générique |
| `/health` répondait OK sans modèle | `test_modele_non_charge_repond_503` | vérification de `app.state.model` |
| Les classes du modèle n'étaient pas contrôlées | `test_classes_inattendues_refusent_le_demarrage` | correspondance explicite des deux classes autorisées |

## 3. Seuil d'abstention

- Courbe : seuil 0,50 → 100 % répondus, exactitude 0,879 ; 0,60 → 72 %,
  exactitude 0,952 ; 0,70 → 64 %, exactitude 1,000.
- Seuil retenu : 0,60 ; 16 avis sur 58 sont envoyés à un humain (28 %).
  Il évite 5 erreurs par rapport à 0,50, tout en conservant 42 réponses.

## 4. Jeu d'or

- Bilan : 6 justes, 12 abstentions, 3 erreurs franches déclarées, sur 21 avis.
- Le modèle est prudent sur les formulations hors vocabulaire et les négations :
  l'abstention évite de présenter une confiance artificielle, mais réduit le taux
  de réponses automatiques.

## 5. Outils statiques

- Remarques au départ : Ruff signalait 18 problèmes et Mypy ne pouvait pas analyser
  correctement `api` (paquet sans `__init__.py`). Après correction : Ruff 0 remarque,
  Mypy 0 erreur.
- Aucun des défauts fonctionnels de la partie 2 n'était détecté par ces outils : les
  tests restent nécessaires pour les comportements HTTP et les limites métier.
