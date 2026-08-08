// scripts/serveur.js — Serveur HTTP local du Portail Livrables
// Leçon 02 — Socle web : HTML/CSS/JS moderne
//
// Lance : node scripts/serveur.js
// puis ouvre http://localhost:3000 dans ton navigateur.
//
// Lecture seule : ce script ne modifie aucun livrable.

const http = require("node:http");
const fs   = require("node:fs");
const path = require("node:path");

// ── Configuration ──────────────────────────────────────────────────────────
const PORT  = 3000;

// Le script vit dans livrables/projets/appli-ia/scripts/
// On remonte de 4 niveaux pour atteindre la racine Claude_Travail/
const RACINE = path.resolve(__dirname, "..", "..", "..", "..");

const EXTENSIONS = [".docx", ".pptx", ".pdf", ".md"];

const DOSSIERS = [
  { cle: "lecons",       chemin: path.join(RACINE, "livrables", "lecons") },
  { cle: "quiz",         chemin: path.join(RACINE, "livrables", "quiz") },
  { cle: "infographies", chemin: path.join(RACINE, "livrables", "infographies") },
  { cle: "veilles",      chemin: path.join(RACINE, "sources",   "veille") },
  { cle: "documents",    chemin: path.join(RACINE, "livrables", "documents") },
  { cle: "controles",    chemin: path.join(RACINE, "livrables", "controles") },
];

// ── Logique métier ─────────────────────────────────────────────────────────

// Renvoie true si le fichier est un livrable réel (pas un verrou Office, pas une extension hors liste)
function estLivrable(nom) {
  // Les fichiers temporaires Office portent un préfixe ~$ — on les exclut
  if (nom.startsWith("~$")) return false;
  return EXTENSIONS.includes(path.extname(nom).toLowerCase());
}

// Parcourt un dossier et ses sous-dossiers, renvoie les fichiers retenus
function listerFichiers(dossier) {
  if (!fs.existsSync(dossier)) return [];
  const resultats = [];
  for (const entree of fs.readdirSync(dossier, { withFileTypes: true })) {
    const complet = path.join(dossier, entree.name);
    if (entree.isDirectory()) {
      resultats.push(...listerFichiers(complet));
    } else if (estLivrable(entree.name)) {
      const stats = fs.statSync(complet);
      resultats.push({
        nom:     entree.name,
        taille:  stats.size,
        modifie: stats.mtime.toISOString().slice(0, 10),
      });
    }
  }
  return resultats;
}

// Construit l'inventaire complet par catégorie
function inventaire() {
  const categories = {};
  for (const { cle, chemin } of DOSSIERS) {
    const fichiers = listerFichiers(chemin);
    const octets   = fichiers.reduce((s, f) => s + f.taille, 0);
    categories[cle] = {
      nombre:    fichiers.length,
      taille_ko: Math.round(octets / 1024),
      recents:   [...fichiers]
        .sort((a, b) => (b.modifie > a.modifie ? 1 : -1))
        .slice(0, 5),
    };
  }
  return categories;
}

// ── Serveur HTTP ───────────────────────────────────────────────────────────

// Les fichiers statiques (HTML, CSS, JS côté client) vivent dans public/
const PUBLIC = path.join(__dirname, "..", "public");

// Table de correspondance extension → type MIME
const TYPES_MIME = {
  ".html": "text/html; charset=utf-8",
  ".css":  "text/css; charset=utf-8",
  ".js":   "application/javascript; charset=utf-8",
};

const serveur = http.createServer((req, res) => {

  // ── Route API : /api/inventaire ─────────────────────────────────────────
  // Renvoie l'inventaire en JSON ; le navigateur le récupère avec fetch()
  if (req.url === "/api/inventaire") {
    const data = JSON.stringify(inventaire(), null, 2);
    res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
    res.end(data);
    return;
  }

  // ── Route statique : fichiers du dossier public/ ────────────────────────
  // / → index.html (convention universelle du web)
  const cible = req.url === "/" ? "/index.html" : req.url;

  // Résolution du chemin absolu
  const absolu = path.resolve(PUBLIC, "." + cible);

  // Garde-fou sécurité : on interdit toute sortie du dossier public/
  // (protection contre les attaques de type "path traversal" : ../../etc/passwd)
  if (!absolu.startsWith(PUBLIC + path.sep) && absolu !== PUBLIC) {
    res.writeHead(403, { "Content-Type": "text/plain; charset=utf-8" });
    res.end("403 — Accès interdit");
    return;
  }

  const ext  = path.extname(absolu);
  const mime = TYPES_MIME[ext] || "application/octet-stream";

  // Lecture asynchrone du fichier (ne bloque pas le serveur pendant la lecture).
  // Exercice « CASSER » de la leçon 02 : ajoute + '.inexistant' au chemin ci-dessous,
  // relance, observe le 404 — puis retire-le. Le serveur ne plante pas : il répond.
  fs.readFile(absolu, (err, contenu) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end("404 — Page introuvable");
      return;
    }
    res.writeHead(200, { "Content-Type": mime });
    res.end(contenu);
  });
});

serveur.listen(PORT, () => {
  console.log(`✅ Portail Livrables démarré → http://localhost:${PORT}`);
  console.log("   Ctrl+C pour arrêter.");
});
