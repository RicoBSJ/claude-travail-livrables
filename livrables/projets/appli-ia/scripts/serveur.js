// scripts/serveur.js — Serveur HTTP local du Portail Livrables
// Leçon 04 — Données réelles : l'API qui connaît vos fichiers (21/08/2026)
//
// Lance : node scripts/serveur.js
// Ou sur un autre port : PORT=8080 node scripts/serveur.js
//
// Changements leçon 04 :
//   - async/await remplace les callbacks imbriqués (fs.promises)
//   - extraireDate() et extraireSlug() extraient les métadonnées du nom de fichier
//   - Résout l'écart n°3 : date issue du NOM, pas du mtime
//   - PORT configurable via variable d'environnement
//   - Nouvelle route /api/livrables?categorie=X pour accès ciblé
//   - URL parsée avec new URL() pour accès aux query params

'use strict';
const http  = require('node:http');
const fs    = require('node:fs/promises');    // API Promise — plus de callbacks
const path  = require('node:path');
const { URL } = require('node:url');

// ── Configuration ──────────────────────────────────────────────────────────

// PORT peut être injecté par l'environnement : PORT=8080 node scripts/serveur.js
const PORT = process.env.PORT || 3000;

// Le script vit dans livrables/projets/appli-ia/scripts/
// On remonte de 4 niveaux pour atteindre la racine Claude_Travail/
const RACINE = path.resolve(__dirname, '..', '..', '..', '..');

// Catégories à inventorier : clé → { chemin absolu, extensions acceptées }
const CATEGORIES = {
  lecons:       { chemin: path.join(RACINE, 'livrables', 'lecons'),       extensions: ['.docx', '.md'] },
  quiz:         { chemin: path.join(RACINE, 'livrables', 'quiz'),         extensions: ['.pptx'] },
  infographies: { chemin: path.join(RACINE, 'livrables', 'infographies'), extensions: ['.pptx'] },
  veilles:      { chemin: path.join(RACINE, 'sources',   'veille'),       extensions: ['.docx', '.md'] },
  documents:    { chemin: path.join(RACINE, 'livrables', 'documents'),    extensions: ['.docx', '.pdf'] },
  controles:    { chemin: path.join(RACINE, 'livrables', 'controles'),    extensions: ['.md', '.docx'] },
};

// Exclusions spec v1.2
const DOCS_DE_DOSSIER = ['readme.md'];

// ── Fonctions utilitaires ──────────────────────────────────────────────────

/**
 * Extrait la date YYYY-MM-DD du nom de fichier (résout écart n°3).
 * Retourne null si le nom ne respecte pas la convention de nommage.
 *
 * Exemples :
 *   "2026-08-21_lecon-appli-ia_04_donnees.docx" → "2026-08-21"
 *   "quiz_rbpp_bientraitance.pptx"               → null
 */
function extraireDate(nom) {
  const match = nom.match(/^(\d{4}-\d{2}-\d{2})/);
  return match ? match[1] : null;
}

/**
 * Extrait le slug descriptif du nom de fichier (partie après la date).
 * Si le nom ne suit pas la convention, retourne le nom sans extension.
 *
 * Exemples :
 *   "2026-08-21_lecon-appli-ia_04_donnees.docx" → "lecon-appli-ia_04_donnees"
 *   "quiz_rbpp_bientraitance.pptx"               → "quiz_rbpp_bientraitance"
 */
