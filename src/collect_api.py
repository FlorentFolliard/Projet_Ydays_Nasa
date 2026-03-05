import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import os
import time
from dotenv import load_dotenv

# --- CHARGEMENT DES VARIABLES D'ENVIRONNEMENT ---
# On charge le fichier .env qui doit se trouver à la racine du projet
load_dotenv(Path(__file__).parent.parent / ".env")

# --- CONFIGURATION ---
api_key = os.getenv("NASA_API_KEY")

# Vérification que la clé est bien présente
if not api_key:
    raise ValueError("Erreur : La variable NASA_API_KEY est introuvable. "
                     "Vérifiez votre fichier .env à la racine du projet.")

start_date = datetime(2025, 1, 1)
end_date = datetime.today()

all_objects = []
step = timedelta(days=7) # Limite API NASA
current_start = start_date

# --- COLLECTE DES DONNÉES ---
while current_start <= end_date:
    current_end = min(current_start + step, end_date)
    
    print(f"Récupération {current_start.strftime('%Y-%m-%d')} → {current_end.strftime('%Y-%m-%d')}")
    
    url = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        "start_date": current_start.strftime("%Y-%m-%d"),
        "end_date": current_end.strftime("%Y-%m-%d"),
        "api_key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "near_earth_objects" in data:
            for date in data["near_earth_objects"]:
                all_objects.extend(data["near_earth_objects"][date])
    except Exception as e:
        print(f"Erreur lors de la requête : {e}")
    
    time.sleep(0.2) # Petite pause pour respecter l'API
    current_start = current_end + timedelta(days=1)

print(f"Objets récupérés : {len(all_objects)}")

# --- TRAITEMENT ET NETTOYAGE (Pandas) ---

if all_objects:
    # 1. Normalisation à plat du JSON
    df = pd.json_normalize(all_objects)

    # 2. Fonction pour extraire les données imbriquées de 'close_approach_data'
    def extract_approach_info(x):
        if isinstance(x, list) and len(x) > 0:
            return pd.Series({
                'vitesse_km_h': float(x[0]['relative_velocity']['kilometers_per_hour']),
                'distance_manquee_km': float(x[0]['miss_distance']['kilometers'])
            })
        return pd.Series({'vitesse_km_h': None, 'distance_manquee_km': None})

    # On applique l'extraction et on fusionne avec le dataframe principal
    approach_details = df['close_approach_data'].apply(extract_approach_info)
    df = pd.concat([df, approach_details], axis=1)

    # 3. Sélection des colonnes pertinentes
    cols_mapping = {
        "id": "id",
        "name": "nom",
        "is_potentially_hazardous_asteroid": "est_dangereux",
        "estimated_diameter.kilometers.estimated_diameter_min": "diametre_min_km",
        "estimated_diameter.kilometers.estimated_diameter_max": "diametre_max_km",
        "vitesse_km_h": "vitesse_km_h",
        "distance_manquee_km": "distance_manquee_km"
    }

    df_final = df[list(cols_mapping.keys())].rename(columns=cols_mapping)
    df_final['est_dangereux'] = df_final['est_dangereux'].astype(bool)

    # --- SAUVEGARDE AVEC CHEMINS CORRIGÉS ---

    # base_path remonte à la racine du projet depuis 'src'
    base_path = Path(__file__).parent.parent
    
    # On cible le dossier /data/raw/
    output_dir = base_path / "data" / "raw"
    output_path = output_dir / "neo_2025_raw_filtered.csv"

    # Création du dossier /data/raw/ s'il n'existe pas
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sauvegarde
    df_final.to_csv(output_path, index=False)

    print(f"✅ Analyse terminée. Fichier sauvegardé dans : {output_path.absolute()}")
else:
    print("❌ Aucun objet récupéré, sauvegarde annulée.")