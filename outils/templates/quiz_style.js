// Templates/quiz_style.js
// Style de référence pour les quiz PowerPoint (pptxgenjs)
// Médico-social — RBPP / TNmP / Droits des personnes
//
// Structure commune à quiz_rbpp_v2, quiz_cnt_v1, quiz_tnmp_v2 :
//   • 1 slide couverture + N paires (question/réponse)
//   • Pas de slide finale distincte
//   • Format 16:9 — 33,78 × 19,05 cm (LAYOUT_WIDE)
//   • Police Calibri partout
//   • Tailles de police IDENTIQUES dans tous les quiz (seules les couleurs varient)

module.exports = {

  // --- Mise en page ---
  layout: "LAYOUT_WIDE",          // 16:9
  canvas: { w: 33.78, h: 19.05 }, // cm
  font: "Calibri",

  // =================================================================
  // PALETTES DE COULEURS — changer `defaultPalette` pour switcher
  // =================================================================
  defaultPalette: "rbpp",

  palettes: {

    // ── RBPP (quiz_rbpp_v2_2026-04-05) ──
    rbpp: {
      background:    "111D3C", // Bleu marine profond
      primary:       "00B4D8", // Cyan — barre top Q, badge Q, option A, sous-titre couverture
      gold:          "FFB703", // Orange-or — barre bottom, option B, ligne séparatrice couverture
      accent3:       "E63946", // Rouge — option C
      accent4:       "06D6A0", // Vert menthe — option D
      answer:        "00C897", // Vert — barre top R, checkmark, BONNE RÉPONSE, EXPLICATION
      optionRowBg:   "1A2F5E", // Fond rangées options
      correctBg:     "044E3A", // Fond zone bonne réponse
      explBg:        "1C2F5A", // Fond zone explication
      muted:         "8BAEC8", // Texte secondaire (source, niveau)
      counter:       "5A7BA8", // Compteur de page
      badgeNumColor: "FFFFFF", // Couleur du numéro dans le badge Q (blanc sur fond gold)
    },

    // ── CNT (quiz_cnt_v1_2026-04-05) ──
    cnt: {
      background:    "110E2A", // Violet nuit
      primary:       "7B61FF", // Violet — barre top Q, badge Q, option A
      gold:          "F9C846", // Or jaune — barre bottom, option B
      accent3:       "FF6B9D", // Rose — option C
      accent4:       "3DD9C5", // Turquoise — option D
      answer:        "3DD9C5", // Turquoise — tout ce qui concerne la réponse
      optionRowBg:   "1E1847",
      correctBg:     "0A2D2B",
      explBg:        "1A1440",
      muted:         "8B8EC8",
      counter:       "5A5A8A",
      badgeNumColor: "110E2A", // Sombre (fond du badge = gold)
    },

    // ── TNmP (quiz_tnmp_v2_2026-04-05) ──
    tnmp: {
      background:    "111D3C",
      primary:       "F4A261", // Orange — barre top Q, option A
      gold:          "2EC4B6", // Turquoise — barre bottom, answer, option B
      accent3:       "9B5DE5", // Violet — option C
      accent4:       "FF6B6B", // Rouge-rose — option D
      answer:        "2EC4B6", // Turquoise
      optionRowBg:   "1A2F5E",
      correctBg:     "0A3D3B",
      explBg:        "1C2F5A",
      muted:         "8BAEC8",
      counter:       "5A7BA8",
      badgeNumColor: "111D3C",
    },
  },

  // =================================================================
  // TAILLES DE POLICE (communes à tous les quiz — demi-points raw)
  // =================================================================
  fontSizes: {
    coverBadge:       1300, // 13 pt — pill surtitre couverture
    coverTitle:       3400, // 34 pt — titre principal couverture
    coverSubtitle:    1700, // 17 pt — sous-titre couverture
    coverCount:       2800, // 28 pt — "N questions"
    coverLevel:       1400, // 14 pt — "Niveau professionnel"
    coverSource:      1100, // 11 pt — source en bas
    qBadgeQ:          1100, // 11 pt — lettre "Q" dans le badge
    qBadgeNum:        2800, // 28 pt — chiffre dans le badge
    qCounter:         1100, // 11 pt — compteur "X / N" en haut droite
    qText:            1700, // 17 pt — texte de la question
    optLetter:        1800, // 18 pt — lettre A/B/C/D dans le cercle
    optText:          1350, // 13,5 pt — texte de l'option
    aLabel:           1400, // 14 pt — "BONNE RÉPONSE"
    aCounter:         1100, // 11 pt — compteur "Q N" sur slide réponse
    aCorrectLetter:   2000, // 20 pt — lettre bonne réponse (cercle)
    aCorrectText:     1700, // 17 pt — texte de la bonne réponse
    aExplLabel:       1000, // 10 pt — label "EXPLICATION"
    aExplText:        1400, // 14 pt — corps de l'explication
  },

  // =================================================================
  // DIMENSIONS ET POSITIONS (en cm — communes à tous les quiz)
  // =================================================================

  // --- Barres horizontales top / bottom ---
  bar: {
    h: 0.33,    // hauteur (cm)
    yBottom: 18.72, // y de la barre bottom
  },

  // --- Couverture ---
  cover: {
    // Décoration droite semi-transparente
    decoRect:   { x: 23.11, y: 0, w: 10.67, h: 19.05, alpha: 22 }, // fill = primary
    decoCircle1:{ cx: 24.13, cy: -1.52, r: 4.06, alpha: 35 },       // fill = primary
    decoCircle2:{ cx: 27.43, cy: 13.72, r: 3.56, alpha: 30 },       // fill = gold
    decoCircle3:{ cx: -1.02, cy: 14.73, r: 2.79, alpha: 25 },       // fill = gold

    badge:  { x: 1.52, y: 3.05, w: 9.14, h: 1.22, rounding: 0.08 }, // fill = primary
    line:   { x: 1.52, y: 8.51, w: 19.05, pt: 1.5 },                 // color = gold
    title:  { x: 1.52, y: 4.52, w: 20.83, h: 4.32 },
    sub:    { x: 1.52, y: 8.61, w: 20.83, h: 0.89 },
    count:  { x: 1.52, y: 10.16, w: 10.16, h: 1.27 },               // bold = gold
    level:  { x: 1.52, y: 11.43, w: 20.83, h: 0.89 },               // color = muted
    source: { x: 1.52, y: 14.22, w: 20.83, h: 0.71 },               // italic, color = muted

    // 4 points décoratifs bas gauche (couleurs = primary, gold, accent3, accent4)
    dots: { x0: 1.52, y: 15.37, r: 0.38, gap: 0.51 },
  },

  // --- Slides Question ---
  question: {
    badge: {
      x: 0.46, y: 0.56, d: 2.84,   // ellipse (fill = gold)
      qLabelY: 0.71,                // y du "Q" dans le badge (relatif au haut du badge)
      numY:    1.15,                // y du chiffre (relatif)
    },
    counter: { x: 28.45, y: 0.51, w: 4.83, h: 0.71 }, // align right, color = counter
    text:    { x: 3.76, y: 0.51, w: 28.45, h: 4.37 }, // bold, white
    sep:     { x: 0.46, y: 5.18, w: 32.87, h: 0.10, alpha: 70 }, // fill = gold

    // Options A, B, C, D
    options: {
      rows: [5.44, 8.41, 11.38, 14.35], // y de départ de chaque rangée (cm)
      h:    2.74,                        // hauteur d'une rangée
      w:    32.87,                       // largeur (pleine largeur - barre gauche)
      leftBarW: 0.203,                   // barre accent gauche (fill = couleur option)
      circle: { x: 0.46, d: 1.78 },     // x et diamètre du cercle lettre
      textX: 3.10,                       // x du texte de l'option
      // Couleurs des 4 options : primary, gold, accent3, accent4
    },
  },

  // --- Slides Réponse ---
  answer: {
    leftBar:  { w: 0.56 },            // barre verticale gauche pleine hauteur (fill = answer)
    check:    { x: 0.89, y: 0.51, d: 1.52 }, // cercle ✓ (fill = answer)
    label:    { x: 2.79, y: 0.66, w: 11.43, h: 0.89 }, // "BONNE RÉPONSE", color = answer
    counter:  { x: 29.21, y: 0.66, w: 4.06, h: 0.71 }, // align right, color = counter
    correctBox: {
      x: 0.56, y: 2.29, w: 33.22, h: 2.997,  // fond = correctBg, border = answer
      circle: { x: 0.97, y: 0.48, d: 1.78 }, // cercle lettre (fill = answer) — relatif à la box
      textX: 3.10, textH: 2.997,
    },
    explLabel:  { x: 0.97, y: 5.40, w: 7.62, h: 0.61 }, // "EXPLICATION", color = answer
    explBox: {
      x: 0.56, y: 6.53, w: 33.22,             // h = jusqu'à la barre bottom
      fill: "explBg",
      goldBar: { w: 0.152 },                   // accent or gauche (fill = gold)
      textX: 1.14,
    },
  },
};
