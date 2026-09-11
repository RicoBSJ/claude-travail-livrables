// scripts/requetes.js — Exemples de requêtes SQL sur portail.db
// Leçon 07 — Persistance : base de données locale (11/09/2026)
//
// Lance : node scripts/requetes.js
// Requiert d'avoir lancé node scripts/indexer.js au préalable.
//
// Ce script n'écrit rien dans la base : { readonly: true } garantit
// qu'aucune modification accidentelle n'est possible.

'use strict';

const path     = require('node:path');
const Database = require('better-sqlite3');

const DB_PATH = path.join(__dirname, '..', 'portail.db');

// Ouverture en lecture seule — aucune écriture possible
const db = new Database(DB_PATH, { readonly: true });

// ── Requête 1 : total par catégorie ──────────────────────────────────────
console.log('\n📊 Total par catégorie :');
const totaux = db.prepare(`
  SELECT
    categorie,
    COUNT(*)                           AS fichiers,
    ROUND(SUM(taille) / 1024.0, 1)    AS total_ko
  FROM livrables
  GROUP BY categorie
  ORDER BY fichiers DESC
`).all();
console.table(totaux);

// ── Requête 2 : 5 livrables les plus récents (toutes catégories) ─────────
console.log('\n🕐 Les 5 livrables les plus récents :');
const recents = db.prepare(`
  SELECT
    categorie,
    nom,
    date,
    ROUND(taille / 1024.0, 1) AS taille_ko
  FROM livrables
  WHERE date IS NOT NULL
  ORDER BY date DESC
  LIMIT 5
`).all();
console.table(recents);

// ── Requête 3 : recherche textuelle sur le slug ───────────────────────────
// Modifie motCle pour chercher ce qui t'intéresse.
// Essaie 'rbpp', 'lecon-appli-ia', 'sqlite', 'serafin'…
const motCle = 'sqlite';

console.log(`\n🔍 Fichiers dont le slug contient "${motCle}" :`);
const resultats = db.prepare(`
  SELECT categorie, nom, date
  FROM livrables
  WHERE slug LIKE @motif
  ORDER BY date DESC
`).all({ motif: `%${motCle}%` });

if (resultats.length === 0) {
  console.log('  (aucun résultat)');
} else {
  console.table(resultats);
}

// ── Requête 4 : répartition par format de fichier ────────────────────────
console.log('\n📂 Répartition par format (extension) :');
const formats = db.prepare(`
  SELECT
    extension,
    COUNT(*) AS fichiers
  FROM livrables
  GROUP BY extension
  ORDER BY fichiers DESC
`).all();
console.table(formats);

// ── Challenge : à compléter (leçon 07, exercice 4) ───────────────────────
// Ajouter ici une requête qui affiche les 3 mois les plus productifs.
// Indice : substr(date, 1, 7) extrait 'YYYY-MM' d'une date texte.

db.close();
