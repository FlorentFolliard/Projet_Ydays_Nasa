import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# --- CHARGEMENT ---
base_path = Path(__file__).parent.parent
file_path = base_path / "raw" / "neo_orbites.csv"

if not file_path.exists():
    print(f"❌ Fichier introuvable : {file_path}")
else:
    df = pd.read_csv(file_path)
    
    # # Configuration du style
    # sns.set_theme(style="whitegrid")
    # plt.figure(figsize=(12, 8))

    # # --- LE SCATTER PLOT OPTIMISÉ ---
    # plot = sns.scatterplot(
    #     data=df,
    #     x="distance_lunaire",
    #     y="diametre_moyen_km",
    #     hue="est_dangereux",
    #     palette={True: "#e74c3c", False: "#3498db"}, # Rouge pour danger, Bleu pour calme
    #     alpha=0.5,           # Transparence pour voir les points superposés
    #     edgecolor=None,      # Supprime le contour des points pour moins de bruit visuel
    #     s=60                 # Taille des points
    # )

    # # --- TECHNIQUE 1 : Échelle Logarithmique sur l'axe Y ---
    # # Très utile car les diamètres varient de quelques mètres à plusieurs kilomètres
    # plt.yscale('log') 

    # # --- TECHNIQUE 2 : Limitation des axes (Zoom) ---
    # # On se concentre sur les objets "proches" (ex: 0 à 100 distances lunaires)
    # # car au-delà, ils sont rarement dangereux.
    # plt.xlim(0, 100) 

    # # --- HABILLAGE ---
    # plt.title("Identification des astéroïdes dangereux (Échelle Logarithmique)", fontsize=15)
    # plt.xlabel("Distance à la Terre (en Distances Lunaires)", fontsize=12)
    # plt.ylabel("Diamètre moyen (km) - Échelle Log", fontsize=12)
    
    # # Ajout d'une ligne horizontale pour marquer le seuil théorique de danger (140m = 0.14km)
    # plt.axhline(y=0.14, color='gray', linestyle='--', alpha=0.5, label="Seuil 140m")

    # plt.legend(title="Potentiellement dangereux")
    
    # plt.tight_layout()
    # plt.show()
 