# coding: utf-8
# Code complet pour Raspberry Pi 5 - YOLOv8 + Contrôle Laser

import cv2
import numpy as np
import gpiozero
from gpiozero import OutputDevice
from ultralytics import YOLO
from matplotlib.path import Path
from time import sleep

# Configuration GPIO
LASER_PIN_Z1 = 17  # Broche GPIO pour la zone 1
LASER_PIN_Z2 = 18  # Broche GPIO pour la zone 2

# Initialisation des sorties lasers
laser_z1 = OutputDevice(LASER_PIN_Z1, active_high=False, initial_value=False)
laser_z2 = OutputDevice(LASER_PIN_Z2, active_high=False, initial_value=False)

# Définition des zones de détection (coordonnées normalisées)
ZONE_1 = np.array([[0.2, 0.2], [0.5, 0.2], [0.5, 0.5], [0.2, 0.5]])  # Zone gauche
ZONE_2 = np.array([[0.5, 0.5], [0.8, 0.5], [0.8, 0.8], [0.5, 0.8]])  # Zone droite

def convert_to_relative(bbox, img_width, img_height):
    """Convertit les coordonnées absolues en relatives"""
    x_center = (bbox[0] + bbox[2]) / (2 * img_width)
    y_center = (bbox[1] + bbox[3]) / (2 * img_height)
    return (x_center, y_center)

def setup_zones(img_width, img_height):
    """Adapte les zones à la résolution réelle de l'image"""
    return {
        'zone1': ZONE_1 * np.array([img_width, img_height]),
        'zone2': ZONE_2 * np.array([img_width, img_height])
    }

def main():
    # Chargement du modèle YOLOv8
    model = YOLO('best.pt')  # Remplacez par votre modèle .pt
    
    # Initialisation de la caméra
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            img_height, img_width = frame.shape[:2]
            zones = setup_zones(img_width, img_height)
            
            # Détection YOLOv8
            results = model(frame, imgsz=320, verbose=False)
            
            # Réinitialisation des états des lasers
            laser_z1.off()
            laser_z2.off()

            # Traitement des détections
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                for box in boxes:
                    x1, y1, x2, y2 = box
                    center = convert_to_relative((x1, y1, x2, y2), img_width, img_height)
                    
                    # Vérification appartenance zone
                    in_zone1 = Path(zones['zone1']).contains_point((center[0]*img_width, center[1]*img_height))
                    in_zone2 = Path(zones['zone2']).contains_point((center[0]*img_width, center[1]*img_height))
                    
                    # Contrôle des lasers
                    if in_zone1:
                        laser_z1.on()
                    if in_zone2:
                        laser_z2.on()

            # Visualisation (optionnel)
            cv2.polylines(frame, [zones['zone1'].astype(int)], True, (0,255,0), 2)
            cv2.polylines(frame, [zones['zone2'].astype(int)], True, (0,0,255), 2)
            cv2.imshow('YOLOv8 Detection', frame)
            
            if cv2.waitKey(1) == ord('q'):
                break

    except KeyboardInterrupt:
        print("Arrêt propre...")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        laser_z1.close()
        laser_z2.close()

if __name__ == '__main__':
    main()
