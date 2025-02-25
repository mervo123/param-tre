import pandas as pd
import numpy as np
from geopy.distance import geodesic
import math

# Fonction pour calculer la distance en kilomètres
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

# Fonction pour calculer l'azimut (angle par rapport au nord)
def calculate_azimuth(lat1, lon1, lat2, lon2):
    delta_lon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    
    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    azimuth = math.degrees(math.atan2(x, y))
    return (azimuth + 360) % 360  # Normalisation entre 0 et 360°

# Fonction pour calculer le tilt (angle d'inclinaison)
def calculate_tilt(lat1, lon1, lat2, lon2):
    distance = calculate_distance(lat1, lon1, lat2, lon2) * 1000  # Convertir en mètres
    hauteur_recepteur = 1.5  # Hauteur moyenne du récepteur (exemple : 1.5m)
    hauteur_emetteur = 50  # Hauteur moyenne de l'émetteur (exemple : 50m)
    
    delta_h = hauteur_emetteur - hauteur_recepteur
    tilt = math.degrees(math.atan(delta_h / distance)) if distance > 0 else 0
    return tilt

# Charger le fichier Excel
def process_excel(file_path):
    df = pd.read_excel(file_path)
    
    # Vérifier si les colonnes nécessaires existent
    required_columns = ['Latitude', 'Longitude', 'Emetteur_Latitude', 'Emetteur_Longitude']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"La colonne '{col}' est absente du fichier Excel.")
    
    # Effectuer les calculs et renseigner les valeurs
    df['Distance_trajet'] = df.apply(lambda row: calculate_distance(row['Latitude'], row['Longitude'], row['Emetteur_Latitude'], row['Emetteur_Longitude']), axis=1)
    df['Azimut'] = df.apply(lambda row: calculate_azimuth(row['Latitude'], row['Longitude'], row['Emetteur_Latitude'], row['Emetteur_Longitude']), axis=1)
    df['Tilt'] = df.apply(lambda row: calculate_tilt(row['Latitude'], row['Longitude'], row['Emetteur_Latitude'], row['Emetteur_Longitude']), axis=1)
    
    # Sauvegarder le fichier mis à jour
    output_file = file_path.replace(".xlsx", "_updated.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Fichier mis à jour enregistré sous : {output_file}")

# Exemple d'utilisation
process_excel("C:/Users/pc/Documents/TIFF/récepteur.xlsx")
