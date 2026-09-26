// scripts/indexer.js — Indexation des livrables dans SQLite
// Leçon 07 — Persistance : base de données locale (11/09/2026)
// Leçon 08 — Factorisation : CATEGORIES et utilitaires déplacés dans utils.js (18/09/2026)
//            Fix extraireDate() : gère maintenant la date en fin de nom (quiz, infographies)
// Leçon 10 — Sécurité et données (26/09/2026) : colonne slug_normalise pour recherche accentuée
//
// Lance     : node scripts/indexer.js
// Ou        : npm run indexer
//
// Ce script scanne les 6 catégories de livrables et les insère dans portail.db.
// À relancer après chaque job automatisé pour mettre à jour l'index.
//
// Note : la bibliothèque better-sqlite3 est synchrone.
//   .all(), .run(), .get() retournent directement leurs résultats — pas de await.
//   Ce choix est délibéré : SQLite sérialise ses accès, une API async n'apporterait
//   pas de vraie concurrence et ajouterait juste de l'overhead de thread.

'use strict';

const path     = require('node:path');
const fs       = require('node:fs');
const Database = require('better-sqlite3');

// Utilitaires et configuration partagés — factorisation leçon 08
const { CATEGORIES, DOCS_DE_DOSSIER,
        extraireDate, extraireSlug, estLivrable, normaliserSlug } = require('./utils');

// La base SQLite est créée au même niveau que PROJET.md (racine du projet)
const DB_PATH = path.join(__dirname, '..', 'portail.db');

/**
 * Version SYNCHRONE de l'inventaire — adaptée à l'API synchrone de better-sqlite3.
 * fs.readdirSync / fs.statSync : bloquants, mais exécutés une seule fois au lancement.
 */
function inventorierSync(dossierPath, extensions, recursif) {
  const livrables = [];
  let entrees;
  try {
    entrees = fs.readdirSync(dossierPath, { withFileTypes: true });
  } catch {
    // Dossier inexistant ou inaccessible — tableau vide, pas d'erreur fatale
    return livrables;
  }

  for (const entree of entrees) {
    if (entree.isDirectory() && recursif) {
      livrables.push(...inventorierSync(
        path.join(dossierPath, entree.name),
        extensions,
        true
      ));
    } else if (entree.isFile() && estLivrable(entree.name, extensions)) {
      const fichierPath = path.join(dossierPath, entree.name);
      let taille = 0;
      try {
        taille = fs.statSync(fichierPath).size;
      } catch {
        // Fichier inaccessible au moment de statSync() — inclus avec taille 0
      }
      livrables.push({
        nom:       entree.name,
        date:      extraireDate(entree.name),   // null si hors convention
        slug:      extraireSlug(entree.name),
        taille,
        extension: path.extname(entree.name).toLowerCase(),
      });
    }
  }
  return livrables;
}

// ── Création du schéma ─────────────────────────────────────────────────────

/**
 * Crée la table livrables et ses index.
 * DROP TABLE IF EXISTS : re-indexation complète à chaque lancement.
 * Acceptable pour une base de cache — ne jamais appliquer ce pattern
 * à une table qui contient des données saisies manuellement.
 */
function creerSchema(db) {
  db.exec(`
    DROP TABLE IF EXISTS livrables;

    CREATE TABLE livrables (
      id              INTEGER PRIMARY KEY AUTOINCREMENT,
      categorie       TEXT    NOT NULL,
      nom             TEXT    NOT NULL,
      date            TEXT,              -- NULL si hors convention YYYY-MM-DD_
      slug            TEXT    NOT NULL,
      slug_normalise  TEXT    NOT NULL,  -- leçon 10 : accents et casse supprimés pour LIKE
      taille          INTEGER NOT NULL DEFAULT 0,
      extension       TEXT    NOT NULL,
      indexe_le       TEXT    NOT NULL   -- horodatage ISO de l'indexation
    );

    -- Index 1 : accélère les requêtes "livrables récents par catégorie"
    CREATE INDEX idx_categorie_date ON livrables(categorie, date DESC);

    -- Index 2 : accélère le filtre par format de fichier
    CREATE INDEX idx_extension ON livrables(extension);
  `);
}

// ── Indexation principale ──────────────────────────────────────────────────

function indexer() {
  const db = new Database(DB_PATH);

  // Mode WAL (Write-Ahead Logging) : meilleures performances en écriture séquentielle.
  // Le pragma s'applique au niveau de la connexion, pas de la transaction.
  db.pragma('journal_mode = WAL');

  console.log('📦 Création du schéma…');
  creerSchema(db);

  // Horodatage de l'indexation — le même pour toutes les lignes de cette session
  const maintenant = new Date().toISOString();

  // Instruction préparée : SQLite la compile une fois, on l'exécute N fois.
  // Les paramètres nommés (@nom) évitent les injections SQL et améliorent la lisibilité.
  const inserer = db.prepare(`
    INSERT INTO livrables (categorie, nom, date, slug, slug_normalise, taille, extension, indexe_le)
    VALUES (@categorie, @nom, @date, @slug, @slug_normalise, @taille, @extension, @indexe_le)
  `);

  // Transaction : toutes les insertions d'une catégorie en un seul commit.
  // Sans transaction : N INSERT = N commits = N écritures disque.
  // Avec transaction : N INSERT + 1 commit = 1 écriture disque.
  const insererTout = db.transaction((rangees) => {
    for (const rangee of rangees) {
      inserer.run(rangee);
    }
  });

  let totalInsere = 0;

  for (const [cle, config] of Object.entries(CATEGORIES)) {
    const livrables   = inventorierSync(config.chemin, config.extensions, config.recursif);

    const rangees = livrables.map(l => ({
      categorie:      cle,
      nom:            l.nom,
      date:           l.date,                  // peut être null → SQLite stocke NULL
      slug:           l.slug,
      slug_normalise: normaliserSlug(l.slug),  // leçon 10 : pour recherche insensible aux accents
      taille:         l.taille,
      extension:      l.extension,
      indexe_le:      maintenant,
    }));

    insererTout(rangees);
    totalInsere += rangees.length;
    console.log(`  ✓ ${cle} — ${rangees.length} fichier(s)`);
  }

  console.log(`\n✅ Indexation terminée — ${totalInsere} fichier(s) dans ${DB_PATH}`);
  db.close();
}

// ── Point d'entrée ─────────────────────────────────────────────────────────

indexer();
