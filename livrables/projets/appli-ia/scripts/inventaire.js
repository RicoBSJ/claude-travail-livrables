// scripts/inventaire.js — Inventaire des livrables Claude_Travail
// Lecture seule : ce script n'écrit ni ne supprime aucun fichier.

const fs = require("fs");
const path = require("path");

// Le script vit dans livrables/projets/appli-ia/scripts/
// On remonte de 4 niveaux pour atteindre la racine Claude_Travail/
const RACINE = path.resolve(__dirname, "..", "..", "..", "..");

const EXTENSIONS = [".docx", ".pptx", ".pdf", ".md"];

const DOSSIERS = [
  { cle: "lecons", chemin: path.join(RACINE, "livrables", "lecons") },
  { cle: "quiz", chemin: path.join(RACINE, "livrables", "quiz") },
  { cle: "infographies", chemin: path.join(RACINE, "livrables", "infographies") },
  { cle: "veilles", chemin: path.join(RACINE, "sources", "veille") },
];

// Parcourt un dossier et ses sous-dossiers, renvoie les fichiers retenus
function listerFichiers(dossier) {
  if (!fs.existsSync(dossier)) return [];

  const resultats = [];
  for (const entree of fs.readdirSync(dossier, { withFileTypes: true })) {
    const complet = path.join(dossier, entree.name);

    if (entree.isDirectory()) {
      resultats.push(...listerFichiers(complet));
    } else if (EXTENSIONS.includes(path.extname(entree.name).toLowerCase())) {
      const stats = fs.statSync(complet);
      resultats.push({
        nom: entree.name,
        taille: stats.size,
        modifie: stats.mtime,
      });
    }
  }
  return resultats;
}

console.log("Inventaire des livrables");
console.log("Racine :", RACINE);
console.log("");

let total = 0;

for (const { cle, chemin } of DOSSIERS) {
  const fichiers = listerFichiers(chemin);
  total += fichiers.length;

  const octets = fichiers.reduce((somme, f) => somme + f.taille, 0);
  const ko = Math.round(octets / 1024);
  console.log(`${cle.padEnd(14)} ${String(fichiers.length).padStart(4)} fichier(s)  ${ko} Ko`);

  // Les 3 plus récents, pour vérifier que la lecture fonctionne
  const recents = [...fichiers]
    .sort((a, b) => b.modifie - a.modifie)
    .slice(0, 3);

  for (const f of recents) {
    const date = f.modifie.toISOString().slice(0, 10);
    console.log(`   ${date}  ${f.nom}`);
  }
}

console.log("");
console.log(`Total : ${total} livrable(s).`);
