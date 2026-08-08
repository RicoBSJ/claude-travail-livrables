// lister_fichiers.js — Liste les fichiers d'un dossier
//
// Usage :
//   node lister_fichiers.js                 → liste le dossier courant
//   node lister_fichiers.js /chemin/dossier → liste le dossier indiqué
//
// Lecture seule : ce script n'écrit, ne renomme ni ne supprime rien.

const fs = require("fs");
const path = require("path");

// Dossier à parcourir : premier argument de la ligne de commande,
// ou le dossier courant si aucun argument n'est donné.
const CIBLE = process.argv[2] || process.cwd();

// Parcourt un dossier et ses sous-dossiers.
function listerFichiers(dossier) {
  const resultats = [];

  let entrees;
  try {
    entrees = fs.readdirSync(dossier, { withFileTypes: true });
  } catch (err) {
    console.error(`  ⚠️  Dossier illisible, ignoré : ${dossier} (${err.code})`);
    return resultats;
  }

  for (const entree of entrees) {
    // On ignore les fichiers et dossiers cachés (.git, .DS_Store…)
    if (entree.name.startsWith(".")) continue;

    const complet = path.join(dossier, entree.name);

    if (entree.isDirectory()) {
      resultats.push(...listerFichiers(complet));
    } else if (entree.isFile()) {
      try {
        const stats = fs.statSync(complet);
        resultats.push({
          chemin: path.relative(CIBLE, complet),
          taille: stats.size,
          modifie: stats.mtime,
        });
      } catch (err) {
        console.error(`  ⚠️  Fichier illisible, ignoré : ${complet}`);
      }
    }
  }

  return resultats;
}

// Affiche une taille en octets sous une forme lisible.
function formaterTaille(octets) {
  if (octets < 1024) return `${octets} o`;
  if (octets < 1024 * 1024) return `${(octets / 1024).toFixed(1)} Ko`;
  return `${(octets / (1024 * 1024)).toFixed(1)} Mo`;
}

// --- Programme principal ---

if (!fs.existsSync(CIBLE)) {
  console.error(`Erreur : le dossier « ${CIBLE} » n'existe pas.`);
  process.exit(1);
}

console.log(`Dossier : ${path.resolve(CIBLE)}`);
console.log("");

const fichiers = listerFichiers(CIBLE);

if (fichiers.length === 0) {
  console.log("Aucun fichier trouvé.");
  process.exit(0);
}

// Tri du plus récent au plus ancien.
fichiers.sort((a, b) => b.modifie - a.modifie);

for (const f of fichiers) {
  const date = f.modifie.toISOString().slice(0, 10);
  const taille = formaterTaille(f.taille).padStart(9);
  console.log(`${date}  ${taille}  ${f.chemin}`);
}

const total = fichiers.reduce((somme, f) => somme + f.taille, 0);
console.log("");
console.log(`${fichiers.length} fichier(s) — ${formaterTaille(total)} au total.`);
