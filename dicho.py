import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Simulation TVI & Dichotomie",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Simulation du TVI : Méthode de Dichotomie")
st.markdown("""
Cette application permet de **visualiser le Théorème des Valeurs Intermédiaires (TVI)** et le fonctionnement de l'algorithme de **dichotomie** pour resserrer l'encadrement d'une solution $f(x) = k$.
""")

# --- BARRE LATÉRALE (Paramètres) ---
st.sidebar.header("⚙️ Paramètres de la fonction")

# Choix de la fonction
choix_fonction = st.sidebar.selectbox(
    "Choisir une fonction f(x) :",
    [
        "x³ - 3x - 1",
        "e^(x) - 3x",
        "x² - 2",
        "15x * e^(-0.5x) - 5"  # Lien avec l'exercice Médicament !
    ]
)

# Définition mathématique selon le choix
if choix_fonction == "x³ - 3x - 1":
    f = lambda x: x**3 - 3*x - 1
    a_def, b_def, k_def = 1.5, 3.0, 0.0
elif choix_fonction == "e^(x) - 3x":
    f = lambda x: np.exp(x) - 3*x
    a_def, b_def, k_def = 1.0, 2.5, 0.0
elif choix_fonction == "x² - 2":
    f = lambda x: x**2 - 2
    a_def, b_def, k_def = 1.0, 2.0, 0.0
else:
    f = lambda x: 15*x*np.exp(-0.5*x) - 5
    a_def, b_def, k_def = 2.0, 12.0, 0.0

# Réglage de l'intervalle et de k
a_in = st.sidebar.number_input("Borne a", value=a_def, step=0.5)
b_in = st.sidebar.number_input("Borne b", value=b_def, step=0.5)
k_val = st.sidebar.number_input("Valeur cible k", value=k_def, step=0.5)
max_iter = st.sidebar.slider("Nombre maximum d'étapes", min_value=1, max_value=15, value=8)

# --- ALGORITHME DE DICHOTOMIE ---
historique = []
a, b = a_in, b_in

for step in range(max_iter + 1):
    m = (a + b) / 2
    historique.append((a, b, m, f(a), f(b), f(m)))
    if (f(a) - k_val) * (f(m) - k_val) <= 0:
        b = m
    else:
        a = m

# --- CURSEUR D'ÉTAPE INTERACTIF ---
st.subheader("🔍 Exploration étape par étape")
etape = st.slider("Avancer dans l'algorithme (Étape) :", 0, max_iter, 0)

a_c, b_c, m_c, fa_c, fb_c, fm_c = historique[etape]

# --- AFFICHAGE GRAPHIQUE ---
col1, col2 = st.columns([2, 1])

with col1:
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # Courbe globale
    margin = abs(b_in - a_in) * 0.2 if b_in != a_in else 1.0
    x_vals = np.linspace(a_in - margin, b_in + margin, 500)
    ax.plot(x_vals, f(x_vals), label="f(x)", color="#2b5c8f", linewidth=2.5)
    ax.axhline(k_val, color="#d9534f", linestyle="--", label=f"y = {k_val}")
    
    # Intervalle courant (Bande pastel)
    ax.axvspan(a_c, b_c, color='#77DD77', alpha=0.35, label=f"Intervalle [{a_c:.4f} ; {b_c:.4f}]")
    ax.plot(m_c, f(m_c), 'ro', markersize=8, label=f"Milieu m = {m_c:.4f}")
    
    ax.set_title(f"Étape {etape} — Amplitude : {b_c - a_c:.5f}", fontsize=13, color="#2b5c8f")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")
    
    st.pyplot(fig)

with col2:
    st.markdown("### 📊 État à l'étape " + str(etape))
    st.metric("Borne a", f"{a_c:.5f}", delta=None)
    st.metric("Borne b", f"{b_c:.5f}", delta=None)
    st.metric("Milieu m", f"{m_c:.5f}", delta=None)
    st.metric("Amplitude (b - a)", f"{b_c - a_c:.5f}")

    # Condition du TVI
    # Évaluation de la condition pour préparer le texte
    if (fa_c - k_val) * (fm_c - k_val) <= 0:
        produit_texte = "négatif"
        intervalle_texte = f"[{a_c:.4f} ; {m_c:.4f}]"
    else:
        produit_texte = "positif"
        intervalle_texte = f"[{m_c:.4f} ; {b_c:.4f}]"

    # Affichage corrigé
    st.info(f"""
    **Vérification du signe :**
    * $f(a) - k = {fa_c - k_val:.3f}$
    * $f(m) - k = {fm_c - k_val:.3f}$
    
    Le produit est **{produit_texte}**, la solution est donc dans l'intervalle **{intervalle_texte}**.
    """)
