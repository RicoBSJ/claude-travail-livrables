// demo_recursivite.js — Même logique que scripts/inventaire.js,
// mais qui RACONTE ce qu'elle fait à chaque appel.
// Lecture seule. Fichier de démonstration, à supprimer après.

const fs = require("fs");
const path = require("path");

const EXTENSIONS = [".docx", ".pptx", ".pdf", ".md"];

// Même repérage relatif que dans inventaire.js : on remonte de 4 niveaux
// depuis scripts/ pour retrouver la racine du projet, plutôt que d'écrire
// un chemin absolu qui casserait sur une autre machine.
const RACINE = path.resolve(__dirname, "..", "..", "..", "..");
const CIBLE = path.join(RACINE, "sources", "veille");

let numeroAppel = 0;

function listerFichiers(dossier, profondeur = 0) {
  const moi = ++numeroAppel;                 // numéro de CET appel
  const marge = "│  ".repeat(profondeur);
  const nom = path.basename(dossier);

  console.log(`${marge}┌─ APPEL #${moi} — j'entre dans « ${nom} » (profondeur ${profondeur})`);

  if (!fs.existsSync(dossier)) {
    console.log(`${marge}└─ APPEL #${moi} — dossier absent, je renvoie 0 fichier`);
    return [];
  }

  const resultats = [];
  const entrees = fs.readdirSync(dossier, { withFileTypes: true });
  const nbDossiers = entrees.filter((e) => e.isDirectory()).length;
  const nbAutres = entrees.length - nbDossiers;
  console.log(`${marge}│  je vois ${entrees.length} entrée(s) : ${nbDossiers} dossier(s), ${nbAutres} fichier(s)`);

  for (const entree of entrees) {
    const complet = path.join(dossier, entree.name);

    if (entree.isDirectory()) {
      console.log(`${marge}│  → « ${entree.name} » est un DOSSIER : je m'appelle moi-même dessus`);
      const sousResultats = listerFichiers(complet, profondeur + 1);
      console.log(`${marge}│  ← je récupère ${sousResultats.length} fichier(s) de « ${entree.name} », je les ajoute aux miens`);
      resultats.push(...sousResultats);
    } else if (EXTENSIONS.includes(path.extname(entree.name).toLowerCase())) {
      resultats.push({ nom: entree.name });
    }
  }

  console.log(`${marge}└─ APPEL #${moi} — je quitte « ${nom} » en renvoyant ${resultats.length} fichier(s)`);
  return resultats;
}

console.log("═".repeat(78));
console.log("DÉMONSTRATION — la fonction s'appelle elle-même pour descendre dans l'arborescence");
console.log("═".repeat(78));
console.log("");

const tous = listerFichiers(CIBLE);

console.log("");
console.log("═".repeat(78));
console.log(`RÉSULTAT : ${tous.length} fichier(s) au total, obtenus en ${numeroAppel} appel(s) de la fonction.`);
console.log("═".repeat(78));
