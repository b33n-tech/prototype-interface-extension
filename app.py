import streamlit as st
import pandas as pd
import json
import uuid
from datetime import datetime

JSON_FILE = "datas-historiques.json"

def load_scenarios():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        # Colonnes définies si fichier absent
        cols = ["id", "secteur", "objectif", "public", "format", "ton", "modeleJeu",
                "langue", "client", "facture", "dateSession", "participants"]
        return pd.DataFrame(columns=cols)

def save_scenario(scenario):
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    data.append(scenario)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

st.title("Générateur de scénarios")

# Charge les scénarios existants
scenarios_df = load_scenarios()

with st.form("form_scenario"):
    secteur = st.selectbox("Secteur", ["BTP", "Transport", "Santé"])
    objectif = st.text_input("Objectif de prévention", "Risque de chute")
    public = st.text_input("Public ciblé (laisser vide si non discriminant)", "")
    format_jeu = st.selectbox("Format", ["jeu narratif interactif", "quizz", "vidéo animée"])
    ton = st.selectbox("Ton", ["réaliste", "humoristique", "dramatique"])
    modele_jeu = st.radio("Modèle de jeu", ["Arbre décisionnel classique", "Modèle itératif/adaptatif"])
    langue = st.selectbox("Langue", ["FR", "EN"])

    st.write("---")
    st.write("Infos archivage (optionnel)")
    client = st.text_input("Client")
    facture = st.text_input("N° facture")
    date_session = st.date_input("Date de la session", datetime.today())
    participants = st.number_input("Nombre participants", min_value=1, value=5)

    submit = st.form_submit_button("Générer et enregistrer")

if submit:
    new_scenario = {
        "id": str(uuid.uuid4())[:8],
        "secteur": secteur,
        "objectif": objectif,
        "public": public,
        "format": format_jeu,
        "ton": ton,
        "modeleJeu": modele_jeu,
        "langue": langue,
        "client": client,
        "facture": facture,
        "dateSession": date_session.strftime("%Y-%m-%d"),
        "participants": participants
    }
    save_scenario(new_scenario)
    st.success("Scénario enregistré !")
    # Recharger pour affichage actualisé
    scenarios_df = load_scenarios()

st.markdown("---")
st.write(f"### Scénarios réalisés dans le secteur : {secteur}")

filtered_sector = scenarios_df[scenarios_df["secteur"] == secteur]

if not filtered_sector.empty:
    filtered_display = filtered_sector.rename(columns=lambda x: x.capitalize())
    st.dataframe(filtered_display)
else:
    st.info(f"Aucun scénario enregistré dans le secteur {secteur}.")
