// frontend/src/filtres.ts — Logique de filtrage extraite de App.tsx
// Leçon 09 — Qualité et débogage (25/09/2026)
//
// `matcheFiltres` et `normaliser` vivent ici, et non dans App.tsx, pour deux raisons :
//   1. Testabilité : un fichier .ts pur peut être chargé par node:test — Node retire
//      les annotations de type à la volée, sans drapeau depuis v23.6.0 et v22.18.0
//      (nodejs.org/api/cli.html, table History de --no-strip-types, consultée le
//      25/09/2026 ; le drapeau --experimental-strip-types a été renommé
//      --no-strip-types en v24.12.0). Mesuré le 25/09/2026 sur v24.15.0 et v24.18.1 :
//      16 pass avec ou sans lui.
//      Corrigé le 25/09/2026 : cet en-tête faisait du drapeau la condition de la
//      testabilité. Il ne l'est pas — la vraie limite est le JSX.
//      Un fichier .tsx ne se charge pas : `node frontend/src/App.tsx` rend
//      TypeError [ERR_UNKNOWN_FILE_EXTENSION] (mesuré le 25/09/2026), et du JSX placé
//      dans un .mts ne se parse pas. Le déshabilleur de types n'est pas un
//      compilateur JSX.
//   2. Réutilisabilité : si une autre page ou un autre composant a besoin de filtrer
//      des livrables, il importe depuis ici, pas depuis App.tsx.
//
// App.tsx importe ces deux fonctions depuis ce module.

import type { Livrable } from './types'

/**
 * Normalise une chaîne pour la recherche :
 *   - Minuscules
 *   - Sans accents (décomposition NFD + suppression des diacritiques U+0300–U+036F)
 *
 * Permet de taper "lecon" pour trouver "leçon",
 * "education" pour "éducation", "bientraitance" pour "Bientraitance".
 */
export function normaliser(s: string): string {
  return s
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
}

/**
 * Teste si un livrable correspond aux trois filtres actifs.
 *
 * @param livrable  - Le livrable à tester
 * @param recherche - Texte libre (vide = pas de filtre texte)
 * @param extension - Extension exacte, point inclus (vide = pas de filtre extension)
 *
 * Les deux filtres sont cumulatifs (ET logique).
 * Le filtre texte recherche dans le nom ET le slug, après normalisation NFD.
 */
export function matcheFiltres(
  livrable: Livrable,
  recherche: string,
  extension: string
): boolean {
  // Filtre par extension (comparaison exacte — ".docx" est différent de ".DOCX")
  if (extension !== '' && livrable.extension !== extension) return false

  // Filtre par texte : on cherche dans le nom ET dans le slug normalisés
  if (recherche !== '') {
    const cible = normaliser(livrable.nom + ' ' + livrable.slug)
    if (!cible.includes(normaliser(recherche))) return false
  }

  return true
}
