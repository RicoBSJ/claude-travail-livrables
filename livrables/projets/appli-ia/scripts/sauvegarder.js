// scripts/sauvegarder.js — Sauvegarde du code source du Portail Livrables
// Leçon 11 — Mise en production (27/09/2026)
//
// Ce script crée un instantané horodaté du code source dans sauvegardes/YYYY-MM-DD_HH-MM-SS/.
//
// Ce qu'on sauvegarde (code source et configuration) :
//   - Racine  : package.json, tsconfig.json, .gitignore, .env.example, SPEC.md
//   - scripts/        (tous les fichiers .js et .mts)
//   - src/            (TypeScript — types et inventaire)
//   - frontend/src/   (React/TypeScript)
//   - frontend/package.json, frontend/tsconfig.json, frontend/vite.config.js, frontend/index.html
//
// Ce qu'on ne sauvegarde PAS (régénérable) :
//   - node_modules/, frontend/node_modules/  → npm install
//   - frontend/dist/                         → cd frontend && npm run build
//   - portail.db, portail.db-shm, portail.db-wal  → node scripts/indexer.js
//   - dist/                                  → npm run build (tsc)
//
// Lance : node scripts/sauvegarder.js
// Ou   : npm run sauvegarder

'use strict';

const fs   = require('node:fs/promises');
const path = require('node:path');

// ── Configuration ──────────────────────────────────────────────────────────

const RACINE_PROJET = path.join(__dirname, '..');
const DOSSIER_SAUVEGARDES = path.join(RACINE_PROJET, 'sauvegardes');

// Horodatage : YYYY-MM-DD_HH-MM-SS (format compatible avec tous les systèmes de fichiers)
function horodatage() {
  const d = new Date();
  const p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}` +
         `_${p(d.getHours())}-${p(d.getMinutes())}-${p(d.getSeconds())}`;
}

// Éléments à copier : { src: chemin relatif à RACINE_PROJET, dest: sous-chemin dans la sauvegarde }
// Pour les fichiers : dest peut être omis (reprend src).
// Pour les dossiers : fs.cp avec recursive:true copie le contenu entier.
const ELEMENTS = [
  // Fichiers racine
  { src: 'package.json',  type: 'fichier' },
  { src: 'tsconfig.json', type: 'fichier' },
  { src: '.gitignore',    type: 'fichier' },
  { src: '.env.example',  type: 'fichier' },
  { src: 'SPEC.md',       type: 'fichier' },
  // Code source
  { src: 'scripts',       type: 'dossier' },
  { src: 'src',           type: 'dossier' },
  // Frontend (source seulement, pas dist ni node_modules)
  { src: path.join('frontend', 'package.json'),  type: 'fichier' },
  { src: path.join('frontend', 'tsconfig.json'), type: 'fichier' },
  { src: path.join('frontend', 'vite.config.js'), type: 'fichier' },
  { src: path.join('frontend', 'index.html'),    type: 'fichier' },
  { src: path.join('frontend', 'src'),           type: 'dossier' },
];

// ── Copie récursive ─────────────────────────────────────────────────────────

/**
 * Copie un fichier ou un dossier dans la destination.
 * fs.promises.cp (stable depuis Node.js v22.3.0, disponible ici v24.15.0) copie
 * récursivement les dossiers sans avoir à les parcourir manuellement.
 */
async function copier(src, dest) {
  const srcAbs  = path.join(RACINE_PROJET, src);
  const destAbs = path.join(dest, src);

  // Crée les dossiers parents si nécessaire
  await fs.mkdir(path.dirname(destAbs), { recursive: true });

  const stat = await fs.stat(srcAbs).catch(() => null);
  if (!stat) {
    console.log(`  ⚠️  Introuvable (ignoré) : ${src}`);
    return 0;
  }

  if (stat.isDirectory()) {
    await fs.cp(srcAbs, destAbs, { recursive: true });
  } else {
    await fs.copyFile(srcAbs, destAbs);
  }

  return stat.size;
}

// ── Point d'entrée ─────────────────────────────────────────────────────────

async function main() {
  const ts   = horodatage();
  const dest = path.join(DOSSIER_SAUVEGARDES, ts);

  console.log(`Portail Livrables — Sauvegarde du code source`);
  console.log(`Destination : ${dest}`);
  console.log('');

  await fs.mkdir(dest, { recursive: true });

  let totalOctets = 0;
  let totalElements = 0;

  for (const el of ELEMENTS) {
    process.stdout.write(`  Copie : ${el.src} … `);
    try {
      const octets = await copier(el.src, dest);
      totalOctets += octets;
      totalElements++;
      console.log(`✓`);
    } catch (err) {
      console.log(`✗ (${err.message})`);
    }
  }

  console.log('');
  console.log(`✓ Sauvegarde terminée : ${totalElements} élément(s) — ${Math.round(totalOctets / 1024)} Ko copiés`);
  console.log(`  Dossier : ${dest}`);
  console.log('');
  console.log('Pour restaurer : copiez les fichiers du dossier de sauvegarde à leur emplacement d\'origine.');
  console.log('Pour reconstruire depuis la sauvegarde :');
  console.log('  npm install');
  console.log('  cd frontend && npm install && npm run build && cd ..');
  console.log('  node scripts/indexer.js');
  console.log('  node scripts/serveur.js');
}

main().catch(err => {
  console.error('Erreur lors de la sauvegarde :', err.message);
  process.exit(1);
});
