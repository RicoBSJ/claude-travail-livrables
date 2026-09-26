// scripts/audit-securite.js — Vérifications de sécurité du Portail Livrables
// Leçon 10 — Sécurité et données (26/09/2026)
//
// Lance : node scripts/audit-securite.js
// Ou    : npm run audit
//
// Ce script réalise 5 vérifications :
//   1. Le fichier .env n'est pas suivi par git (protection des secrets)
//   2. portail.db n'est pas suivi par git (base de cache, non versionnée)
//   3. .env.example est présent (documentation des variables configurables)
//   4. npm audit sur le projet racine (0 vulnérabilité connue attendu)
//   5. Les en-têtes de sécurité sont présents dans serveur.js

'use strict';

const path         = require('node:path');
const fs           = require('node:fs');
const { execSync } = require('node:child_process');

const PROJ    = path.join(__dirname, '..');
const GIT_ROOT = path.join(PROJ, '..', '..', '..');

// ── Helpers ────────────────────────────────────────────────────────────────

let ok = 0;
let ko = 0;

function passer(message) {
  console.log(`  ✓ ${message}`);
  ok++;
}

function echouer(message) {
  console.error(`  ✗ ${message}`);
  ko++;
}

// Retourne true si le fichier (chemin relatif depuis GIT_ROOT) est suivi par git.
function estSuiviParGit(cheminRelatif) {
  try {
    const sortie = execSync(`git ls-files "${cheminRelatif}"`, {
      cwd: GIT_ROOT,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim();
    return sortie !== '';
  } catch {
    return false;
  }
}

// ── Vérifications ──────────────────────────────────────────────────────────

console.log('\nPortail Livrables — audit de sécurité\n');

// ── 1. .env non versionné ──────────────────────────────────────────────────
console.log('1. Fichier .env');
const envPath = path.join(PROJ, '.env');
const envExiste = fs.existsSync(envPath);
const envSuivi  = estSuiviParGit('livrables/projets/appli-ia/.env');

if (envSuivi) {
  echouer('.env est suivi par git — retire-le immédiatement avec : git rm --cached .env');
} else if (!envExiste) {
  passer('.env absent (normal si PORT=3000 par défaut convient)');
} else {
  passer('.env présent mais non suivi par git — les secrets restent locaux');
}

// ── 2. portail.db non versionné ────────────────────────────────────────────
console.log('\n2. Base de cache SQLite (portail.db)');
const dbSuivi = estSuiviParGit('livrables/projets/appli-ia/portail.db');

if (dbSuivi) {
  echouer('portail.db est suivi par git — retire-le avec : git rm --cached portail.db');
} else {
  passer('portail.db non suivi par git');
}

// ── 3. .env.example présent ────────────────────────────────────────────────
console.log('\n3. Documentation (.env.example)');
const examplePath = path.join(PROJ, '.env.example');

if (fs.existsSync(examplePath)) {
  passer('.env.example présent — les variables configurables sont documentées');
} else {
  echouer('.env.example absent — crée-le pour documenter les variables attendues');
}

// ── 4. npm audit ───────────────────────────────────────────────────────────
console.log('\n4. npm audit (dépendances du projet racine)');
try {
  // npm audit --json sort en code non-zéro si des vulnérabilités sont trouvées.
  // On capture stdout dans les deux cas (exit 0 et exit non-0).
  let json = '';
  try {
    json = execSync('npm audit --json', { cwd: PROJ, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  } catch (err) {
    json = err.stdout || '{}';
  }
  const rapport = JSON.parse(json);
  const meta    = rapport.metadata || {};
  const vulns   = meta.vulnerabilities || {};
  const total   = Object.values(vulns).reduce((s, n) => s + n, 0);
  const hasCritical = (vulns.critical || 0) + (vulns.high || 0) > 0;

  if (total === 0) {
    passer(`0 vulnérabilité trouvée (${meta.totalDependencies || '?'} dépendances analysées)`);
  } else if (hasCritical) {
    echouer(`${total} vulnérabilité(s) dont ${vulns.critical || 0} critique(s) et ${vulns.high || 0} haute(s) — lance npm audit fix`);
  } else {
    passer(`${total} vulnérabilité(s) de sévérité basse/modérée — vérifie npm audit pour détails`);
  }
} catch (err) {
  echouer(`Impossible de lancer npm audit : ${err.message}`);
}

// ── 5. En-têtes de sécurité dans serveur.js ────────────────────────────────
console.log('\n5. En-têtes de sécurité HTTP (scripts/serveur.js)');
const serveurPath = path.join(PROJ, 'scripts', 'serveur.js');
const serveurCode = fs.readFileSync(serveurPath, 'utf8');

const enTetesAttendus = [
  'X-Content-Type-Options',
  'X-Frame-Options',
  'Referrer-Policy',
  'Content-Security-Policy',
];

const manquants = enTetesAttendus.filter(h => !serveurCode.includes(h));

if (manquants.length === 0) {
  passer(`4 en-têtes de sécurité présents dans serveur.js`);
} else {
  echouer(`En-tête(s) manquant(s) dans serveur.js : ${manquants.join(', ')}`);
}

// ── Bilan ──────────────────────────────────────────────────────────────────
console.log(`\n──────────────────────────────────────────`);
console.log(`Bilan : ${ok} contrôle(s) OK · ${ko} problème(s)`);
if (ko > 0) {
  console.error('Corrige les problèmes signalés avant de continuer.\n');
  process.exit(1);
} else {
  console.log('Tout est en ordre.\n');
}
