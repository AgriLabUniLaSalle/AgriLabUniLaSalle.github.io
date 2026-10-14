# Entrainement d'une intelligence artificielle

Le modèle utilisé est Yolo en version 8. C’est un modèle créé et développé par l’entreprise Ultralytics. Il permet de faire de la reconnaissance d’objet et de la segmentation d’images. Pour que le modèle fonctionne, il lui faut une base de données sur laquelle s’entrainer appelée dataset. Yolo s’utilise sur un raspberry pi 5 avec de préférence un AI hat+ de l’organisation Raspberry Pi en association avec la société Hailo (le hat augmente la puissance de calcul de la carte et permet de décharger la puce de la carte principale, ce qui rend l’exploitation du modèle réclamant plus de ressources de manière plus fluide). Le système d'exploitation à utiliser est de préférence un système basé sur Debian et adapté aux raspberry pi tels que Raspberry Pi OS, Ubuntu Desktop, Pop OS (de l'entreprise System 76)

Le logiciel permettant d’entrainer le modèle est Google Colab qui permet d’executer du code python sur une sorte de bureau virtuel ("Lien de téléchargement du modèle de bureau virtuel utilisable pour entrainer l'IA":https://agrilab.unilasalle.fr/projets/attachments/download/6437/Notebook_d_entrainement_pour_yolov8.ipynb)) avec des ressources limités allouées mais suffisante pour cette utilisation (2 cœurs CPU, 16 go de RAM et 16 go de mémoire vidéo, cette dernière étant indispensable). Ces ressources étant utilisables pour tout le monde, la priorité est fixée sur les comptes ayant un abonnement payant sur le service.

L’entrainement du modèle peut donc s’avérer compliqué pendant les heures de pointe, sachant que la formule de base est gratuite, l'utilisation des ressources plus importantes sont réservées aux comptes ayant un abonnement payant.
Sur le logiciel, un tutoriel est proposé au lien suivant ("Lien du tutoriel":https://www.youtube.com/watch?v=SILmGmR6S_8)) un ensemble de lignes de code python à exécuter à adapter selon le dataset et la localisation des fichiers sur la machine hôte.

Le ou les datasets utilisés proviennent du site internet Roboflow ("Roboflow":https://universe.roboflow.com/)) qui en propose gratuitement et légalement pour faire du computer vision. Ce site permet aussi de créer ses propres datasets et de recadrer et faire du détourage avec les outils proposés tels que la sélection de l'objet pour le classer par catégories ( [Création d'un dataset via Roboflow](creation-d-un-dataset-via-roboflow.md) ) .

Les différentes étapes sont à effectuer dans l’ordre de présentation de la page :

1 :
```python
import os
HOME = os.getcwd()
print(HOME)
```

2 :
```python
!pip install ultralytics

from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()
```

3 :
```python
from ultralytics import YOLO

from IPython.display import display, Image
```

4 (cette partie du code est à modifier en fonction du dataset) :
```python
!mkdir {HOME}/datasets
%cd {HOME}/datasets

!pip install roboflow --quiet
from roboflow import Roboflow
rf = Roboflow(api_key="partie cachée sur roboflow")
project = rf.workspace("rgy").project("weed-nyehp")
version = project.version(5)
dataset = version.download("yolov8")
```

C'est à cette étape que le dataset s'installe et est décompressé.

5 :
```python
!yolo task=detect mode=train model=yolo11s.pt data=/content/weed-5/data.yaml epochs=70 imgsz=410 plots=True
```

La partie "model=" correspond au modèle d'IA qui va être utilisé, ici ce sera le modèle yolo v8n (modèle d'ancienne version présentant plus de documentation disponible).

Le "data=" correspond à la localisation du fichier .yaml dans l'archive du dataset. Il est nécessaire de le changer avant de lancer l'entrainement car cela dépend de sa localisation dans les fichiers du bureau virtuel.

Le mot "epochs" indique le nombre d'entrainements que va faire le modèle pour détecter ce que l'on veut. Plus le modèle fait d'entrainements le dataset a d'images, plus il sera fiable.

Le "imgsz" correspond à la taille en pixels des images du dataset. Il est nécessaire d'indiquer l'information de la page Roboflow.

Ensuite, pour  la procédure d'entrainement, il est recommandé de connecter son ordinateur à internet de façon stable (par câble) afin d'éviter les déconnections et les erreurs du bureau virtuel.

Le fichier qui sera généré en .pt peut être ré-entrainé et est directement utilisable pour la détéction via un programme python sur le Raspberry Pi.

---

[← Retour au sommaire](../README.md)
