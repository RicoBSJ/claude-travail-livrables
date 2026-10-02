// scripts/maintenance.js — Bilan de santé hebdomadaire du Portail Livrables
// Leçon 12 — Maintenance et évolution (02/10/2026)
//
// Lance : node scripts/maintenance.js
// Ou   : npm run maintenance
//
// Enchaîne 4 vérifications dans l'ordre :
//   1. Tests automatisés (npm test)
//   2. Audit de sécurité (node scripts/audit-securite.js)
//   3. Dépendances obsolètes (npm outdated)
//   4. Dernière sauvegarde (sauvegardes/)
//
// Code de sortie :
//   0 — tout est en ordre
//   1 — au moins un problème détecté

'use strict';

const path        = require('node:path');
const fs          = require('node:fs');
const { spawnSync } = require('node:child_process');

const PROJ = path.join(__dirname, '..');

// ── Helpers ────────────────────────────────────────────────────────────────

let ok = 0;
let ko = 0;

function passer(titre) { console.log(`  ✓ ${titre}`); ok++; }
function echouer(titre) { console.error(`  ✗ ${titre}`); ko++; }

// Exécute une commande et retourne { code, stdout, stderr }.
// spawnSync prend commande + tableau d'arguments séparément : le shell n'interprète
// jamais les arguments, ce qui évite les injections de commande si l'on passe
// des valeurs variables. execSync prend une chaîne que le shell analyse d'abord.
function lancer(commande, args, options) {
  const resultat = spawnSync(commande, args, Object.assign({
    encoding: 'utf8',
    cwd: PROJ,
    stdio: 'pipe',
  }, options));
  return {
    code:   resultat.status !== null ? resultat.status : 1,
    stdout: (resultat.stdout || '').trim(),
    stderr: (resultat.stderr || '').trim(),
  };
}

// ── Vérifications ──────────────────────────────────────────────────────────

console.log('\nPortail Livrables — bilan de santé\n');

// ── 1. Tests ───────────────────────────────────────────────────────────────
console.log('1. Tests automatisés');
const tests = lancer('npm', ['test']);
if (tests.code === 0) {
  // Extrait les compteurs "ℹ pass N" et "ℹ fail N" de la sortie de node:test
  const sortie     = tests.stdout + tests.stderr;
  const passeTotal = (sortie.match(/ℹ pass (\d+)/g) || [])
    .reduce((s, m) => s + parseInt(m.replace('ℹ pass ', ''), 10), 0);
  const echecTotal = (sortie.match(/ℹ fail (\d+)/g) || [])
    .reduce((s, m) => s + parseInt(m.replace('ℹ fail ', ''), 10), 0);
  passer(`${passeTotal} tests · ${echecTotal} échec(s)`);
} else {
  echouer('Les tests échouent — relis la sortie de npm test');
  console.error(tests.stderr.slice(-500));
}

// ── 2. Audit de sécurité ───────────────────────────────────────────────────
console.log('\n2. Audit de sécurité');
const audit = lancer('node', ['scripts/audit-securite.js']);
if (audit.code === 0) {
  passer('5/5 contrôles passés');
} else {
  echouer('Des contrôles de sécurité ont échoué — relis node scripts/audit-securite.js');
}

// ── 3. Dépendances obsolètes ───────────────────────────────────────────────
console.log('\n3. Dépendances obsolètes');

// npm outdated sort en code 1 s'il trouve des packages obsolètes, 0 sinon.
// On capture les deux cas (code 0 ou 1) sans lever d'exception.
function compterOutdated(repertoire) {
  const r = lancer('npm', ['outdated'], { cwd: repertoire });
  // La première ligne du tableau est l'en-tête ; on ne compte que les lignes de données
  const lignes = r.stdout.split('\n').filter(function (l) {
    return l.trim() && !l.startsWith('Package');
  });
  return lignes.length;
}

const nbRacine   = compterOutdated(PROJ);
const nbFrontend = compterOutdated(path.join(PROJ, 'frontend'));
const totalOut   = nbRacine + nbFrontend;

if (totalOut === 0) {
  passer('Toutes les dépendances sont à jour');
} else {
  echouer(totalOut + ' dépendance(s) obsolète(s)');
  if (nbRacine)   console.log('  Racine   : ' + nbRacine   + ' paquet(s) — lance npm outdated');
  if (nbFrontend) console.log('  Frontend : ' + nbFrontend + ' paquet(s) — lance cd frontend && npm outdated');
}

// ── 4. Dernière sauvegarde ─────────────────────────────────────────────────
console.log('\n4. Dernière sauvegarde');
const dossierSauv = path.join(PROJ, 'sauvegardes');

if (!fs.existsSync(dossierSauv)) {
  echouer('Aucune sauvegarde trouvée — lance npm run sauvegarder');
} else {
  const entrees = fs.readdirSync(dossierSauv)
    .filter(function (n) { return n.match(/^\d{4}-\d{2}-\d{2}_/); })
    .sort()
    .reverse();

  if (entrees.length === 0) {
    echouer('Dossier sauvegardes/ vide — lance npm run sauvegarder');
  } else {
    const derniere  = entrees[0];
    const dateStr   = derniere.slice(0, 10);        // "YYYY-MM-DD"
    const aujStr    = new Date().toISOString().slice(0, 10);
    const diffJours = Math.round(
      (new Date(aujStr) - new Date(dateStr)) / (1000 * 60 * 60 * 24)
    );
    if (diffJours === 0) {
      passer('Sauvegarde du jour (' + derniere + ')');
    } else if (diffJours <= 7) {
      passer('Dernière sauvegarde il y a ' + diffJours + ' jour(s) (' + derniere + ')');
    } else {
      echouer('Dernière sauvegarde il y a ' + diffJours + ' jour(s) (' + derniere + ') — lance npm run sauvegarder');
    }
  }
}

// ── Résumé ─────────────────────────────────────────────────────────────────
console.log('\n──────────────────────────────────────────');
console.log('Bilan : ' + ok + ' OK · ' + ko + ' point(s) à traiter');
if (ko > 0) {
  console.error('Règle les points signalés pour maintenir le portail en bonne santé.\n');
  process.exit(1);
} else {
  console.log('Le portail est en bonne santé.\n');
}
