// Templates/word_style.js
// Style de référence pour les documents Word (librairie docx — npm)
// Basé sur 2026-04-06_veille_SERAFIN-PH.docx
// Médico-social — RBPP / TNmP / Droits des personnes

const { AlignmentType, HeadingLevel, LevelFormat, BorderStyle, ShadingType, WidthType } = require("docx");

module.exports = {

  // --- Police de base ---
  font: "Calibri",

  // --- Dimensions de page A4 (en twips) ---
  page: {
    width:   11906,
    height:  16838,
    // Marges serrées (document dense, optimisé écran)
    margins: {
      top:    400,  // ~0,71 cm
      bottom: 400,
      left:   500,  // ~0,88 cm
      right:  500,
      header: 708,  // ~1,25 cm
      footer: 708,
    },
    // Largeur de contenu = 11906 - 500 - 500 = 10906 DXA
    contentWidth: 10906,
  },

  // =================================================================
  // COULEURS (palette complète du document SERAFIN-PH)
  // =================================================================
  colors: {
    navy:          "1B3A6B", // Bleu marine — titre, H1, en-têtes tableau, labels callout
    blue:          "2563EB", // Bleu électrique — H2
    gray:          "6B7280", // Gris — méta, date, caption pied de page
    dark:          "1F2937", // Gris-bleu sombre — corps de texte par défaut
    white:         "FFFFFF", // Sur fond bleu (en-têtes tableau)
    tableEven:     "EEF2F7", // Lignes paires tableau — bleu-gris très pâle
    tableOdd:      "FFFFFF", // Lignes impaires tableau — blanc
    sepLine:       "E5E7EB", // Séparateur horizontal — gris clair
    // Callouts
    warnBorder:    "FCD34D", // ⚠️ Bordure jaune ambre
    warnBg:        "FFFBEB", // ⚠️ Fond jaune très pâle
    infoBorder:    "BFDBFE", // 💡 Bordure bleu ciel
    infoBg:        "EFF6FF", // 💡 Fond bleu très pâle
    successBorder: "86EFAC", // ✅ Bordure vert clair
    successBg:     "F0FDF4", // ✅ Fond vert très pâle
  },

  // =================================================================
  // STYLES DE PARAGRAPHE
  // Tailles en demi-points : 18pt=36, 14pt=28, 12pt=24, 11pt=22, 10pt=20, 9pt=18
  // =================================================================
  styles: {

    // Titre principal (unique, centré, haut de document)
    title: {
      fontSize:     36,          // 18 pt
      bold:         true,
      color:        "1B3A6B",
      alignment:    AlignmentType.CENTER,
      spacingAfter: 40,
    },

    // Ligne méta (date, auteur — sous le titre)
    meta: {
      fontSize:     20,          // 10 pt
      italic:       true,
      color:        "6B7280",
      alignment:    AlignmentType.CENTER,
      spacingAfter: 80,
    },

    // H1 — Section principale (ex. "📋 Sources", "📅 Agenda")
    h1: {
      fontSize:      28,         // 14 pt
      bold:          true,
      color:         "1B3A6B",
      spacingBefore: 240,
      spacingAfter:   80,
    },

    // H2 — Sous-section
    h2: {
      fontSize:      24,         // 12 pt
      bold:          true,
      color:         "2563EB",
      spacingBefore: 160,
      spacingAfter:   60,
    },

    // Corps de texte courant
    body: {
      fontSize:     22,          // 11 pt
      color:        "1F2937",
      spacingAfter:  40,
    },

    // Caption / pied de document
    caption: {
      fontSize:      18,         // 9 pt
      italic:        true,
      color:         "6B7280",
      alignment:     AlignmentType.CENTER,
      spacingBefore: 160,
    },

    // Séparateur horizontal (paragraphe vide avec bordure bas)
    separator: {
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "E5E7EB", space: 0 } },
      spacingBefore: 100, spacingAfter: 100,
    },

    // ── Callouts (encadrés à bordure gauche) ──

    // ⚠️ Avertissement / Point de vigilance
    calloutWarning: {
      fontSize: 22, color: "1F2937",
      spacingAfter: 80,
      border: { left: { style: BorderStyle.SINGLE, size: 12, color: "FCD34D", space: 200 } },
      shading: { fill: "FFFBEB", type: ShadingType.CLEAR },
      indent: { left: 200 },
    },

    // 💡 Information / Orientation
    calloutInfo: {
      fontSize: 22, color: "1F2937",
      spacingAfter: 80,
      border: { left: { style: BorderStyle.SINGLE, size: 12, color: "BFDBFE", space: 200 } },
      shading: { fill: "EFF6FF", type: ShadingType.CLEAR },
      indent: { left: 200 },
    },

    // ✅ Nouveauté / Succès
    calloutSuccess: {
      fontSize: 22, color: "1F2937",
      spacingAfter: 80,
      border: { left: { style: BorderStyle.SINGLE, size: 12, color: "86EFAC", space: 200 } },
      shading: { fill: "F0FDF4", type: ShadingType.CLEAR },
      indent: { left: 200 },
    },

    // Bullet (liste non ordonnée) — utiliser LevelFormat.BULLET
    bullet: {
      fontSize:     22,
      color:        "1F2937",
      spacingAfter:  40,
      // Référence numbering à déclarer dans le Document :
      //   reference: "bullets", level: 0
      //   Caractère niveau 0 : ●   indent left=720, hanging=360
      //   Caractère niveau 1 : ○   indent left=1440, hanging=360
      //   Caractère niveau 2 : ■   indent left=2160, hanging=360
    },
  },

  // =================================================================
  // TABLEAUX
  // =================================================================
  table: {
    // TOUJOURS WidthType.DXA — JAMAIS WidthType.PERCENTAGE
    // Largeur totale = page.contentWidth (10906 DXA)
    defaultWidth:  10906,
    borderStyle:   BorderStyle.SINGLE,
    borderSize:    4,
    borderColor:   "000000",
    cellPadding: { top: 40, bottom: 40, left: 100, right: 100 },
    headerFill:    "1B3A6B",
    headerColor:   "FFFFFF",
    headerBold:    true,
    headerSize:    20,          // 10 pt
    evenRowFill:   "EEF2F7",   // lignes paires
    oddRowFill:    "FFFFFF",   // lignes impaires
    bodyCellSize:  20,          // 10 pt
    // ShadingType.CLEAR obligatoire pour tous les fill de cellule
  },

  // =================================================================
  // CONFIGURATION BULLETS (à passer dans new Document({ numbering: ... }))
  // =================================================================
  numbering: {
    reference: "bullets",
    levels: [
      {
        level: 0,
        format: LevelFormat.BULLET,
        text: "●",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } },
      },
      {
        level: 1,
        format: LevelFormat.BULLET,
        text: "○",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 1440, hanging: 360 } } },
      },
      {
        level: 2,
        format: LevelFormat.BULLET,
        text: "■",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 2160, hanging: 360 } } },
      },
    ],
  },

  // =================================================================
  // RÈGLES CRITIQUES (rappel pour les scripts générateurs)
  // =================================================================
  // ❌ JAMAIS \n dans les TextRun → utiliser des Paragraph séparés
  // ❌ JAMAIS WidthType.PERCENTAGE → toujours WidthType.DXA
  // ✅ ShadingType.CLEAR pour tous les fill de cellule/paragraphe
  // ✅ LevelFormat.BULLET pour les listes (jamais de caractères manuels)
  // ✅ Tailles de police en demi-points (fontSize × 2)
  // ✅ Espacements en twips (pt × 20)
};
