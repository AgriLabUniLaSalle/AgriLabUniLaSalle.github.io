<!--
Projet Redmine : Tutoriels
Source : Question
ID source : 209
Section : Atelier de formations
Derniere modification : 2024-09-05 17:28:36
-->

# Atelier Découpe plasma

_Cette documentation a en partie été rédigé à l'aide de ChatGPT : vous trouverez ces parties en italic plus bas_
# Introduction
## Références 

Documentation Plasma Cutting Primer for LinuxCNC Users - http://linuxcnc.org/docs/html/plasma/plasma-cnc-primer.html
Documentation Plasma C LinuxCNC - http://linuxcnc.org/docs/html/plasma/plasmac-user-guide.html
Documentation QT Plasma C - https://linuxcnc.org/docs/devel/html/plasma/qtplasmac.html
Page poste de découpe plasma Hypertherm Powermax 45XP - https://agrilab.unilasalle.fr/projets/questions/38-decoupeuse-plasma-hypertherm-powermax-45-xp

*Paramètres de découpe dans le .pdf en bas de page.*
## Le plasma

_Le plasma est le quatrième état de la matière, c'est un gaz ionisé qui a été chauffé à une température extrêmement élevée et ionisé de sorte qu'il devient conducteur électriquement. Les processus de coupe et de gougeage à l'arc au plasma utilisent ce plasma pour transférer un arc électrique sur la pièce à travailler. Le métal à couper ou à enlever est fondu par la chaleur de l'arc, puis soufflé loin._

_L'objectif de la coupe à l'arc plasma est de séparer le matériau, tandis que le gougeage à l'arc plasma est utilisé pour enlever les métaux jusqu'à une profondeur et une largeur contrôlées._

_Les torches à plasma sont similaires en conception à la bougie d'allumage d'une voiture. Elles se composent de sections négatives et positives séparées par un isolant central. À l'intérieur de la torche, l'arc pilote démarre dans l'espace entre l'électrode chargée négativement et la pointe chargée positivement. Une fois que l'arc pilote a ionisé le gaz de plasma, la colonne de gaz surchauffé passe par l'orifice de petite taille à l'extrémité de la torche, qui est focalisé sur le métal à couper._

_Dans une torche de coupe au plasma, un gaz froid entre dans la Zone B, où un arc pilote entre l'électrode et la pointe de la torche chauffe et ionise le gaz. Ensuite, l'arc principal de coupe est transféré vers la pièce à travailler à travers la colonne de gaz de plasma dans la Zone C. En forçant le gaz de plasma et l'arc électrique à travers un petit orifice, la torche délivre une concentration élevée de chaleur sur une petite zone. L'arc plasma rigide et resserré est illustré dans la Zone C. Un courant continu (CC) de polarité droite est utilisé pour la coupe au plasma, comme montré dans l'illustration. La Zone A canalise un gaz secondaire qui refroidit la torche. Ce gaz aide également le gaz de plasma à haute vélocité à souffler le métal fondu hors de la coupe, permettant ainsi une coupe rapide et sans scories._

![primer_torch-head](assets/images/primer_torch-head.png)

_Les opérations de plasma sur les machines CNC sont assez uniques en comparaison avec le fraisage ou le tournage, et constituent un processus un peu particulier. Le chauffage inégal du matériau par l'arc plasma peut entraîner le pliage et le gauchissement de la pièce. La plupart des feuilles de métal ne sortent pas de l'usine ou de la presse dans un état très uniforme ou plat. Les feuilles épaisses (30 mm ou plus) peuvent présenter un écart de plan allant jusqu'à 50 mm à 100 mm. La plupart des autres opérations CNC basées sur le Gcode commenceront à partir d'une référence connue ou d'une pièce de matériau dont la taille et la forme sont connues, et le Gcode est écrit pour ébaucher l'excès de matière, puis enfin découper la pièce finie. Avec le plasma, l'état inconnu de la feuille rend impossible la génération d'un Gcode qui puisse prendre en compte ces variations du matériau._

_Un arc plasma a une forme ovale et la hauteur de coupe doit être contrôlée pour minimiser les bords biseautés. Si la torche est trop haute ou trop basse, les bords peuvent devenir excessivement biseautés. Il est également essentiel que la torche soit maintenue perpendiculaire à la surface._

_En résumé, les opérations de plasma sur les machines CNC sont uniques car elles traitent avec des feuilles de métal dont l'état initial peut varier considérablement. Cela rend difficile la création d'un Gcode adapté à ces variations. De plus, il est crucial de contrôler la hauteur de coupe et de maintenir la torche perpendiculaire à la surface pour obtenir des résultats de coupe optimaux._

![primer_cut-angularity](assets/images/primer_cut-angularity.png)
# Règles de sécurité

