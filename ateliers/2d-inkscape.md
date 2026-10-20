---
layout: default
title: Inkscape et dessin 2D
description: Découvrir les principales opérations d’Inkscape et les extensions utiles pour la découpe laser.
permalink: /ateliers/2d-inkscape/
---

# Inkscape et dessin 2D

**Inkscape** est un logiciel libre de dessin vectoriel. Il permet de créer et de modifier des fichiers adaptés à la découpe laser, à la découpe vinyle, à la gravure et à certaines opérations d’usinage CNC.

[Accéder au site officiel d’Inkscape](https://inkscape.org/){: .btn .btn-primary }

## Sommaire

- #opérations-de-base
- #applications-en-fabrication-numérique
- #extensions-pour-la-découpe-laser
- #créer-des-effets-de-trame
- #ressources-complémentaires

---

## Opérations de base

### Créer un cercle ou une ellipse

L’outil **Cercle et ellipse** permet de dessiner des formes circulaires, des ellipses et des arcs.

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/inkscape-002b_ellipse.png
      <br>
      <em>Création d’une ellipse</em>
    </td>
    <td align="center">
      /ateliers/assets/images/inkscape-002_ellipse.png
      <br>
      <em>Résultat obtenu</em>
    </td>
  </tr>
</table>

---

### Créer des courbes de Bézier

L’outil **Courbes de Bézier** permet de créer des tracés droits ou courbes à partir d’une succession de points.

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/inkscape-003b_curve.png
      <br>
      <em>Création du tracé</em>
    </td>
    <td align="center">
      /ateliers/assets/images/inkscape-003_curve.png
      <br>
      <em>Modification des nœuds</em>
    </td>
  </tr>
</table>

---

### Dissocier des éléments

La commande **Dégrouper** permet de séparer les objets qui ont précédemment été regroupés.

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/inkscape-004_break_appart.png
      <br>
      <em>Avant la séparation</em>
    </td>
    <td align="center">
      /ateliers/assets/images/inkscape-004b_break_appart.png
      <br>
      <em>Après la séparation</em>
    </td>
  </tr>
</table>

---

### Réaliser l’union de deux formes

L’opération **Union** fusionne plusieurs formes en un seul objet vectoriel.

> Sélectionnez les formes, puis utilisez **Chemin → Union**.

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/inkscape-005_union.png
      <br>
      <em>Formes initiales</em>
    </td>
    <td align="center">
      /ateliers/assets/images/inkscape-005b_union.png
      <br>
      <em>Résultat de l’union</em>
    </td>
  </tr>
</table>

---

### Réaliser la différence entre deux formes

L’opération **Différence** soustrait la forme placée au-dessus de celle située en dessous.

> Sélectionnez les deux formes, puis utilisez **Chemin → Différence**.

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/inkscape-006_difference.png
      <br>
      <em>Formes initiales</em>
    </td>
    <td align="center">
      /ateliers/assets/images/inkscape-006b_difference.png
      <br>
      <em>Résultat de la différence</em>
    </td>
  </tr>
</table>

---

## Applications en fabrication numérique

Inkscape permet de préparer des fichiers pour différentes machines du FabLab :

- découpeuse vinyle ;
- découpeuse laser ;
- fraiseuse CNC ;
- graveuse ;
- machine de découpe pilotée numériquement.

### Découpe vinyle

La découpe vinyle permet de produire des autocollants, des marquages, des pochoirs et des éléments destinés au flocage textile.

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/vinyle01.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/vinyle02.jpg
    </td>
  </tr>
  <tr>
    <td align="center">
      /ateliers/assets/images/vinyle03.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/vinyle04.jpg
    </td>
  </tr>
</table>

---

### Fraisage et moulage

Un dessin vectoriel peut également servir à préparer un usinage destiné à fabriquer un moule.

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/chocolat01.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/chocolat02.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/chocolat03.jpg
    </td>
  </tr>
  <tr>
    <td align="center">
      /ateliers/assets/images/chocolat04.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/chocolat05.jpg
    </td>
    <td></td>
  </tr>
</table>

---

### Fraisage de mobilier

Les fichiers vectoriels peuvent servir à concevoir des pièces de mobilier découpées ou fraisées sur une machine CNC.

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/muble01.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/muble02.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/muble03.jpg
    </td>
  </tr>
  <tr>
    <td align="center">
      /ateliers/assets/images/muble04.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/muble05.jpg
    </td>
    <td></td>
  </tr>
</table>

---

## Extensions pour la découpe laser

Certaines extensions ajoutent à Inkscape des fonctions utiles pour la gravure, la création de boîtes et la préparation des fichiers de découpe laser.

### Hershey Text

**Hershey Text** permet de générer du texte composé de lignes simples. Ce type de tracé est particulièrement adapté à la gravure laser, car il évite de graver deux fois le contour d’un caractère.

[Découvrir l’extension Hershey Text](https://www.evilmadscientist.com/2011/hershey-text-an-inkscape-extension-for-engraving-fonts/)

<table>
  <tr>
    <td align="center">
      /ateliers/assets/images/hershey.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/hershey2.jpg
    </td>
  </tr>
  <tr>
    <td align="center">
      /ateliers/assets/images/hershey3.jpg
    </td>
    <td align="center">
      /ateliers/assets/images/hershey0.jpg
    </td>
  </tr>
</table>

---

### Tabbed Box Maker

**Tabbed Box Maker** génère automatiquement les plans d’une boîte assemblée par tenons et mortaises.

[Télécharger Tabbed Box Maker](https://github.com/paulh-rnd/TabbedBoxMaker)

#### Installation

Copiez les fichiers suivants dans le dossier des extensions d’Inkscape :

```text
Boxmaker.inx
Schroffmaker.inx
Boxmaker.py