// scripts/tests-filtres.mts — Tests pour la logique de filtrage frontend
// Leçon 09 — Qualité et débogage (25/09/2026)
//
// Lance avec : node --experimental-strip-types --test scripts/tests-filtres.mts
//  ou       : npm test  (script npm qui combine les deux suites)
//
// Extension .mts (TypeScript ESModule) : force Node.js à traiter ce fichier
// comme un module ES, ce qui permet d'utiliser `import` au lieu de `require`.
// L'extension .mts est reconnue par Node.js v24+ via --experimental-strip-types.
// Testé le 25/09/2026 sur Node.js v24.15.0.
//
// POURQUOI .mts ET PAS .ts ?
// Le package.json du projet ne déclare pas "type":"module" : tous les .js/.ts
// sont traités comme CommonJS. Un fichier .ts avec `import` échoue donc avec
// "Cannot use import statement outside a module".
// L'extension .mts (ou .mjs pour JavaScript) signale explicitement "ce fichier
// est un module ES" — quel que soit le package.json parent.
//
// POURQUOI NE PAS AJOUTER "type":"module" AU package.json ?
// Cela casserait tous les scripts/*.js existants qui utilisent `require()`.
// Le choix .mts est chirurgical : seul ce fichier change de système.

import { test, describe } from 'node:test'
import assert from 'node:assert/strict'
import { matcheFiltres, normaliser } from '../frontend/src/filtres.ts'
import type { Livrable } from '../frontend/src/types.ts'

// Livrables de test représentatifs du dépôt réel
const LECON: Livrable = {
  nom: '2026-09-25_lecon-appli-ia_09_qualite-tests-debogage.docx',
  extension: '.docx',
  slug: 'lecon-appli-ia_09_qualite-tests-debogage',
  date: '2026-09-25',
  taille: 45000
}

const QUIZ: Livrable = {
  nom: 'quiz_rbpp_bientraitance_2026-04-06.pptx',
  extension: '.pptx',
  slug: 'quiz_rbpp_bientraitance',
  date: '2026-04-06',
  taille: 1200000
}

// ── normaliser ────────────────────────────────────────────────────────────────

describe('normaliser', () => {

  test('met en minuscules', () => {
    assert.strictEqual(normaliser('LECON'), 'lecon')
    assert.strictEqual(normaliser('Bientraitance'), 'bientraitance')
  })

  test('supprime les diacritiques', () => {
    assert.strictEqual(normaliser('leçon'), 'lecon')
    assert.strictEqual(normaliser('éducation'), 'education')
    assert.strictEqual(normaliser('bientraitance'), 'bientraitance') // inchangé
  })

  test('combine minuscules et accents', () => {
    assert.strictEqual(normaliser('Leçon'), 'lecon')
  })

  test('chaîne vide reste vide', () => {
    assert.strictEqual(normaliser(''), '')
  })
})

// ── matcheFiltres ─────────────────────────────────────────────────────────────

describe('matcheFiltres', () => {

  // Sans filtre, tout passe
  test('sans filtre — accepte tout livrable', () => {
    assert.strictEqual(matcheFiltres(LECON, '', ''), true)
    assert.strictEqual(matcheFiltres(QUIZ, '', ''), true)
  })

  // Filtre par extension
  test('filtre extension — correspondance exacte', () => {
    assert.strictEqual(matcheFiltres(LECON, '', '.docx'), true)
    assert.strictEqual(matcheFiltres(QUIZ, '', '.pptx'), true)
  })

  test('filtre extension — pas de correspondance', () => {
    assert.strictEqual(matcheFiltres(LECON, '', '.pptx'), false)
    assert.strictEqual(matcheFiltres(QUIZ, '', '.docx'), false)
  })

  test('filtre extension vide — désactivé', () => {
    assert.strictEqual(matcheFiltres(LECON, '', ''), true)
  })

  // Filtre par texte
  test('filtre texte — correspondance dans le nom', () => {
    assert.strictEqual(matcheFiltres(LECON, 'lecon', ''), true)
    assert.strictEqual(matcheFiltres(QUIZ, 'bientraitance', ''), true)
  })

  test('filtre texte — correspondance dans le slug', () => {
    // 'tests' figure dans le slug de la leçon
    assert.strictEqual(matcheFiltres(LECON, 'tests', ''), true)
  })

  test('filtre texte — insensible aux accents (NFD)', () => {
    // "leçon" normalisé = "lecon", qui est dans le nom
    assert.strictEqual(matcheFiltres(LECON, 'leçon', ''), true)
  })

  test('filtre texte — insensible à la casse', () => {
    assert.strictEqual(matcheFiltres(LECON, 'LECON', ''), true)
    assert.strictEqual(matcheFiltres(QUIZ, 'Bientraitance', ''), true)
  })

  test('filtre texte — pas de correspondance', () => {
    assert.strictEqual(matcheFiltres(LECON, 'psychopathologie', ''), false)
    assert.strictEqual(matcheFiltres(QUIZ, 'stoicisme', ''), false)
  })

  // Filtres combinés (ET logique)
  test('filtres combinés — les deux correspondent', () => {
    assert.strictEqual(matcheFiltres(LECON, 'lecon', '.docx'), true)
  })

  test('filtres combinés — texte correspond mais extension non', () => {
    assert.strictEqual(matcheFiltres(LECON, 'lecon', '.pptx'), false)
  })

  test('filtres combinés — extension correspond mais texte non', () => {
    assert.strictEqual(matcheFiltres(LECON, 'psychopathologie', '.docx'), false)
  })
})