*La découpeuse plasma est un outil qui génère beaucoup de chaleur, d'étincelles et de poussières, il faut donc suivre des règles de sécurité stricte.*

* Toujours avoir l'approbation d'un fabmanager
* Être au moins 2 dans le bâtiment (idéalement dans le grand méca)
* Allumer la ventilation générale et si possible utiliser la ventilation ciblée de l'atelier
## EPI

*Équipement de sécurité minimal :*

* Lunettes de sécurité teintée
* Gants pour manipuler le métal
# Procédures

*Cette partie décrit la procédure de mise en route de la machine ainsi que la génération de fichiers compatible avec l'outil de découpe plasma à commande numérique (CNC).*
## Mise en route
### Machine

* Pour mettre en route la machine, assurez vous que le câble d'alimentation est branché puis débloquez le l'interrupteur coup de poing en tournant celui-ci dans le sens inverse des aiguilles d'une montre.
* Allumez ensuite l'ordinateur en appuyant sur le bouton de mise en route sur la façade du boitier de celui-ci.
* Ouvrez la vanne d'air comprimé à coté du poste de découpe plasma.
* Assurez vous que le poste est branché à une prise 380V
* Tournez le bouton d'alimentation du poste de découpe plasma.

*Ne pas oublier de mettre la pince du poste de découpe sur le matériau !*

*Tous les voyants doivent passer au vert.*

![IMG_0353](assets/images/img_0353.jpg)
![IMG_0354](assets/images/img_0354.jpg)
![IMG_0357](assets/images/img_0357.jpg)
![IMG_0359](assets/images/img_0359.jpg)
### Logiciel

* Lorsque l'ordinateur démarre, patientez jusqu'à ce que l'application QT Plasma C s’exécute.
* Sur l'interface de l'application, cliquez sur le bouton virtuel *"E-stop"* puis sur le bouton *"Power"*.
* Il faut maintenant que la machine trouve ses origines.
* Assurez vous qu'il n'y ai aucun obstacle sur la surface de travail de la machine.
* Cliquez sur *"Home all"* pour démarrer la procédure de Homing et attendez que celle-ci se termine.

*Vous pouvez désormais déplacer la machine à l'aide des flèches dans l'interface de QT plasma C.*

![Capture d’écran_2024-04-03_16-44-41](assets/images/capture-d-ecran_2024-04-03_16-44-41.png)
![Capture d’écran_2024-04-03_16-44-58](assets/images/capture-d-ecran_2024-04-03_16-44-58.png)
![Capture d’écran_2024-04-03_16-45-11](assets/images/capture-d-ecran_2024-04-03_16-45-11.png)
# Découpe
## Fichier
### Sur Sheetcam

# Ouvrir l'application SheetCam
# Cliquer sur "fichier" puis sur "importer un dessin" et sélectionner l'origine du dessin lors de l'import. Le fichier en question doit être un .svg ou .dxf.
# Cliquer sur "nouvel opération de jet".
# Sélectionner le calque à découper ainsi que l'outil utiliser en fonction du matériau (composition et épaisseur).
# Modifier les paramètres en fonction du résultat souhaité (ex : angles vifs = ajouter des boucles en entrée/sorties).
# Cliquer sur éxécuter le post-processeur et choisir le dossier de sortie.

![Capture d’écran_2024-04-03_16-54-06](assets/images/capture-d-ecran_2024-04-03_16-54-06.png)
![Capture d’écran_2024-04-03_16-54-40](assets/images/capture-d-ecran_2024-04-03_16-54-40.png)
![Capture d’écran_2024-04-03_16-55-11](assets/images/capture-d-ecran_2024-04-03_16-55-11.png)
![Capture d’écran_2024-04-03_16-55-28](assets/images/capture-d-ecran_2024-04-03_16-55-28.png)
![Capture d’écran_2024-04-03_16-55-56](assets/images/capture-d-ecran_2024-04-03_16-55-56.png)
![Capture d’écran_2024-04-03_16-56-11](assets/images/capture-d-ecran_2024-04-03_16-56-11.png)
![Capture d’écran_2024-04-03_16-56-25](assets/images/capture-d-ecran_2024-04-03_16-56-25.png)
![Capture d’écran_2024-04-03_16-56-35](assets/images/capture-d-ecran_2024-04-03_16-56-35.png)
![Capture d’écran_2024-04-03_16-56-59](assets/images/capture-d-ecran_2024-04-03_16-56-59.png)
![Capture d’écran_2024-04-03_16-57-12](assets/images/capture-d-ecran_2024-04-03_16-57-12.jpg)
## Lancement
### Sur Qt Plasma C

