#!/usr/bin/env python
"""Trace et sauvegarde la matrice de confusion du modele de sentiment.

Usage :
  python src/plot_confusion.py                 # jeu de demonstration
  python src/plot_confusion.py --allocine      # jeu Allocine
  python src/plot_confusion.py --normaliser    # valeurs en pourcentage

Produit : docs/images/matrice-confusion.png
"""
import argparse
import sys
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")          # pas d affichage interactif, compatible CI
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

# -- Importer les constantes et la fonction charger depuis train.py ----------
sys.path.insert(0, str(Path(__file__).resolve().parent))
from train import GRAINE, MODELE, charger

RACINE    = Path(__file__).resolve().parents[1]
SORTIE    = RACINE / "docs" / "images" / "matrice-confusion.png"
ETIQUETTES = ["negative", "positive"]


def tracer(mc: np.ndarray, etiquettes, titre: str, normalise: bool) -> None:
    """Dessine la matrice, l axe x = prediction, l axe y = verite."""
    if normalise:
        data   = mc.astype(float) / mc.sum(axis=1, keepdims=True)
        fmt    = ".2f"
        vmax   = 1.0
        label_cb = "Proportion"
    else:
        data   = mc
        fmt    = "d"
        vmax   = mc.max()
        label_cb = "Nombre d avis"

    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(data, interpolation="nearest", cmap="Blues", vmin=0, vmax=vmax)
    fig.colorbar(im, ax=ax, label=label_cb)

    ax.set(
        xticks=range(len(etiquettes)),
        yticks=range(len(etiquettes)),
        xticklabels=etiquettes,
        yticklabels=etiquettes,
        xlabel="Prediction",
        ylabel="Verite",
        title=titre,
    )
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    thresh = data.max() / 2.0
    for i in range(len(etiquettes)):
        for j in range(len(etiquettes)):
            val = f"{data[i, j]:{fmt}}"
            ax.text(j, i, val, ha="center", va="center",
                    color="white" if data[i, j] > thresh else "black")

    fig.tight_layout()
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(SORTIE, dpi=150)
    plt.close(fig)
    print(f"Figure sauvegardee : {SORTIE.relative_to(RACINE)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allocine",   action="store_true", help="utiliser le jeu Allocine")
    parser.add_argument("--normaliser", action="store_true", help="afficher les proportions")
    args = parser.parse_args()

    if not MODELE.exists():
        raise SystemExit("models/sentiment.joblib absent : lancez d abord python src/train.py")
    pipeline = joblib.load(MODELE)

    df, source = charger(args.allocine)
    _, X_test, _, y_test = train_test_split(
        df["review"], df["label"],
        test_size=0.2, random_state=GRAINE, stratify=df["label"]
    )
    y_pred = pipeline.predict(X_test)

    mc     = confusion_matrix(y_test, y_pred, labels=ETIQUETTES)
    n_test = len(y_test)
    n_err  = int((y_test.values != y_pred).sum())

    from sklearn.metrics import f1_score
    f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

    print(f"Jeu : {source}  |  {n_test} avis de test  |  {n_err} erreurs  |  F1 macro = {f1:.3f}")
    print()
    print("Matrice de confusion (lignes = verite, colonnes = prediction)")
    header = f"{'':>12}" + "".join(f"{e:>12}" for e in ETIQUETTES)
    print(header)
    for nom, ligne in zip(ETIQUETTES, mc, strict=True):
        print(f"{nom:>12}" + "".join(f"{v:>12}" for v in ligne))
    print()

    titre_norm = " (normalisee)" if args.normaliser else ""
    titre = f"Matrice de confusion — {source}{titre_norm}"
    tracer(mc, ETIQUETTES, titre, args.normaliser)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
