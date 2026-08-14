// src/inventaire.ts — Inventaire typé des livrables (TypeScript)
// Leçon 03 — TypeScript et structure de projet (14/08/2026)
//
// Lance (après compilation) : node dist/inventaire.js
//
// Lecture seule : ce script ne modifie aucun livrable.

import * as fs from "node:fs";
import * as path from "node:path";
import type { Livrable, Categorie, Inventaire, DossierConfig } from "./types";

// ── Configuration ──────────────────────────────────────────────────────────

// Le script compilé vit dans livrables/projets/appli-ia/dist/
// On remonte de 4 niveaux pour atteindre la racine Claude_Travail/
const RACINE: string = path.resolve(__dirname, "..", "..", "..", "..");

const EXTENSIONS: string[] = [".docx", ".pptx", ".pdf", ".md"];

// Exclusions spec v1.2 :
//   ~$…       → fichiers temporaires de verrouillage Office
//   readme.md → décrit le dossier, n'est pas un livrable (écart n°4, résolu leçon 03)
const PREFIXE_VERROU = "~$";
const DOCS_DE_DOSSIER: string[] = ["readme.md"];

const DOSSIERS: DossierConfig[] = [
  { cle: "lecons",       chemin: path.join(RACINE, "livrables", "lecons") },
  { cle: "quiz",         chemin: path.join(RACINE, "livrables", "quiz") },
  { cle: "infographies", chemin: path.join(RACINE, "livrables", "infographies") },
  { cle: "veilles",      chemin: path.join(RACINE, "sources",   "veille") },
  { cle: "documents",    chemin: path.join(RACINE, "livrables", "documents") },
  { cle: "controles",    chemin: path.join(RACINE, "livrables", "controles") },
];

// ── Logique métier ─────────────────────────────────────────────────────────

function estLivrable(nom: string): boolean {
  if (nom.startsWith(PREFIXE_VERROU)) return false;
  if (DOCS_DE_DOSSIER.includes(nom.toLowerCase())) return false;
  return EXTENSIONS.includes(path.extname(nom).toLowerCase());
}

function listerFichiers(dossier: string): Livrable[] {
  if (!fs.existsSync(dossier)) return [];
  const resultats: Livrable[] = [];
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

function construireInventaire(): Inventaire {
  const categories: Inventaire = {};
  for (const { cle, chemin } of DOSSIERS) {
    const fichiers: Livrable[] = listerFichiers(chemin);
    const octets: number = fichiers.reduce((s, f) => s + f.taille, 0);
    const cat: Categorie = {
      nombre:    fichiers.length,
      taille_ko: Math.round(octets / 1024),
      recents:   [...fichiers]
        .sort((a, b) => (b.modifie > a.modifie ? 1 : -1))
        .slice(0, 5),
    };
    categories[cle] = cat;
  }
  return categories;
}

// ── Affichage terminal ─────────────────────────────────────────────────────

function formaterMo(ko: number): string {
  return (ko / 1024).toFixed(1) + " Mo";
}

const data: Inventaire = construireInventaire();

console.log("Portail Livrables — inventaire TypeScript\n");
for (const [cle, cat] of Object.entries(data)) {
  console.log(
    `${cle.padEnd(14)} ${String(cat.nombre).padStart(3)} fichier(s)   ${formaterMo(cat.taille_ko)}`
  );
  for (const f of cat.recents) {
    console.log(`   ${f.modifie}  ${f.nom}`);
  }
  console.log("");
}