# Ouvrer le fichier gcode en .tap généré sur SheetCam.
# définisser l'origine de votre découpe en plaçant la croix laser où vous souhaitez commencer puis cliquer sur "laser" puis "mark edge".
# lancer une découpe "à blanc" pour visualiser votre découpe.
# si le modèle passe dans votre plaque, cliquer sur "Torch on" puis lancer la découpe.

*Il arrive que le logiciel se mette en erreur car le poste rencontre des difficultés pour générer l'arc électrique, activer la fonction "Ignore OK" peut dépanner le soucis toutefois vous perdrez la fonction THC (Torch Height control).*

![Capture d’écran_2024-04-03_16-45-44](assets/images/capture-d-ecran_2024-04-03_16-45-44.png)
![Capture d’écran_2024-04-03_16-46-00](assets/images/capture-d-ecran_2024-04-03_16-46-00.png)
![Capture d’écran_2024-04-03_16-46-25](assets/images/capture-d-ecran_2024-04-03_16-46-25.png)
![Capture d’écran_2024-04-03_16-46-35](assets/images/capture-d-ecran_2024-04-03_16-46-35.png)


L'interface QT Plasma C vous permet de créer des G-Code de toutes pièce grâce à l'onglet "Conversational".
# Gravure Laser sur métal avec AtomStack R30
## Fichier
### Avec Gimp et le plugin Buildbotic Laser modifié

# Ouvrir GIMP dans Application > Graphisme
# Ouvrir un fichier .png/.jpeg avec la meilleure résolution possible
# Exporter en gcode Fichier > Export g-code for laser engraving
# Définir les paramètres en fonction de vos besoins :
- Largeur de l'image
- Espacement des lignes
- Vitesse
- Puissance minimum
- Puissance maximum
- Distance minimum pour la vitesse rapide
- Valeur de pixel minimum pris en compte
# Enregistrer le fichier dans le dossier nc_files

![2024-09-05_17-18-54](assets/images/2024-09-05_17-18-54.png)
![2024-09-05_17-19-50](assets/images/2024-09-05_17-19-50.png)
![2024-09-05_17-20-11](assets/images/2024-09-05_17-20-11.png)
![2024-09-05_17-20-38](assets/images/2024-09-05_17-20-38.png)
![2024-09-05_17-21-01](assets/images/2024-09-05_17-21-01.png)
![2024-09-05_17-21-39](assets/images/2024-09-05_17-21-39.png)
![2024-09-05_17-22-03](assets/images/2024-09-05_17-22-03.png)
## Lancement
### Sur la machine

# Installer le module laser dans son emplacement
# Serrer les deux vis sur la droite du support en positionnant le module à la bonne hauteur
# Brancher le câble du module sur le câble de la machine
# Allumer le module en enclenchant l'interrupteur dans l'armoire électrique
# Sortir la pige de calibration et descendre le module en Z- jusqu'à ce que la pige touche le matériau

![IMG_0441](assets/images/img_0441.jpg)
![IMG_0450](assets/images/img_0450.jpg)
![IMG_0452](assets/images/img_0452.jpg)
![IMG_0455](assets/images/img_0455.jpg)
![IMG_0456](assets/images/img_0456.jpg)
![IMG_0459](assets/images/img_0459.jpg)
![IMG_0461](assets/images/img_0461.jpg)
![IMG_0462](assets/images/img_0462.jpg)
### Sur Qt Plasma C

# Cliquer sur "Choose Laser" pour utiliser le pointeur du module laser comme origine
# Cliquer sur "Open" pour ouvrir la fenêtre de sélection du fichier
# En bas de cette fenêtre, cliquer sur "all" dans les types de fichier à afficher
# Sélectionner le fichier puis cliquer sur "Select"
# Définir l'origine du job
# Cliquer sur "Cycle Start" pour démarrer le job

![Capture d’écran_2024-09-05_17-23-19](assets/images/capture-d-ecran_2024-09-05_17-23-19.png)
![Capture d’écran_2024-09-05_17-24-48](assets/images/capture-d-ecran_2024-09-05_17-24-48.png)
![Capture d’écran_2024-09-05_17-25-26](assets/images/capture-d-ecran_2024-09-05_17-25-26.png)
![Capture d’écran_2024-09-05_17-25-53](assets/images/capture-d-ecran_2024-09-05_17-25-53.png)
![Capture d’écran_2024-09-05_17-26-07](assets/images/capture-d-ecran_2024-09-05_17-26-07.png)
![Capture d’écran_2024-09-05_17-26-38](assets/images/capture-d-ecran_2024-09-05_17-26-38.png)
![Capture d’écran_2024-09-05_17-26-55](assets/images/capture-d-ecran_2024-09-05_17-26-55.png)
