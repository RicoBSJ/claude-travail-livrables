// scripts/tests.js — Tests automatisés pour les utilitaires serveur
// Leçon 09 — Qualité et débogage (25/09/2026)
//
// Lance avec : node scripts/tests.js
//  ou       : npm test  (exécute les deux fichiers de tests)
//
// Utilise node:test (intégré, stable depuis Node.js v22+, testé sur v24.15.0 le 25/09/2026).
// Aucune bibliothèque externe n'est nécessaire.

'use strict';

const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const { extraireDate, extraireSlug, estLivrable } = require('./utils');

// ── extraireDate ──────────────────────────────────────────────────────────────
// Cette fonction a deux conventions à gérer. Chaque cas ci-dessous correspond
// à un type de fichier réel dans le dépôt.

describe('extraireDate', () => {

  // Convention 1 : date en tête (leçons, veilles, documents, contrôles)
  test('convention 1 — leçon avec numéro', (t) => {
    assert.strictEqual(
      extraireDate('2026-09-18_lecon-appli-ia_08_api-architecture-contrats.docx'),
      '2026-09-18'
    );
  });

  test('convention 1 — veille HAS', (t) => {
    assert.strictEqual(
      extraireDate('2026-09-02_veille_HAS.docx'),
      '2026-09-02'
    );
  });

  test('convention 1 — note de contrôle hebdomadaire', (t) => {
    assert.strictEqual(
      extraireDate('2026-09-19_controle-livrables.md'),
      '2026-09-19'
    );
  });

  // Convention 2 : date en fin (quiz, infographies)
  test('convention 2 — quiz PPTX', (t) => {
    assert.strictEqual(
      extraireDate('quiz_rbpp_bientraitance_2026-04-06.pptx'),
      '2026-04-06'
    );
  });

  test('convention 2 — infographie PPTX', (t) => {
    assert.strictEqual(
      extraireDate('infographie_rbpp_tsa-enfant-adolescent_2026-02-12.pptx'),
      '2026-02-12'
    );
  });

  // Fichiers sans date
  test('pas de date — readme.md', (t) => {
    assert.strictEqual(extraireDate('readme.md'), null);
  });

  test('pas de date — fichier sans convention', (t) => {
    assert.strictEqual(extraireDate('Ancien document.docx'), null);
  });

  // Cas limite documenté : double extension .fiche.md
  // path.parse().name retourne "veille-essms-2026-05-20-2026-05-26.fiche"
  // L'ancre $ tombe sur ".fiche", pas sur une date. Comportement attendu : null.
  // Documenté dans PROJET.md le 18/09/2026.
  test('cas limite — double extension (.fiche.md) → null attendu', (t) => {
    assert.strictEqual(
      extraireDate('veille-essms-2026-05-20-2026-05-26.fiche.md'),
      null
    );
  });
});

// ── extraireSlug ──────────────────────────────────────────────────────────────

describe('extraireSlug', () => {

  test('convention 1 — tout ce qui suit la date', (t) => {
    assert.strictEqual(
      extraireSlug('2026-09-18_lecon-appli-ia_08_api-architecture-contrats.docx'),
      'lecon-appli-ia_08_api-architecture-contrats'
    );
  });

  test('convention 2 — tout ce qui précède la date', (t) => {
    assert.strictEqual(
      extraireSlug('quiz_rbpp_bientraitance_2026-04-06.pptx'),
      'quiz_rbpp_bientraitance'
    );
  });

  test('hors convention — nom complet sans extension', (t) => {
    // Si aucune date n'est détectée, le nom entier (sans extension) est le slug.
    assert.strictEqual(
      extraireSlug('Ancien document.docx'),
      'Ancien document'
    );
  });
});

// ── estLivrable ───────────────────────────────────────────────────────────────

describe('estLivrable', () => {

  test('exclut les verrous Office (~$)', (t) => {
    assert.strictEqual(estLivrable('~$document en cours.docx', ['.docx']), false);
  });

  test('exclut readme.md (insensible à la casse)', (t) => {
    assert.strictEqual(estLivrable('README.md', ['.docx', '.md']), false);
    assert.strictEqual(estLivrable('readme.md', ['.docx', '.md']), false);
  });

  test('accepte un fichier .docx valide', (t) => {
    assert.strictEqual(
      estLivrable('2026-09-18_lecon-appli-ia_08.docx', ['.docx']),
      true
    );
  });

  test('accepte un fichier .pptx valide', (t) => {
    assert.strictEqual(
      estLivrable('quiz_rbpp_bientraitance_2026-04-06.pptx', ['.pptx']),
      true
    );
  });

  test('rejette une extension non listée', (t) => {
    // Un script .js dans le même dossier ne doit pas apparaître dans l'inventaire.
    assert.strictEqual(estLivrable('script.js', ['.docx', '.md']), false);
  });

  test('rejette une extension valide mais non autorisée pour cette catégorie', (t) => {
    // Un .md dans la catégorie quiz (qui n'accepte que .pptx) est exclu.
    assert.strictEqual(estLivrable('note.md', ['.pptx']), false);
  });
});
