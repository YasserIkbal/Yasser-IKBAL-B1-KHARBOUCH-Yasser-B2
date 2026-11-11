"""Interface Streamlit du service de sentiment, cliente de l'API HTTP."""
from __future__ import annotations

import pandas as pd
import streamlit as st

try:
    from ui.client import APIClientError, analyser_avis
except ModuleNotFoundError:  # Streamlit exécute parfois le script depuis ui/
    from client import APIClientError, analyser_avis  # noqa: E402

st.set_page_config(page_title="Analyse de sentiment", page_icon="💬", layout="wide")
st.title("Analyse de sentiment des avis clients")
st.caption("Interface cliente de l'API · le modèle reste côté serveur")


def afficher_resultat(resultat: dict[str, object]) -> None:
    label = str(resultat["label"])
    score = float(resultat["score"])
    if label == "INDETERMINE":
        st.warning("Je ne sais pas : à faire vérifier par un humain")
    elif label == "NEGATIVE":
        st.error("Avis négatif : à traiter en priorité")
    else:
        st.success("Avis positif")
    colonne_verdict, colonne_score = st.columns([2, 1])
    with colonne_verdict:
        st.write(f"Verdict API : `{label}`")
    with colonne_score:
        st.metric("Confiance", f"{score:.0%}")
    st.progress(score)


onglet_avis, onglet_lot, onglet_aide = st.tabs(["Un avis", "Un fichier CSV", "Comment ça marche"])

with onglet_avis:
    texte = st.text_area("Avis à analyser", "Livraison rapide, produit conforme.", height=130)
    if st.button("Analyser", type="primary"):
        try:
            afficher_resultat(analyser_avis(texte))
        except APIClientError as erreur:
            st.error(str(erreur))

with onglet_lot:
    st.write("Fichier CSV contenant une colonne `review`. Exemple : `data/avis_exemple.csv`.")
    fichier = st.file_uploader("Choisir un fichier", type="csv")
    if fichier is not None:
        try:
            source = pd.read_csv(fichier)
            if "review" not in source.columns:
                raise ValueError("colonne 'review' absente du fichier")
            lignes = []
            for avis in source["review"].fillna("").astype(str):
                if avis.strip():
                    resultat = analyser_avis(avis)
                    lignes.append({
                        "review": avis,
                        "prediction": resultat["label"],
                        "confiance": round(float(resultat["score"]), 3),
                    })
            if not lignes:
                raise ValueError("aucun avis exploitable dans le fichier")
            resultat_lot = pd.DataFrame(lignes)
            resultat_lot["verdict"] = resultat_lot["prediction"].map(
                {"INDETERMINE": "à vérifier", "POSITIVE": "positive", "NEGATIVE": "negative"}
            )
        except (APIClientError, ValueError, pd.errors.ParserError) as erreur:
            st.error(str(erreur))
        else:
            negatifs = int((resultat_lot["prediction"] == "NEGATIVE").sum())
            a_verifier = int((resultat_lot["prediction"] == "INDETERMINE").sum())
            c1, c2, c3 = st.columns(3)
            c1.metric("Avis analysés", len(resultat_lot))
            c2.metric("Négatifs détectés", negatifs)
            c3.metric("À vérifier", a_verifier)
            st.dataframe(resultat_lot, use_container_width=True)
            st.download_button(
                "Télécharger les résultats",
                resultat_lot.to_csv(index=False).encode("utf-8"),
                "resultats.csv",
                "text/csv",
            )

with onglet_aide:
    st.markdown(
        """
        L'interface n'importe pas le modèle. Elle envoie les avis à l'API avec `POST /predict`.

        Une confiance faible produit « Je ne sais pas : à faire vérifier par un humain ».
        Les erreurs de saisie, l'indisponibilité du modèle et l'API injoignable sont affichées
        comme des messages destinés à l'utilisateur.
        """
    )
