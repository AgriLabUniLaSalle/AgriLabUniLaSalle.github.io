# Atelier Découpeuse Laser

1. Atelier Découpeuse Laser

## Conditions importantes de sécurité

*La machine peut prendre feu donc il est obligatoire de rester devant la machine lorsqu'on l'utilise.*
La fumée émise par la machine peut être toxique, il est donc important de demander à un fabmanager avant d'utiliser un matériau s'il peut être utilisé pour de la découpe laser.

## Fonctionnement de la machine

Un tube situé derrière la découpeuse excite des électrons qui vont former un faisceau lumineux qui va être projeté sur différents miroirs. Le faisceau lumineux va converger vers une lentille qui va concentrer l'énergie lumineuse pour pouvoir découper ou graver.
Il est donc important de faire une focale avant chaque utilisation.

Le matériau ne doit pas être trop épais afin de pouvoir avoir une découpe "propre" (en raison de la distance focale)
Epaisseur max du matériau : 6mm

La machine fonctionne capot fermé pour que la fumée puisse être évacuée dehors.

1) Démarrer : tourner la clé, l'aération se met directement en marche
2) Faire la focale : Appuyer sur "Z", mettre la petite plaque noir sous la plaque dorée en métal située derrière le laser, appuyer sur "Datum"
3) Sélectionner le fichier : avec les flèches haut et bas
4) Découper/Graver (à partir du logiciel) : rester près de la machine
5) Eteindre : attendre quelques minutes que les fumées partent avant d'éteindre puis tourner la clé ou appuyer sur le petit bouton rouge près de la clé (le gros bouton rouge est un bouton d'arrêt d'urgence)

## Fonctionnement du logiciel de la machine : LaserCut

1) Importer son fichier sous format dxf ou dessiner directement sur LaserCut (mais figures limitées) : attention l'image doit être vectorisée
2) Les couches/couleurs : permettent de demander à la machine de découper ou graver (en mettant des puissances différentes)
Attention avant de lancer réellement la machine, il est préférable de faire des tests de puissance et de profondeur pour tester la découpe et/ou la gravure (Pour cela, tester un petit carré dans le matériau par exemple)
Mode Cut : Le laser suit les courbes
Mode Engrave : Le laser parcourt la surface
3) Envoyer en cliquant sur "Start", si jamais ça ne fonctionne pas, essayer de relancer car il y a quelques fois un faux-contact entre l'ordinateur et la machine.

Prérequis:
- Pixel vs vecteur
![vector-vs-bitmap](/ateliers/assets/images/vector-vs-bitmap.gif)
<img src="/ateliers/assets/images/Bezier_curve.png" alt="Bezier curve" width="400">

Point importants :
- Chemin du laser : tube, miroir, lentille
![optics path](/ateliers/assets/images/optics_path.jpg)
- Fonctionnement lentille focale : importance de la mise au point, matériel plane, limitation d'épaisseur
<img src="/ateliers/assets/images/Focal-length-a.png" alt="Focal-length-a" width="400">
![non-focus](/ateliers/assets/images/non-focus.jpg)
<img src="/ateliers/assets/images/epaisseur-materiel.jpg" alt="epaisseur-materiel" width="400">
- Les différents éléments et pourquoi : compresseur air, refroidissement à eau, extraction fumée
- Longueur d'onde et absorption des matériaux -> ne fonctionne pas avec métal. Notion gravure/découpe
- Notion de Kerf : assemblage et dimensions
![kerf](/ateliers/assets/images/kerf.png)
- Pas de compensation d'outil
- Test systématique de puissance et vitesse
- Ordre de découpe
- Notion de calque/couleur dans le logiciel : puissance/vitesse/ordre

Matériaux strictement interdits = Expulsion immédiate et définitive sans recours possible :
- PVC
- matériaux contenant du chlore
- Certains types de vinyles

---

[← Retour aux ateliers](/ateliers/)
