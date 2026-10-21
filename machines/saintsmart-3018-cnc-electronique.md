<!--
Projet Redmine : Tutoriels
Source : Question
ID source : 190
Section : Machines
Derniere modification : 2021-12-07 16:01:14
-->

# SaintSmart 3018 CNC - electronique

![cnc3018_site](assets/images/cnc3018_site.jpg)

Lien fabricant : [[https://docs.sainsmart.com/article/3jgtgas880-genmitsu-3018-pro-resources]]

Destinée à l'usinage de circuits électroniques.

Zone usinable , environ 300mm sur 180mm et 80mm (moins martyre et fraise).

Attention : inversion des limits switchs par rapport à la notation sur la carte de controle GRBL , inversion entre Z et X !!!

GRBL dernier réglages :
$1=25
$2=2
$3=2
$4=0
$5=0
$6=0
$10=1
$11=0.010
$12=0.002
$13=0
$20=0
$21=1
$22=1
$23=3
$24=25.000
$25=500.000
$26=250
$27=2.000
$30=1000
$31=0
$32=0
$100=800.000
$101=800.000
$102=800.000
$110=1000.000
$111=1000.000
$112=600.000
$120=30.000
$121=30.000
$122=30.000
$130=291.000
$131=169.000
$132=50.000


Tutoriel pour le palpeur en Z : https://docs.sainsmart.com/article/yhgowhcb8x-what-is-a-z-probe-how-do-i-use-it

Utiliser la sonde Z et le heighmap : https://github.com/adriantrains/cnc_home_lab
