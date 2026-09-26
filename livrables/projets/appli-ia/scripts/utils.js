// scripts/utils.js — Utilitaires et configuration partagés du Portail Livrables
// Leçon 08 — API et architecture (18/09/2026)
// Leçon 10 — Sécurité et données (26/09/2026) : ajout de normaliserSlug
//
// Ce module extrait le code qui était dupliqué entre scripts/serveur.js
// et scripts/indexer.js : mêmes constantes CATEGORIES et DOCS_DE_DOSSIER,
// mêmes fonctions extraireDate, extraireSlug, estLivrable.
//
// Principe CommonJS : require('./utils') est mis en cache après le premier appel.
// Tous les fichiers qui l'importent partagent la même instance — pas de copie.
// Si l'on ajoute une 7e catégorie ici, serveur.js et indexer.js en profitent
// automatiquement sans qu'on touche à leurs fichiers.
//
// Usage :
//   const { RACINE, CATEGORIES, DOCS_DE_DOSSIER,
//           extraireDate, extraireSlug, estLivrable } = require('./utils');

'use strict';

const path = require('node:path');

// ── Configuration ─────────────────────────────────────────────────────────────

// Le script vit dans livrables/projets/appli-ia/scripts/
// On remonte de 4 niveaux pour atteindre la racine Claude_Travail/
const RACINE = path.resolve(__dirname, '..', '..', '..', '..');

// Catégories à inventorier : clé → { chemin absolu, extensions acceptées }
// `recursif` : la catégorie déclare elle-même si ses sous-dossiers comptent (23/09/2026).
// Avant, l'appelant testait `cle === 'veilles'` en dur, à quatre endroits — le jour où
// livrables/lecons/ a été rangé par parcours, le portail aurait affiché zéro leçon.
const CATEGORIES = {
  lecons:       { chemin: path.join(RACINE, 'livrables', 'lecons'),       extensions: ['.docx', '.md'], recursif: true },
  quiz:         { chemin: path.join(RACINE, 'livrables', 'quiz'),         extensions: ['.pptx'], recursif: false },
  infographies: { chemin: path.join(RACINE, 'livrables', 'infographies'), extensions: ['.pptx'], recursif: false },
  veilles:      { chemin: path.join(RACINE, 'sources',   'veille'),       extensions: ['.docx', '.md'], recursif: true },
  documents:    { chemin: path.join(RACINE, 'livrables', 'documents'),    extensions: ['.docx', '.pdf'], recursif: false },
  controles:    { chemin: path.join(RACINE, 'livrables', 'controles'),    extensions: ['.md', '.docx'], recursif: false },
};

// Fichiers à exclure quel que soit leur dossier (spec v1.2)
const DOCS_DE_DOSSIER = ['readme.md'];

// ── Fonctions utilitaires ─────────────────────────────────────────────────────

/**
 * Extrait la date YYYY-MM-DD du nom de fichier.
 * Gère deux conventions de nommage :
 *
 *   Convention 1 — date en tête (leçons, veilles, documents, contrôles)
 *     Exemple : "2026-09-18_lecon-appli-ia_08_api.docx" → "2026-09-18"
 *
 *   Convention 2 — date en fin (quiz, infographies)
 *     Exemple : "quiz_rbpp_bientraitance_2026-04-06.pptx" → "2026-04-06"
 *
 * Retourne null si aucune date YYYY-MM-DD n'est trouvée.
 *
 * Note : path.parse(nom).name retire l'extension avant d'appliquer le regex,
 * ce qui est nécessaire pour la convention 2 : sans ça, ".pptx" serait
 * après la date et l'ancre $ ne trouverait rien.
 */
function extraireDate(nom) {
  const { name } = path.parse(nom);
  // Convention 1 : date en tête
  let match = name.match(/^(\d{4}-\d{2}-\d{2})/);
  if (match) return match[1];
  // Convention 2 : date en fin
  match = name.match(/(\d{4}-\d{2}-\d{2})$/);
  return match ? match[1] : null;
}

/**
 * Extrait le slug descriptif du nom de fichier (partie descriptive sans la date).
 * Si le nom ne suit aucune convention, retourne le nom sans extension.
 *
 * Exemples :
 *   "2026-08-21_lecon-appli-ia_04_donnees.docx" → "lecon-appli-ia_04_donnees"
 *   "quiz_rbpp_bientraitance_2026-04-06.pptx"   → "quiz_rbpp_bientraitance"
 *   "Quiz Autodetermination.pptx"               → "Quiz Autodetermination"
 */
function extraireSlug(nom) {
  const { name } = path.parse(nom);
  // Convention 1 : date en préfixe
  let match = name.match(/^\d{4}-\d{2}-\d{2}_(.+)$/);
  if (match) return match[1];
  // Convention 2 : date en suffixe
  match = name.match(/^(.+)_\d{4}-\d{2}-\d{2}$/);
  return match ? match[1] : name;
}

/**
 * Retourne true si le fichier est un livrable réel.
 *   - Exclut les verrous Office (~$…)
 *   - Exclut les docs de dossier (readme.md)
 *   - Filtre sur les extensions autorisées par catégorie
 */
function estLivrable(nom, extensions) {
  if (nom.startsWith('~$')) return false;
  if (DOCS_DE_DOSSIER.includes(nom.toLowerCase())) return false;
  return extensions.includes(path.extname(nom).toLowerCase());
}

/**
 * Normalise une chaîne pour la recherche insensible aux accents et à la casse.
 * Miroir exact de normaliser() dans frontend/src/filtres.ts :
 *   - Minuscules
 *   - Décomposition NFD puis suppression des diacritiques U+0300–U+036F
 *
 * Stocké dans portail.db (colonne slug_normalise) pour que LIKE devienne insensible
 * aux accents : LIKE '%lecon%' trouve les slugs contenant 'leçon'.
 *
 * Exemples :
 *   "leçon-appli-ia_08_api" → "lecon-appli-ia_08_api"
 *   "bientraitance-RBPP"    → "bientraitance-rbpp"
 *   "Évaluation HAS"        → "evaluation has"
 */
function normaliserSlug(s) {
  return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

module.exports = { RACINE, CATEGORIES, DOCS_DE_DOSSIER, extraireDate, extraireSlug, estLivrable, normaliserSlug };
