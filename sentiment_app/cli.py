"""Commande principale du paquet sentiment-app."""

from __future__ import annotations

import argparse
import importlib.metadata
import subprocess
import sys
from pathlib import Path

from sentiment_app.predict import predict


def version() -> str:
    try:
        return importlib.metadata.version("sentiment-app")
    except importlib.metadata.PackageNotFoundError:
        return "0.6.0"


def construire_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sentiment", description="Analyse de sentiment")
    parser.add_argument("--version", action="version", version=f"%(prog)s {version()}")
    commandes = parser.add_subparsers(dest="commande", required=True)

    prediction = commandes.add_parser("predict", help="prédit le sentiment d'un avis")
    prediction.add_argument("texte", nargs="+", help="texte de l'avis")

    serveur = commandes.add_parser("serve", help="démarre l'API FastAPI")
    serveur.add_argument("--host", default="127.0.0.1")
    serveur.add_argument("--port", type=int, default=8000)

    interface = commandes.add_parser("ui", help="démarre l'interface Streamlit")
    interface.add_argument("--port", type=int, default=8501)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = construire_parser().parse_args(argv)
    if args.commande == "predict":
        resultat = predict(" ".join(args.texte))
        print(f"{resultat['label']} (confiance {resultat['score']:.0%})")
        return 0
    if args.commande == "serve":
        import uvicorn

        uvicorn.run("api.main:app", host=args.host, port=args.port)
        return 0
    script = Path(__file__).resolve().parents[1] / "ui" / "app.py"
    return subprocess.call(
        [sys.executable, "-m", "streamlit", "run", str(script), "--server.port", str(args.port)]
    )


if __name__ == "__main__":
    raise SystemExit(main())

