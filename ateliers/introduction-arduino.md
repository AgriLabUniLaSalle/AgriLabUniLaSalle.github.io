# Introduction Arduino

1. Introduction Arduino

<img src="/ateliers/assets/images/arduino.jpg" alt="arduino" width="300">

Site principal : [https://www.arduino.cc](https-www-arduino-cc.md)

Logiciel : [https://www.arduino.cc/en/Main/Software](https-www-arduino-cc-en-main-software.md)

Tutoriel officiel : [https://www.arduino.cc/en/Tutorial/HomePage](https-www-arduino-cc-en-tutorial-homepage.md)

Ressources, toutes les commandes : [https://www.arduino.cc/reference/en/](https-www-arduino-cc-reference-en.md)

Exemple de code :

```text
/*
  Blink
  Turns an LED on for one second, then off for one second, repeatedly.
*/

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);                       // wait for a second
  digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);                       // wait for a second
}
```

Schémat électronique correspondant

<img src="/ateliers/assets/images/blink_schematic.png" alt="blink schematic" width="300">

<img src="/ateliers/assets/images/blink_fritzing.png" alt="blink fritzing" width="300">

---

[← Retour aux ateliers](/ateliers/)
