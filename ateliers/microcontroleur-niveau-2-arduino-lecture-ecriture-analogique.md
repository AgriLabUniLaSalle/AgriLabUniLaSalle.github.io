<!--
Projet Redmine : Tutoriels
Source : Question
ID source : 97
Section : Atelier de formations
Derniere modification : 2022-03-07 11:51:17
-->

# Microcontroleur niveau 2 - Arduino - Lecture/écriture analogique

niveau 2 : Lecture/ écriture analogique
## Déroulé

* Lire une valeur analogique : résistance variable , analogRead() 
* Combiner la résistance variable (potentiomètre) avec une autre fonction vue au niveau 1
* conditionnel if() et opérateurs de comparaison
* opération mathématique de base et complexification
* différents types de mémoires compréhension et limitations
* analogWrite() 

Si temps restant :
* utilisation d'un capteur dans le kit KEYES et début d'un projet personnel , lien https://wiki.tkkrlab.nl/tkkrlab.nl/wiki/Arduino_37_sensors.html
* tone et haut parleur
## Contenu illustratif

https://www.arduino.cc/en/Tutorial/AnalogInput

!https://www.arduino.cc/en/uploads/Tutorial/AnalogReadSerial_sch.png!


Exemple de potentiometre avec Haut-parleur,

<pre><code class="c">
int valeur;


void setup() {
  
}


void loop() {
  valeur = analogRead(A0);
  
map(valeur, 0, 1023, 200, 13000);

  tone(8, valeur);
}


```

### Remerciements:

Ce projet est cofinancé par l'Union Européenne avec le fond Européen de Développement (FEDER) région Haut-de-France et AgriLab UniLaSalle , dans le cadre de l'OpenLab.
!http://agrilab.unilasalle.fr/wp-content/uploads/2019/11/Logo-UE-SD.jpg! !http://agrilab.unilasalle.fr/wp-content/uploads/2019/11/FEDER-SD.png! !{width:300px}http://fab.academany.org/2021/labs/agrilab/images/about/agrilabLogo.jpg!