function extraireSlug(nom) {
  const { name } = path.parse(nom);
  const match = name.match(/^\d{4}-\d{2}-\d{2}_(.+)$/);
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
 * Parcourt un dossier (et ses sous-dossiers si recursif=true) de façon asynchrone.
 * Retourne un tableau de livrables enrichis.
 */
async function inventorierDossier(dossierPath, extensions, recursif) {
  const livrables = [];

  let entrees;
  try {
    entrees = await fs.readdir(dossierPath, { withFileTypes: true });
  } catch {
    // Dossier inexistant ou inaccessible : on retourne un tableau vide sans planter
    return livrables;
  }

  for (const entree of entrees) {
    if (entree.isDirectory() && recursif) {
      const sous = await inventorierDossier(
        path.join(dossierPath, entree.name),
        extensions,
        true
      );
      livrables.push(...sous);
    } else if (entree.isFile() && estLivrable(entree.name, extensions)) {
      const fichierPath = path.join(dossierPath, entree.name);
      let taille = 0;
      try {
        const stats = await fs.stat(fichierPath);
        taille = stats.size;
      } catch {
        // Fichier inaccessible au moment de stat() — inclus avec taille 0
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

/**
 * Construit l'inventaire complet par catégorie.
 * Trie les livrables par date décroissante (date issue du NOM — écart n°3 résolu).
 * Les fichiers sans date (null) sont placés en fin de liste.
 */
async function construireInventaire() {
  const categories = {};
  let totalFichiers = 0;
  let totalOctets   = 0;

  for (const [cle, config] of Object.entries(CATEGORIES)) {
    const estRecursif = cle === 'veilles';
    const livrables   = await inventorierDossier(config.chemin, config.extensions, estRecursif);

    // Tri : date décroissante ; les null en fin (fichiers hors convention)
    livrables.sort((a, b) => {
      if (a.date === null && b.date === null) return 0;
      if (a.date === null) return 1;
      if (b.date === null) return -1;
      return b.date.localeCompare(a.date);
    });

    const octets   = livrables.reduce((s, l) => s + l.taille, 0);
    const taille_ko = Math.round(octets / 1024);  // conservé pour compat frontend

    categories[cle] = {
      nombre:    livrables.length,
      taille_ko,
      recents:   livrables.slice(0, 5),  // les 5 plus récents, triés par DATE du NOM
      livrables,                          // liste complète (nouvelle route)
    };

    totalFichiers += livrables.length;
    totalOctets   += octets;
  }

  return { categories, total: { fichiers: totalFichiers, octets: totalOctets } };
}

// ── Serveur HTTP ───────────────────────────────────────────────────────────

const DOSSIER_PUBLIC = path.join(__dirname, '..', 'public');

const TYPES_MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.ico':  'image/x-icon',
};

/**
 * Gestionnaire principal des requêtes HTTP — async.
 *
 * Routes :
 *   GET /api/inventaire              → inventaire complet (compat frontend leçons 1-3)
 *   GET /api/livrables?categorie=X   → liste complète d'une catégorie (nouveau leçon 04)
 *   GET /                            → public/index.html
 *   GET /style.css, /app.js, …       → fichiers statiques du dossier public/
 */
async function gererRequete(req, res) {
  // Parsing de l'URL et extraction du chemin + query params
  // La base "http://localhost" est requise pour que new URL() accepte des chemins relatifs.
  const urlParsee  = new URL(req.url, 'http://localhost');
  const chemin     = urlParsee.pathname;

  // ── Route : inventaire complet ─────────────────────────────────────────
  if (chemin === '/api/inventaire') {
    const { categories } = await construireInventaire();
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    // On expose uniquement les clés utilisées par le frontend (compat leçons 1-3)
    const reponse = {};
    for (const [cle, cat] of Object.entries(categories)) {
      reponse[cle] = { nombre: cat.nombre, taille_ko: cat.taille_ko, recents: cat.recents };
    }
    res.end(JSON.stringify(reponse, null, 2));
    return;
  }

  // ── Route : livrables d'une catégorie ─────────────────────────────────
  if (chemin === '/api/livrables') {
    const categorie = urlParsee.searchParams.get('categorie');
    if (!categorie || !CATEGORIES[categorie]) {
      const valeurs = Object.keys(CATEGORIES).join(', ');
      res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({
        erreur: `Catégorie inconnue ou absente. Valeurs acceptées : ${valeurs}`,
      }));
      return;
    }
    const config     = CATEGORIES[categorie];
    const estRecursif = categorie === 'veilles';
    const livrables  = await inventorierDossier(config.chemin, config.extensions, estRecursif);
    livrables.sort((a, b) => {
      if (a.date === null && b.date === null) return 0;
      if (a.date === null) return 1;
      if (b.date === null) return -1;
      return b.date.localeCompare(a.date);
    });
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ categorie, nombre: livrables.length, livrables }, null, 2));
    return;
  }

  // ── Fichiers statiques ─────────────────────────────────────────────────
  const cible     = chemin === '/' ? '/index.html' : chemin;
  const absolu    = path.resolve(DOSSIER_PUBLIC, '.' + cible);

  // Garde-fou path traversal : le chemin résolu doit rester dans DOSSIER_PUBLIC
  if (!absolu.startsWith(DOSSIER_PUBLIC + path.sep) && absolu !== DOSSIER_PUBLIC) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('403 — Accès interdit');
    return;
  }

  const ext  = path.extname(absolu).toLowerCase();
  const mime = TYPES_MIME[ext] || 'application/octet-stream';

  try {
    const contenu = await fs.readFile(absolu);
    res.writeHead(200, { 'Content-Type': mime });
    res.end(contenu);
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 — Page introuvable');
  }
}

// ── Démarrage ──────────────────────────────────────────────────────────────

const serveur = http.createServer((req, res) => {
  // gererRequete est async → elle retourne une Promise.
  // Si cette Promise rejette (erreur non gérée), on l'attrape ici.
  gererRequete(req, res).catch(err => {
    console.error('Erreur non gérée :', err.message);
    if (!res.headersSent) {
      res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify({ erreur: 'Erreur interne du serveur' }));
    }
  });
});

serveur.listen(PORT, () => {
  console.log(`Portail Livrables démarré → http://localhost:${PORT}`);
  console.log(`  Inventaire  : http://localhost:${PORT}/api/inventaire`);
  console.log(`  Par catég.  : http://localhost:${PORT}/api/livrables?categorie=lecons`);
  console.log('Ctrl+C pour arrêter.');
});
