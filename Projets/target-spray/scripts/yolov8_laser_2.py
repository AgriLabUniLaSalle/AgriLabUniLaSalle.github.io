# coding: utf-8
# Code complet pour Raspberry Pi 5 - YOLOv8 + Contrôle Laser avec picamera2

import cv2
import numpy as np
import gpiozero
from gpiozero import OutputDevice
from ultralytics import YOLO
from matplotlib.path import Path
from picamera2 import Picamera2, Preview
import logging
from time import sleep

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration GPIO
LASER_PIN_Z1 = 17  # Broche GPIO pour la zone 1
LASER_PIN_Z2 = 27  # Broche GPIO pour la zone 2

# Initialisation des sorties lasers
try:
    laser_z1 = OutputDevice(LASER_PIN_Z1, active_high=False, initial_value=False)
    laser_z2 = OutputDevice(LASER_PIN_Z2, active_high=False, initial_value=False)
except gpiozero.exc.PinError as e:
    logging.error(f"Erreur d'initialisation GPIO: {e}")
    exit(1)  # Arrêt immédiat car les lasers sont essentiels

# Définition des zones de détection (coordonnées normalisées)
ZONE_1 = np.array([[0.2, 0.2], [0.5, 0.2], [0.5, 0.5], [0.2, 0.5]])  # Zone gauche
ZONE_2 = np.array([[0.5, 0.5], [0.8, 0.5], [0.8, 0.8], [0.5, 0.8]])  # Zone droite
ZONE_POINTS = {
    'zone1': ZONE_1,
    'zone2': ZONE_2,
}

def convert_to_relative(bbox, img_width, img_height):
    """Convertit les coordonnées absolues en relatives."""
    x_center = (bbox[0] + bbox[2]) / (2 * img_width)
    y_center = (bbox[1] + bbox[3]) / (2 * img_height)
    return (x_center, y_center)

def setup_zones(img_width, img_height):
    """Adapte les zones à la résolution réelle de l'image."""
    zones = {}
    for zone_name, zone_points in ZONE_POINTS.items():
        zones[zone_name] = zone_points * np.array([img_width, img_height])
    return zones

def check_if_inside(point, zone_points):
    """Vérifie si un point est à l'intérieur d'une zone polygonale."""
    path = Path(zone_points)
    return path.contains_point(point)

def main():
    """Fonction principale pour exécuter la détection d'objets et le contrôle laser."""
    logging.info("Chargement du modèle YOLOv8...")
    try:
        model = YOLO('best.pt')  # Remplacez par votre modèle .pt (lien du fichier)
    except Exception as e:
        logging.error(f"Erreur lors du chargement du modèle YOLOv8: {e}")
        return

    logging.info("Initialisation de la caméra avec picamera2...")
    try:
        picam2 = Picamera2()
        config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
        picam2.configure(config)
        picam2.start()
    except Exception as e:
        logging.error(f"Erreur lors de l'initialisation de la caméra : {e}")
        return

    try:
        while True:
            # Capture d'une image avec picamera2
            frame = picam2.capture_array()
            img_height, img_width = frame.shape[:2]
            zones = setup_zones(img_width, img_height)

            # Détection YOLOv8
            try:
                results = model(frame, imgsz=320, verbose=False)
            except Exception as e:
                logging.error(f"Erreur lors de la détection YOLOv8: {e}")
                continue

            # Réinitialisation des états des lasers
            laser_z1.off()
            laser_z2.off()

            # Traitement des détections
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                for box in boxes:
                    x1, y1, x2, y2 = box
                    center = convert_to_relative((x1, y1, x2, y2), img_width, img_height)
                    center_pixel = (center[0] * img_width, center[1] * img_height)

                    # Vérification appartenance zone
                    in_zone1 = check_if_inside(center_pixel, zones['zone1'])
                    in_zone2 = check_if_inside(center_pixel, zones['zone2'])

                    # Contrôle des lasers
                    if in_zone1:
                        logging.info("Objet détecté dans la zone 1. Activation du laser Z1.")
                        laser_z1.on()
                    if in_zone2:
                        logging.info("Objet détecté dans la zone 2. Activation du laser Z2.")
                        laser_z2.on()

            # Visualisation (optionnel)
            cv2.polylines(frame, [zones['zone1'].astype(int)], True, (0, 255, 0), 2)
            cv2.polylines(frame, [zones['zone2'].astype(int)], True, (0, 0, 255), 2)
            cv2.imshow('YOLOv8 Detection', frame)

            if cv2.waitKey(1) == ord('q'):
                logging.info("Arrêt demandé par l'utilisateur.")
                break

    except KeyboardInterrupt:
        logging.info("Arrêt propre via interruption clavier.")
    finally:
        logging.info("Libération des ressources...")
        picam2.stop()
        cv2.destroyAllWindows()
        laser_z1.close()
        laser_z2.close()

if __name__ == '__main__':
    main()
