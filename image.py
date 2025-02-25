import requests
import os
from io import BytesIO
from PIL import Image  # Pillow remplace PIL ici
from geopy.distance import geodesic
import numpy as np

# Configuration de l'API Google Maps
API_KEY = "API_KEY_WORD"
BASE_URL = "https://maps.googleapis.com/maps/api/staticmap"

# Dossier de stockage des images
IMAGE_DIR = "C:/Users/pc/Documents/TIFF/P1COTO"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Coordonnées des deux points (émetteur et récepteur)
emitter = {"lat": 6.4302, "lon": 2.3471}  # Exemple
receiver = {"lat": 6.37272, "lon": 2.34774}  # Exemple

def get_google_maps_image(lat, lon, filename, zoom=19, size=(640, 640)):
    params = {
        "center": f"{lat},{lon}",
        "zoom": zoom,
        "size": f"{size[0]}x{size[1]}",
        "maptype": "satellite",  # Vue satellite
        "key": API_KEY
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Lève une exception pour les erreurs HTTP
        img = Image.open(BytesIO(response.content))  # Ouvrir l'image avec Pillow
        img = img.convert("RGB")  # Assurer la compatibilité
        img_path = os.path.join(IMAGE_DIR, filename)
        img.save(img_path)  # Sauvegarde de l'image sans compression supplémentaire
        return img_path
    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête pour {filename}: {e}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de l'image {filename}: {e}")
    return None

# Génération des images tout au long du trajet
def capture_path_images(start, end, step_distance=100, vertical_offset=107):
    lat1, lon1 = start["lat"], start["lon"]
    lat2, lon2 = end["lat"], end["lon"]
    
    total_distance = geodesic((lat1, lon1), (lat2, lon2)).meters
    num_steps = int(total_distance // step_distance)  # Nombre d'étapes sans chevauchement
    
    lats = np.linspace(lat1, lat2, num_steps + 1)
    lons = np.linspace(lon1, lon2, num_steps + 1)
    
    image_paths = []
    for i, (lat, lon) in enumerate(zip(lats, lons)):
        # Image principale sur le trajet
        filename_main = f"image_{i}.jpg"
        image_path = get_google_maps_image(lat, lon, filename_main)
        if image_path:
            image_paths.append(image_path)
            print(f"Image enregistrée : {image_path}")
        
        # Images au-dessus et en dessous
        filename_top = f"image_{i}_top.jpg"
        filename_bottom = f"image_{i}_bottom.jpg"
        
        # Calcul des nouveaux points avec l'offset vertical
        lat_top = lat + (vertical_offset / 111320)  # Conversion de mètres en degrés
        lat_bottom = lat - (vertical_offset / 111320)
        
        # Récupérer les images supplémentaires
        image_path_top = get_google_maps_image(lat_top, lon, filename_top)
        image_path_bottom = get_google_maps_image(lat_bottom, lon, filename_bottom)
        
        if image_path_top:
            image_paths.append(image_path_top)
            print(f"Image enregistrée : {image_path_top}")
        if image_path_bottom:
            image_paths.append(image_path_bottom)
            print(f"Image enregistrée : {image_path_bottom}")

    return image_paths

# Capture des images entre l'émetteur et le récepteur
image_paths = capture_path_images(emitter, receiver)
