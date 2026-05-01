"use strict";
// highlight_mcp_registry.js
// Ajoute deux sections "SÉLECTION" en tête du registre MCP :
//   — MÉDICO-SOCIAL (santé, handicap, soins, thérapie…)
//   — PRODUCTION DE CONTENUS (documents, PDF, présentations, markdown…)

const fs = require("fs");

const SRC  = "/Users/utilisateur/kDrive/Claude_Travail/Ressources/MCP_servers_registry.txt";
const DEST = "/Users/utilisateur/kDrive/Claude_Travail/Ressources/MCP_servers_registry.txt";

// ── Mots-clés ─────────────────────────────────────────────────────────────────
const MEDICO_KEYWORDS = [
  "health","medical","clinic","patient","hospital","therapy","rehabilitat",
  "mental health","pharma","drug","diagnostic","ehr","fhir","emr",
  "nursing","elder","senior","dementia","autism","disabilit",
  "wellbeing","wellness","clinical trial","pubmed","medline",
  "healthcare","care provider","social care","medical record",
  "telemedicine","telehealth","radiology","patholog","oncolog"
];

const CONTENT_KEYWORDS = [
  "document generation","pdf generation","pdf creation","pdf export",
  "powerpoint","presentation","pptx","slide deck","slides",
  "google docs","google slides","confluence","notion",
  "content creation","writing assistant","writing tool",
  "docx","word document","newsletter","editorial",
  "markdown publish","publish markdown","shareable url",
  "content publish","blog post"
];

// ── Parser : découpe en blocs d'entrée ────────────────────────────────────────
function parseBlocks(text) {
  // Chaque bloc commence par "   N. nom/serveur"
  const raw = text.split(/\n(?=\s{0,4}\d+\. )/);
  return raw.map(b => b.trim()).filter(b => /^\d+\./.test(b));
}

function match(block, keywords) {
  const low = block.toLowerCase();
  return keywords.some(k => low.includes(k));
}

// ── Formattage d'un bloc pour la section de sélection ─────────────────────────
function formatShort(block) {
  const lines = block.split("\n");
  // Ligne 0 : numéro + nom, Ligne 1 : version/type, Ligne 2 : desc
  const name    = lines[0].replace(/^\d+\.\s+/, "").trim();
  const meta    = (lines[1] || "").trim();
  const desc    = (lines[2] || "").replace(/Desc\s+:\s*/i, "").trim();
  const repo    = (lines[3] || "").replace(/Repo\s+:\s*/i, "").trim();
  const url     = (lines[4] || "").replace(/URL MCP\s+:\s*/i, "").trim();

  let out = `  • ${name}\n`;
  out += `    ${meta}\n`;
  if (desc && desc !== "—") out += `    ${desc.slice(0,110)}${desc.length>110?"…":""}\n`;
  if (url && url !== "—")  out += `    URL MCP : ${url}\n`;
  else if (repo && repo !== "—") out += `    Repo    : ${repo}\n`;
  return out;
}

// ── Main ──────────────────────────────────────────────────────────────────────
const text   = fs.readFileSync(SRC, "utf8");
const blocks = parseBlocks(text);

const medicoBlocks  = blocks.filter(b => match(b, MEDICO_KEYWORDS));
const contentBlocks = blocks.filter(b => match(b, CONTENT_KEYWORDS));

console.log(`Médico-social    : ${medicoBlocks.length} serveurs`);
console.log(`Production cont. : ${contentBlocks.length} serveurs`);

// ── Construire l'en-tête de sélection ─────────────────────────────────────────
const SEP = "=".repeat(80);
const sep = "-".repeat(80);

let header = "";
header += SEP + "\n";
header += "★  SÉLECTION — MÉDICO-SOCIAL & SANTÉ\n";
header += `   ${medicoBlocks.length} serveurs identifiés (santé, soins, handicap, thérapie, dossier médical…)\n`;
header += SEP + "\n\n";

for (const b of medicoBlocks) {
  header += formatShort(b) + "\n";
}

header += SEP + "\n";
header += "★  SÉLECTION — PRODUCTION DE CONTENUS\n";
header += `   ${contentBlocks.length} serveurs identifiés (documents, PDF, présentations, markdown, publishing…)\n`;
header += SEP + "\n\n";

for (const b of contentBlocks) {
  header += formatShort(b) + "\n";
}

header += SEP + "\n";
header += "FIN DES SÉLECTIONS — REGISTRE COMPLET CI-DESSOUS\n";
header += SEP + "\n\n";

// ── Insérer après le premier séparateur d'en-tête du fichier ──────────────────
// Le fichier commence par une ligne "====…" puis REGISTRE DES SERVEURS MCP …
// On insère la sélection juste avant la première entrée numérotée
const insertAt = text.indexOf("\n   1. ");
const newContent = text.slice(0, insertAt + 1) + header + text.slice(insertAt + 1);

fs.writeFileSync(DEST, newContent, "utf8");

const kb = Math.round(fs.statSync(DEST).size / 1024);
console.log(`\n✅ Fichier mis à jour : ${DEST}`);
console.log(`   Taille : ${kb} Ko`);
