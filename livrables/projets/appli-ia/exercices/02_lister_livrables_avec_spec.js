// lister_livrables_spec.js — Liste les livrables, conformément à SPEC.md v1.2
//
// Conformité revendiquée, point par point :
//   Données      : les 6 dossiers déclarés, extensions .docx .pptx .pdf .md
//   Exclusions   : fichiers de verrouillage Office (~$…)
//   Hors périmètre : livrables/projets/ n'est jamais parcouru
//   Lecture seule : aucune écriture, aucune suppression, aucun renommage
//   Fonction 1   : lister avec date, type, taille
//   Fonction 2   : rechercher par mot-clé dans le nom     → --recherche=mot
//   Fonction 3   : filtrer par type                       → --type=lecon
//   Fonction 4   : trier par date décroissante (date du NOM, pas le mtime)
//   Fonction 5   : « ouvrir d'un clic » — hors de portée d'un script terminal, voir plus bas
//
// Usage :
//   node lister_livrables_spec.js
//   node lister_livrables_spec.js --type=lecon
//   node lister_livrables_spec.js --recherche=serafin
//   node lister_livrables_spec.js --type=veille --recherche=imac

const fs = require("fs");
const path = require("path");

// --- Constantes issues directement de SPEC.md ---

// Le script vit dans livrables/projets/appli-ia/exercices/ :
// on remonte de 4 niveaux pour atteindre la racine Claude_Travail/.
// (Ce chemin a dû être corrigé le 08/08/2026 après déplacement du fichier —
//  illustration concrète de la dette « chemin en dur » notée dans PROJET.md.)
const RACINE = path.resolve(__dirname, "..", "..", "..", "..");

// SPEC « Données » : les six dossiers déclarés, et eux seuls.
const SOURCES = [
  { type: "lecon", libelle: "Leçon", dossier: path.join(RACINE, "livrables", "lecons") },
  { type: "quiz", libelle: "Quiz", dossier: path.join(RACINE, "livrables", "quiz") },
  { type: "infographie", libelle: "Infographie", dossier: path.join(RACINE, "livrables", "infographies") },
  { type: "veille", libelle: "Veille", dossier: path.join(RACINE, "sources", "veille") },
  { type: "document", libelle: "Document", dossier: path.join(RACINE, "livrables", "documents") },
  { type: "controle", libelle: "Contrôle", dossier: path.join(RACINE, "livrables", "controles") },
];

// SPEC « Extensions retenues »
const EXTENSIONS = [".docx", ".pptx", ".pdf", ".md"];

// SPEC « Exclusions explicites » (v1.2)
const PREFIXE_VERROU = "~$";                    // fichiers de verrouillage Office
const DOCS_DE_DOSSIER = ["readme.md"];          // décrivent le dossier, n'en sont pas un livrable

// SPEC « Hors périmètre » : livrables/projets/ est le code du portail, pas un livrable.
// Aucune des six sources ne pointe dessus — la garantie est structurelle, pas un filtre.

// --- Lecture des arguments ---

function lireArgument(nom) {
  const prefixe = `--${nom}=`;
  const trouve = process.argv.find((a) => a.startsWith(prefixe));
  return trouve ? trouve.slice(prefixe.length).toLowerCase() : null;
}

const filtreType = lireArgument("type");
const filtreRecherche = lireArgument("recherche");

// --- Règles de la SPEC ---

// SPEC « Précision sur la date » : la date de référence est celle contenue dans le NOM
// du fichier (YYYY-MM-DD_…), et NON le mtime du disque.
function dateDuNom(nomFichier) {
  const trouve = nomFichier.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (!trouve) return null;
  return trouve[0];
}

function estLivrable(nomFichier) {
  if (nomFichier.startsWith(PREFIXE_VERROU)) return false;                 // exclusion SPEC
  if (DOCS_DE_DOSSIER.includes(nomFichier.toLowerCase())) return false;    // exclusion SPEC v1.2
  return EXTENSIONS.includes(path.extname(nomFichier).toLowerCase());
}

// --- Parcours (lecture seule) ---

function collecter(dossier, type, libelle) {
  if (!fs.existsSync(dossier)) return [];

  const resultats = [];
  for (const entree of fs.readdirSync(dossier, { withFileTypes: true })) {
    const complet = path.join(dossier, entree.name);

    if (entree.isDirectory()) {
      // SPEC : sources/veille inclut ses sous-dossiers
      resultats.push(...collecter(complet, type, libelle));
    } else if (entree.isFile() && estLivrable(entree.name)) {
      const stats = fs.statSync(complet);
      resultats.push({
        nom: entree.name,
        type,
        libelle,
        date: dateDuNom(entree.name),        // null si le nom ne porte pas de date
        taille: stats.size,
        chemin: complet,
      });
    }
  }
  return resultats;
}

function formaterTaille(octets) {
  if (octets < 1024) return `${octets} o`;
  if (octets < 1024 * 1024) return `${(octets / 1024).toFixed(0)} Ko`;
  return `${(octets / (1024 * 1024)).toFixed(1)} Mo`;
}

// --- Programme principal ---

let livrables = [];
for (const source of SOURCES) {
  livrables.push(...collecter(source.dossier, source.type, source.libelle));
}

const totalAvantFiltres = livrables.length;

// Fonction 3 — filtrer par type
if (filtreType) {
  livrables = livrables.filter((l) => l.type === filtreType);
}

// Fonction 2 — rechercher par mot-clé dans le nom
if (filtreRecherche) {
  livrables = livrables.filter((l) => l.nom.toLowerCase().includes(filtreRecherche));
}

// Fonction 4 — trier par date décroissante.
// Les fichiers sans date dans leur nom sont renvoyés en fin de liste.
livrables.sort((a, b) => {
  if (a.date && b.date) return b.date.localeCompare(a.date);
  if (a.date) return -1;
  if (b.date) return 1;
  return a.nom.localeCompare(b.nom);
});

// --- Affichage ---

console.log("Portail Livrables — inventaire conforme à SPEC.md v1.2");
if (filtreType) console.log(`Filtre type      : ${filtreType}`);
if (filtreRecherche) console.log(`Filtre recherche : « ${filtreRecherche} »`);
console.log("");

if (livrables.length === 0) {
  console.log("Aucun livrable ne correspond.");
  process.exit(0);
}

// Fonction 1 — lister avec date, type, taille
for (const l of livrables) {
  const date = l.date ? l.date : "(sans date)";
  const type = l.libelle.padEnd(12);
  const taille = formaterTaille(l.taille).padStart(8);
  console.log(`${date}  ${type} ${taille}  ${l.nom}`);
}

const sansDate = livrables.filter((l) => !l.date).length;
const octets = livrables.reduce((s, l) => s + l.taille, 0);

console.log("");
console.log(`${livrables.length} livrable(s) affiché(s) sur ${totalAvantFiltres} — ${formaterTaille(octets)}.`);
if (sansDate > 0) {
  console.log(`⚠️  ${sansDate} fichier(s) sans date dans leur nom, classés en fin de liste.`);
}

// Fonction 5 — « ouvrir un livrable d'un clic » : impossible dans un terminal.
// Elle relève de l'interface web (leçon 05). En attendant, le chemin complet
// permet de l'ouvrir à la main :
if (livrables.length === 1) {
  console.log("");
  console.log(`Pour ouvrir : open "${livrables[0].chemin}"`);
}
