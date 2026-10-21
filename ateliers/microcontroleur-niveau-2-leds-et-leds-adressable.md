<!--
Projet Redmine : Tutoriels
Source : Question
ID source : 204
Section : Atelier de formations
Derniere modification : 2023-04-11 16:31:05
-->

# Microcontroleur niveau 2 - LEDs et LEDs adressable

Prérequis : Arduino niveau 1 et apporter son ordinateur (avec arduino installé)

Principe de fonctionnement LED et alimentation
U = R I
![LED_Blink_s](assets/images/led_blink_s.png)


![led](assets/images/led-2.jpg) et ![LED_SMt_s](assets/images/led_smt_s.jpg) 

Puissance = transistor

![transistor](assets/images/transistor.png)

![transistor_led](assets/images/transistor_led.png)

LED SMD , digikey
rouge : 67-1356-1-ND , https://www.digikey.fr/fr/products/detail/lumex-opto-components-inc/SML-LX1206IC-TR/229140?s=N4IgTCBcDaIGwHYC0BGAzAVjqpA5AIiALoC%2BQA , 
Fiche constructeur : [[SML-LX1206IC-TR.pdf]] , [[http://agrilab.unilasalle.fr/projets/attachments/3801]]
vert : 67-1357-1-ND
orange : 350-2049-1-ND
bleu : 732-4989-1-ND
blanc : 1214-1447-1-ND
## Intérieur

![D233ZOEUwAAJ1FK](assets/images/d233zoeuwaaj1fk.jpg)
## Bande et couleur

![couleur_principe](assets/images/couleur_principe.jpg)

![bande_multiple](assets/images/bande_multiple.jpg)

![bande_principe](assets/images/bande_principe.png)


!Adressable!

= adresse = microcontroleur dédié par LED
### WS2812B 

![WS2812B-5050_01](assets/images/ws2812b-5050_01.jpg)

![WS2812B-5050_03](assets/images/ws2812b-5050_03.jpg)

[[source:WS2812B_Datasheet.pdf]] et [[http://agrilab.unilasalle.fr/projets/attachments/3812]]
## Bibliothèque

Adafruit NeoPixel Library , https://github.com/adafruit/Adafruit_NeoPixel


Voir exemple de la biblbiothèque


<pre><code class="c">
// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// Released under the GPLv3 license to match the rest of the
// Adafruit NeoPixel library

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PIN        6 // On Trinket or Gemma, suggest changing this to 1

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 16 // Popular NeoPixel ring size

// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. Note that for older NeoPixel
// strips you might need to change the third parameter -- see the
// strandtest example for more information on possible values.
Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

void setup() {
  // These lines are specifically to support the Adafruit Trinket 5V 16 MHz.
  // Any other board, you can remove this part (but no harm leaving it):
#if defined(__AVR_ATtiny85__) && (F_CPU == 16000000)
  clock_prescale_set(clock_div_1);
#endif
  // END of Trinket-specific code.

  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
}

void loop() {
  pixels.clear(); // Set all pixel colors to 'off'

  // The first NeoPixel in a strand is #0, second is 1, all the way up
  // to the count of pixels minus one.
  for(int i=0; i<NUMPIXELS; i++) { // For each pixel...

    // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
    // Here we're using a moderately bright green color:
    pixels.setPixelColor(i, pixels.Color(0, 150, 0));

    pixels.show();   // Send the updated pixel colors to the hardware.

    delay(DELAYVAL); // Pause before next pass through loop
  }
}

```


Exemple de Bleu à rouge

<pre><code class="c">

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> 
#endif

#define PIN        6 
#define NUMPIXELS 10

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin(); 
}

void loop() {
  //pixels.clear(); 
  /*
  pixels.setPixelColor(0, pixels.Color(255, 0, 0));
  pixels.show();
  delay(1000);
  pixels.setPixelColor(0, pixels.Color(0, 0, 255));
  pixels.show(); 
  delay(1000);
  */

  for(int i=0; i<5; i++) { 
    pixels.setPixelColor(i, pixels.Color(0, 0, 255));
    pixels.show(); 
    delay(500);
    pixels.clear();  
  }
  for(int i=5; i<9; i++) { 
    pixels.setPixelColor(i, pixels.Color(255, 0, 0));
    pixels.show(); 
    delay(500); 
    pixels.clear(); 
  }

}


```


<pre><code class="c">
/*
Code réalisé à AgriLab par Luc Hanneuse
CC BY SA
*/

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> 
#endif

#define PIN        6 
#define NUMPIXELS 30
int nombre_pixel = 30;
int vitesse = 100;

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  pixels.begin(); 
  Serial.begin(9600);
}

void loop() {

  for(int i=0; i<nombre_pixel; i++) { 
    int rouge = (i+1)  * ( 255 / nombre_pixel) ;
    int bleu = 255 - rouge;
    Serial.print(i);Serial.print(" ");Serial.println(rouge);
    pixels.setPixelColor(i, pixels.Color(rouge  , 0, bleu));
    pixels.show(); 
    delay(vitesse);
    pixels.clear();  
  }

}

```
