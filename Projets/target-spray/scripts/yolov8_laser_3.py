# coding: utf-8
# Code complet pour Raspberry Pi 5 - YOLOv8 + Contrôle Laser avec picamera2 + cadre autour des plantes

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

# Initialisation des sorties lasers avec active_high=True pour H-bridge
try:
    laser_z1 = OutputDevice(LASER_PIN_Z1, active_high=True, initial_value=False)
    laser_z2 = OutputDevice(LASER_PIN_Z2, active_high=True, initial_value=False)
except gpiozero.exc.PinError as e:
    logging.error(f"Erreur d'initialisation GPIO: {e}")
    exit(1)  # Arrêt immédiat car les lasers sont essentiels

def convert_to_relative(bbox, img_width, img_height):
    """Convertit les coordonnées absolues en relatives."""
    x_center = (bbox[0] + bbox[2]) / (2 * img_width)
    y_center = (bbox[1] + bbox[3]) / (2 * img_height)
    return (x_center, y_center)

def main():
    """Fonction principale pour exécuter la détection d'objets et le contrôle laser."""
    logging.info("Chargement du modèle YOLOv8...")
    try:
        model = YOLO('/home/agrilab/Downloads/yolov8n1500.pt')  # Remplacez par votre modèle .pt
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
            frame = picam2.capture_array()
            img_height, img_width = frame.shape[:2]

            object_in_zone1 = False
            object_in_zone2 = False

            # Détection YOLOv8
            try:
                results = model(frame, imgsz=320, verbose=False)
            except Exception as e:
                logging.error(f"Erreur lors de la détection YOLOv8: {e}")
                continue

            # Traitement des détections
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                for box in boxes:
                    x1, y1, x2, y2 = box
                    center = convert_to_relative((x1, y1, x2, y2), img_width, img_height)
                    center_pixel_x = center[0] * img_width  # Coordonnée X en pixels

                    if center_pixel_x < img_width / 2:
                        object_in_zone1 = True
                    elif center_pixel_x >= img_width / 2:
                        object_in_zone2 = True

            # Activation/désactivation immédiate des lasers selon la détection
            if object_in_zone1:
                laser_z1.on()
                logging.info("Laser Z1 allumé (détection en cours).")
            else:
                laser_z1.off()
            if object_in_zone2:
                laser_z2.on()
                logging.info("Laser Z2 allumé (détection en cours).")
            else:
                laser_z2.off()

            # Visualisation (optionnel)
            cv2.line(frame, (img_width // 2, 0), (img_width // 2, img_height), (255, 0, 0), 2)
            cv2.imshow('YOLOv8 Detection', frame)

            if cv2.waitKey(1) == ord('q'):
                logging.info("Arrêt demandé par l'utilisateur.")
                break

    except KeyboardInterrupt:
        logging.info("Arrêt propre via interruption clavier.")
    finally:
        logging.info("Libération des ressources...")
        laser_z1.off()
        laser_z2.off()
        laser_z1.close()
        laser_z2.close()
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
