import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Décroissance Radioactive", layout="wide")
st.title("Mesure interactive du temps de demi-vie")

# Données physiques initiales
N0 = 1000
demi_vies = {'Carbone 14': 5730, 'Uranium 238': 4.468e9}

# Interface latérale Streamlit pour les réglages
st.sidebar.header("Paramètres de simulation")
isotope_actuel = st.sidebar.radio("Choix de l'isotope", ('Carbone 14', 'Uranium 238'))

t_max = demi_vies[isotope_actuel] * 4
t_actuel = st.sidebar.slider(
    "Curseur temporel (années)", 
    min_value=0.0, 
    max_value=float(t_max), 
    value=0.0, 
    step=float(t_max)/500
)

# Modèle mathématique
def calculer_N(t, t12):
    lam = np.log(2) / t12
    return N0 * np.exp(-lam * t)

# Création de la figure
fig, ax = plt.subplots(figsize=(10, 6))
t = np.linspace(0, t_max, 500)

# Tracé de la loi de décroissance
ax.plot(t, calculer_N(t, demi_vies[isotope_actuel]), 'b-', lw=2, label=f"Population de {isotope_actuel}")

# Tracé du point de mesure interactif
n_actuel = calculer_N(t_actuel, demi_vies[isotope_actuel])
ax.plot(t_actuel, n_actuel, 'ro', markersize=8, label=f"Mesure : N = {n_actuel:.0f}")

# Formatage rigoureux du graphique
ax.set_xlabel("Temps $t$ (années)")
ax.set_ylabel("Nombre de noyaux $N(t)$")
ax.grid(True)
ax.legend()

# Affichage de la figure sur l'application web
st.pyplot(fig)
