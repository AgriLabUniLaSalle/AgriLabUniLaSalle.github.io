# Code python et logiciel

Le choix a été fait de faire fonctionner l'intelligence artificielle sans le module hat accélérateur d'IA afin de vérifier le bon fonctionnement des lasers. L'utilisation du module supplémentaire nécessite une conversion du fichier .pt en fichier optimisé. La conversion d'un fichier .pt en fichier .hef qui est optimisé pour l'utilisation du hat  étant nécessaire un tutoriel a été suivi (https://wiki.seeedstudio.com/tutorial_of_ai_kit_with_raspberrypi5_about_yolov8n_object_detection/). Celui-ci a posé problème car n'étant pas à jour et optimisé car il utilise python 3.8 sortie en 2019 et maintenu jusqu'en 2024. Cette version n'est plus installable facilement car elle n'est plus disponible sur les dépôts de fichiers officiels de python.

Si l'on a pas installé les versions des paquets et logiciels utilisés le tutoriel, plusieurs erreurs peuvent se déclencher une par une suite aux incompatibilités ce qui a fait perdre du temps. Le Raspberry Pi fonctionnera donc seul.

Pour obtenir un code adapté, l'intelligence artificielle Perplexity avec la requête suivante :
Comment faire de la reconnaissance d'image avec un fichier .pt et yolov8 sur un Raspberry Pi 5 tout en ayant 2 zones distinctes qui vont déclencher chacune un laser via le gpio.

```python
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
```

Le code présenté ci-dessus n'est pas fonctionnel car il ne présente aucun affichage.

Grâce à Microsoft Visual Studio Code via l'extension Github Copilot (intelligence artificielle spécialisée dans le codage proposée par Github), plusieurs fonctionnalités ont été rajoutés telles qu'un affichage à l'écran qui s'adapte à la résolution de l'écran qui affiche l'image de la caméra, l'ajout de "logs" pour savoir si un élément du code ou un composant qui n'est pas détecté, la gestion des lasers et des coordonnées des objets détecté pour l'allumage des lasers, un cadre qui s'affiche autour de chaque plante détéctée.

Voici un code fonctionnel qui demande quelques corrections :
```python
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
```

Les broches GPIO utilisées sont les 17 et 27 (en configuration BCM (Broadcom, la marque du processeur situé sur le Raspberry Pi), la seconde étant la board avec la numérotation physique des broches).
Pour connaitre la configuration de son matériel, il faut utiliser la commande "pinout" sur le terminal du Raspberry Pi. Pour aussi voir a quoi sert chaque broche le site internet https://pinout.xyz/ peut être utile pour les carte possédant 40 broches tels que les Raspberry Pi 1, 2, 3, 4 et 5 avec leurs déclinaisons A, B et compute module.

Les broches 17 et 27 sont des broches qui permettent d'envoyer un signal simple, ici une impulsion pour piloter l'allumage des lasers.
Les lasers sont alimentés via le H-Bridge pour éviter d'utiliser les sorties 5v de l'ordinateur et de pouvoir ajouter plus de lasers (avec H-Bridge) si besoin.

Code actuel et définitif :

Fichier pré-entrainé : ("Fichier .pt":https://agrilab.unilasalle.fr/projets/attachments/download/6417/yolov8n1500.pt). Celui-ci est créé à partir du dataset : https://app.roboflow.com/test-dwijd/dandelion-8fytt/browse . Celui-ci présente un nombre de 46 images dont une partie de capture d'écran issues de la vidéo de présentation du projet ainsi que des images proposées en open source sur d'autres dataset présentant des pissenlits (plante reconnue). L'entrainement du modèle présenté a pu bénéficier de 1500 epochs (séquences d'entrainement) car le nombre d'image n'est pas très élevé.

```python
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
```

Avec ce code, le Raspberry Pi est capable de détecter des plantes, aussi la couleur jaune car la résolution de l'écran est basse. Une des limitations présentées est la puissance du Raspberry Pi qui créé de la latence dans la détection et donc un retard des lasers.

---

[← Retour au sommaire](../README.md)
