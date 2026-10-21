<!--
Projet Redmine : Tutoriels
Source : Question
ID source : 177
Section : Atelier de formations
Derniere modification : 2024-03-18 16:15:02
-->

# Microcontroleur niveau 0 - introduction et MicroBit
## Description

* Qu'est ce qu'un microcontroleur ?
* Alimentation de la carte : 3.6V max
* Composants intégrés dans la cartes :
** Capteurs de mouvement
** Emetteur/recepteur bluetooth
** Emetteur/récepteur Radio
** Matrice Led 5x5
** 19 GPIOs

[Micro:Bit V1.5 hardware](https://tech.microbit.org/hardware/1-5-revision/)
![microbit-overview-1-5](assets/images/microbit-overview-1-5.png)

[Pin Out](https://tech.microbit.org/hardware/edgeconnector/)
![edge_connector](assets/images/edge_connector.png)
## Exercices

Lien pour coder : https://makecode.microbit.org/

# Utiliser la matrice pour afficher un texte
![microbit1](assets/images/microbit1.jpg)
![microbit2.7](assets/images/microbit2.7.jpg) 
![microbit2](assets/images/microbit2.jpg)
![microbit3](assets/images/microbit3.jpg) 
# Utiliser les boutons intégrés pour afficher différents textes
![microbit2.5](assets/images/microbit2.5.jpg) 
# Utiliser les capteurs de mouvements pour afficher différents textes
# Brancher une led externe en dimensionnant une résistance sur le 3V [datasheet led rouge](https://www.farnell.com/datasheets/1498852.pdf)
# Brancher une led externe sur une broche pilotable (digital) et la faire clignoter
![microbit4](assets/images/microbit4.jpg) 
![microbit5](assets/images/microbit5.jpg)
![microbit6](assets/images/microbit6.jpg)
![branchement_led](assets/images/branchement_led.png)
# Créer un programme avec une boucle "tant que" et des variables pour faire clignoter la led de plus en plus rapidement
![microbit7](assets/images/microbit7.jpg)
# Brancher la led externe sur une broche pilotable (pwm : expliquer de quoi il s'agit) et faire varier son intensité lumineuse
![microbit8](assets/images/microbit8.jpg)
# Créer un programme avec une boucle "tant que" et des variables pour faire varier l'intensité lumineuse de la led au cours du temps
![microbit9](assets/images/microbit9.jpg)
# Brancher un bouton externe avec une résistance PullDown
[exemple arduino](https://docs.arduino.cc/built-in-examples/digital/Button/)
![branchement_bouton](assets/images/branchement_bouton.png)
# Créer un programme pour allumer la led lorsque l'on appui sur le bouton avec une fonction (si/sinon) 
![microbit10](assets/images/microbit10.jpg)
