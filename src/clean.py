import pandas as pd
from pathlib import Path
import os

def clean_data():
    # RACINE DU PROJET (Projet Ydays Nasa)
    base_path = Path(__file__).parent.parent
    
    # CHEMINS VERS LES DONNÉES
    # Il faut entrer dans le dossier 'data' puis 'raw'
    raw_file = base_path / "raw" / "neo_2025_raw_filtered.csv"
    processed_dir = base_path / "processed"
    output_file = processed_dir / "neo_2025_clean.csv"

    # Vérification
    if not raw_file.exists():
        print(f"❌ Erreur : Fichier introuvable à l'adresse : {raw_file.absolute()}")
        print("Vérifiez que le fichier est bien dans /data/raw/")
        return

    print("--- Début du nettoyage ---")
    df = pd.read_csv(raw_file)

    # Transformations
    df["diametre_moyen_km"] = (df["diametre_min_km"] + df["diametre_max_km"]) / 2
    df["distance_lunaire"] = df["distance_manquee_km"] / 384400
    df["est_dangereux"] = df["est_dangereux"].astype(bool)
    
    # Nettoyage des lignes vides
    df = df.dropna(subset=["diametre_moyen_km", "distance_manquee_km"])

    # Création du dossier processed s'il manque
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Sauvegarde
    df.to_csv(output_file, index=False)
    print(f"✅ Succès ! Fichier sauvegardé dans : {output_file.absolute()}")

if __name__ == "__main__":
    clean_data()