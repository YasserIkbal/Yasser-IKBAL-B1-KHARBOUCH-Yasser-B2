"""Calcule combien d avis tombent sous differents seuils de confiance.

Usage : python scripts/seuils.py
Necessite : data/demo_reviews.csv et models/sentiment.joblib
"""
import sys
from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "ui"))

from helpers import charger_predicteur, predire_lot  # noqa: E402  (chemin UI ajouté ci-dessus)

SEUILS = [0.50, 0.60, 0.75]


def main() -> int:
    csv = RACINE / "data" / "demo_reviews.csv"
    if not csv.exists():
        raise SystemExit("data/demo_reviews.csv absent : lancez python src/make_demo.py")
    df = pd.read_csv(csv)
    predicteur = charger_predicteur()
    resultats = predire_lot(df, predicteur)
    total = len(resultats)
    print(f"Fichier : {csv.name}  —  {total} avis analyses\n")
    print(f"{'Seuil':>8}  {'Sous le seuil':>14}  {'Pourcentage':>12}")
    print("-" * 40)
    for s in SEUILS:
        sous = int((resultats["confiance"] < s).sum())
        pct = round(100 * sous / total, 1)
        print(f"{s:>8.2f}  {sous:>14}  {pct:>11.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
