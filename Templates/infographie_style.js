// Templates/infographie_style.js
// Style de référence pour les infographies PowerPoint (pptxgenjs)
// Médico-social — RBPP / TNmP / Droits des personnes
//
// Deux formats supportés :
//   • "petale"  — Fleur rayonnante (RBPP, TNmP, format standard médico-social)
//   • "cartes"  — Grille de cartes thématiques (CNT HAS 2026, format avancé)
// Basé sur infographie_cnt_has2026.pptx (palette et structure de référence)

module.exports = {

  // --- Mise en page ---
  layout: "LAYOUT_WIDE",          // 16:9
  canvas: { w: 33.87, h: 19.05 }, // cm
  font:      "Calibri",
  fontEmoji: "Segoe UI Emoji",

  // --- Format par défaut ---
  defaultFormat: "petale",        // "petale" ou "cartes"

  // =================================================================
  // COULEURS
  // =================================================================
  colors: {
    background:   "0E0C25", // Fond quasi-noir (toutes les slides)
    cardDark:     "14112A", // Fond des cartes (format cartes)
    cardPanel:    "12103A", // Variante panneau (colonne gauche)
    text:         "FFFFFF", // Texte principal
    textMuted:    "8B8EC8", // Sous-titres, légendes
    textDesc:     "C4C8E8", // Descriptions italiques dans les cartes
    textOnAccent: "0E0C25", // Texte sur fond clair/coloré (badges numéros)

    // Palette d'accents — 7 couleurs (une par thème / pétale)
    accents: [
      "7B61FF", // Violet     — thème 1
      "F9C846", // Or ambre   — thème 2 / séparateurs
      "00B4D8", // Cyan       — thème 3
      "06D6A0", // Vert menthe — thème 4
      "FF6B9D", // Rose vif   — thème 5
      "FB923C", // Orange     — thème 6
      "C084FC", // Lavande    — thème 7
    ],

    // Teintes sombres appairées aux accents (fond de cartes CNT, slide colonnes)
    accentDark: [
      "083D4A", // sombre cyan
      "4A1030", // sombre rose
      "023D2E", // sombre vert
      "3D3000", // sombre or
    ],
  },

  // =================================================================
  // FORMAT PÉTALE / FLEUR — format standard RBPP
  // =================================================================
  petale: {
    // Slide 1 — fleur
    flower: {
      cx: 16.94,  // Centre horizontal (cm)
      cy:  9.53,  // Centre vertical (cm)
      r:   2.5,   // Rayon du cercle central (cm)
      circleFill: "7B61FF", // Couleur du cercle central (accents[0])
      titleFontSize: 14, bold: true, color: "FFFFFF",

      // 7 pétales — positions angulaires en degrés
      petalAngles: [270, 321, 12, 63, 141, 192, 243],
      petalDist:   5.2,  // Distance centre-pétale → centre-fleur (cm)
      petalW:      4.5,  // Largeur du pétale (cm)
      petalH:      3.2,  // Hauteur du pétale (cm)
      petalRounding: 0.08, // Arrondi (ratio)
      petalFontSize: 11, petalBold: true,
    },

    // Slides détail (une par pétale)
    detail: {
      barH:    0.305,   // Hauteur barres top/bottom (cm)
      headerTitle: {
        x: 0.76, y: 0.56, h: 1.40,
        fontSize: 22, bold: true, color: "FFFFFF",
      },
      headerSub: {
        x: 0.76, y: 1.91, h: 0.89,
        fontSize: 12, color: "8B8EC8",
      },
      numDecoBg: {
        // Grand numéro décoratif en arrière-plan (haut droite)
        x: 27.0, y: 0.40, w: 6.5, h: 5.0,
        fontSize: 96, bold: true, alpha: 70, // couleur = accent du pétale
      },
      card: {
        x: 0.89, y: 3.10, w: 32.09,  // h = jusqu'à barre bottom
        fill: "14112A",
        borderPt: 1.0,
        topBarH: 0.20,                 // barre colorée top de la carte
        bulletSquare: { size: 0.30 }, // indicateur carré devant chaque bullet
        bulletX: 0.89,  bulletTextX: 1.50,
        bulletFontSize: 14, bulletColor: "FFFFFF",
      },
    },
  },

  // =================================================================
  // FORMAT CARTES — format avancé (d'après infographie_cnt_has2026)
  // =================================================================
  cartes: {
    // En-tête standard (slides contenu)
    header: {
      title:   { x: 0.76, y: 0.56, h: 1.40, fontSize: 22, bold: true, color: "FFFFFF" },
      subtitle:{ x: 0.76, y: 1.91, h: 0.89, fontSize: 12, color: "8B8EC8" },
      contentTopY: 3.05, leftMargin: 0.89,
    },
    barH: 0.305, // barres top/bottom

    // Couverture (slide 1)
    cover: {
      decoRect:    { x: 21.59, y: 0, w: 12.19, h: 19.05, alpha: 16 }, // fill = accents[0]
      decoCircle1: { cx: 22.35, cy: -2.03, r:  5.08, alpha: 30 },
      decoCircle2: { cx: 26.67, cy: 13.21, r:  4.06, alpha: 25 },
      decoCircle3: { cx: -1.52, cy: 14.73, r:  3.56, alpha: 20 },
      divider:     { x: 0, y: 9.14, w: 19.81, pt: 1.5 },              // color = accents[1]
      badge:       { x: 1.52, y: 3.05, w: 7.11, h: 1.17, rounding: 0.05 },
      title:       { x: 1.52, y: 4.52, w: 20.83, h: 4.32, fontSize: 32, bold: true, color: "FFFFFF" },
      subtitle:    { x: 1.52, y: 8.61, w: 20.83, h: 0.89, fontSize: 16, color: "8B8EC8" },
      stats: {
        y: 10.67, h: 2.79, colW: 6.35,
        xs: [1.52, 8.89, 16.26],       // 3 colonnes de stats
        valueFontSize: 36, bold: true,  // color = accents[1]
        labelFontSize: 11, color: "8B8EC8",
      },
      dots: { xs: [1.52, 7.11, 12.70, 18.29], y: 15.37, d: 0.76 }, // couleurs = accents 0-3
      source: { x: 1.52, y: 16.51, w: 20.83, h: 0.71, fontSize: 10, italic: true, color: "8B8EC8" },
    },

    // Grille de cartes (slides 3, 6, etc.)
    cardGrid: {
      // Grille 3×2
      cols3x2: { xs: [0.89, 11.76, 22.63], ys: [3.05, 10.69], w: 10.67, h: 7.34 },
      // Grille 4×2 (fiches 1-7 sur slide 4)
      cols4x2: { xs: [0.89, 9.07, 17.25, 25.43], ys: [2.997, 10.64], w: 8.13, h: 7.34 },
      // Anatomie carte standard (type slide 3)
      card: {
        fill:       "14112A",
        borderPt:   1.0,
        topBarH:    0.20,
        numBadge:   { offsetX: 0.30, offsetY: 0.38, d: 1.40, fontSize: 9, bold: true, textColor: "0E0C25" },
        title:      { offsetX: 1.63, offsetY: 0.33, fontSize: 13, bold: true, color: "FFFFFF" },
        desc:       { offsetX: 0.30, offsetY: 2.54, fontSize: 10, italic: true, color: "C4C8E8" },
        sep:        { offsetY: 4.42, h: 0.05, alpha: 50 },
        bullet: {
          dotD: 0.30, dotOffsetX: 0.30,
          textOffsetX: 0.75, fontSize: 9, color: "FFFFFF",
          // 4 bullets en grille 2×2 : espacement 0.97cm vertical, 5.03cm horizontal
          grid: { rows: 2, cols: 2, stepY: 0.97, stepX: 5.03, startOffsetY: 5.38 },
        },
      },
      // Variante carte type slide 6 (barre verticale gauche au lieu de barre top)
      cardV: {
        fill:      "13112C",
        borderPt:  1.0,
        leftBarW:  0.20,
        emoji:     { offsetX: 0.38, offsetY: 0.38, d: 1.40, fontSize: 22 },
        title:     { offsetX: 1.78, offsetY: 0.33, fontSize: 13, bold: true }, // color = accent
        body:      { offsetX: 0.38, offsetY: 2.08, fontSize: 10.5, color: "FFFFFF" },
      },
    },

    // Slide colonnes (slide 2 — architecture du référentiel)
    colonnes: {
      n: 4, startX: 0.89, stepX: 8.15, w: 8.00, h: 15.44, startY: 1.90,
      topBarH: 0.25,
      badge:    { h: 0.71, alpha: 30, fontSize: 9, bold: true },
      sepH:     0.08, sepAlpha: 60,
      bulletBar:{ w: 0.13, h: 1.17 },
      itemH:    1.12,
      title:    { fontSize: 13, bold: true, color: "FFFFFF" },
      item:     { fontSize: 10, color: "FFFFFF" },
      borderPt: 1.0,
    },

    // Barre citation pied de slide
    quoteBar: {
      x: 0, y: 17.02, w: 33.87, h: 1.73,
      fill: "1B163D",
      leftAccent: { w: 0.15, color: "F9C846" },
      fontSize: 11, italic: true, color: "FFFFFF",
    },
  },

  // =================================================================
  // TITRE ET PIED DE PAGE (communs aux deux formats)
  // =================================================================
  slideTitle: { x: 0.76, y: 0.56, h: 1.40, fontSize: 22, bold: true, color: "FFFFFF" },
  footer: {
    x: 0.76, y: 18.54, w: 32.35, h: 0.40,
    fontSize: 10, italic: true, color: "8B8EC8", align: "right",
  },
};
