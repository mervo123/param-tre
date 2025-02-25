import pandas as pd
import numpy as np

def calculate_azimuth(lat1, lon1, lat2, lon2):
    """
    Calcule l'azimut entre un point d'émission (lat1, lon1)
    et un point de réception (lat2, lon2).
    """
    # Conversion des degrés en radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Différence de longitude
    delta_lon = lon2 - lon1

    # Formule de l'azimut
    x = np.sin(delta_lon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(delta_lon)
    azimuth = np.arctan2(x, y)
    
    # Conversion en degrés et normalisation entre 0° et 360°
    azimuth = np.degrees(azimuth)
    azimuth = (azimuth + 360) % 360

    return azimuth

# --- EXEMPLE AVEC PLUSIEURS POINTS ---

# Coordonnées de l'antenne émettrice (Exemple : une station TNT)
lat_emetteur = 6.352268  # Latitude de l'antenne (Exemple : Cotonou)
lon_emetteur = 2.402957  # Longitude de l'antenne

# Charger les points de réception depuis un fichier CSV
# Format attendu : "latitude,longitude" dans chaque ligne du fichier
xlsx_file = "C:/Users/pc/Documents/TIFF/database(csv)/merged_data.xlsx"  # Nom du fichier CSV contenant les points de réception
df = pd.read_excel(xlsx_file)  # Charger les coordonnées des points de réception

# Calculer l'azimut pour chaque point
df["Azimut"] = df.apply(lambda row: calculate_azimuth(lat_emetteur, lon_emetteur, row["Lat"], row["Long"]), axis=1)

# Afficher les résultats
print(df)

# Sauvegarde des résultats avec azimut dans un nouveau fichier CSV
df.to_excel("C:/Users/pc/Documents/TIFF/database(csv)/merged_data_azimut.xlsx", index=False)
