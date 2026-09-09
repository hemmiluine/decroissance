import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# Données physiques initiales
N0 = 1000
demi_vies = {'Carbone 14': 5730, 'Uranium 238': 4.468e9}
isotope_actuel = 'Carbone 14'

def calculer_N(t, t12):
    lam = np.log(2) / t12
    return N0 * np.exp(-lam * t)

# Configuration de la fenêtre graphique
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3, left=0.25)

t_max = demi_vies[isotope_actuel] * 4
t = np.linspace(0, t_max, 500)

# Tracé de la courbe et du point de mesure interactif
courbe, = ax.plot(t, calculer_N(t, demi_vies[isotope_actuel]), 'b-', lw=2)
point_mesure, = ax.plot(0, N0, 'ro', markersize=8)

ax.set_title("Mesure interactive du temps de demi-vie")
ax.set_xlabel("Temps (années)")
ax.set_ylabel("Nombre de noyaux $N(t)$")
ax.grid(True)

# Création des éléments d'interface
ax_radio = plt.axes([0.02, 0.5, 0.18, 0.15])
radio = RadioButtons(ax_radio, ('Carbone 14', 'Uranium 238'))

ax_slider = plt.axes([0.25, 0.15, 0.65, 0.03])
slider_temps = Slider(ax_slider, 'Curseur temporel', 0, t_max, valinit=0)

# Fonctions de mise à jour
def update_isotope(label):
    global isotope_actuel
    isotope_actuel = label
    t_max_new = demi_vies[label] * 4
    t_new = np.linspace(0, t_max_new, 500)
    
    courbe.set_xdata(t_new)
    courbe.set_ydata(calculer_N(t_new, demi_vies[label]))
    ax.set_xlim(0, t_max_new)
    
    slider_temps.valmax = t_max_new
    slider_temps.ax.set_xlim(0, t_max_new)
    slider_temps.set_val(0)
    fig.canvas.draw_idle()

def update_curseur(val):
    t_actuel = slider_temps.val
    n_actuel = calculer_N(t_actuel, demi_vies[isotope_actuel])
    point_mesure.set_xdata([t_actuel])
    point_mesure.set_ydata([n_actuel])
    fig.canvas.draw_idle()

radio.on_clicked(update_isotope)
slider_temps.on_changed(update_curseur)

plt.show()
