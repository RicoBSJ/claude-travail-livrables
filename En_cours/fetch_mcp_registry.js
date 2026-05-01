// fetch_mcp_registry.js
// Récupère la liste complète du registre MCP via pagination curseur
// Ne garde que la version "latest" de chaque serveur
"use strict";

const https = require("https");
const fs = require("fs");

const BASE_URL = "https://registry.modelcontextprotocol.io/v0.1/servers";
const LIMIT = 96;
const OUT_PATH = "/Users/utilisateur/kDrive/Claude_Travail/Ressources/MCP_servers_registry.txt";

function fetchPage(cursor) {
  return new Promise((resolve, reject) => {
    const url = cursor
      ? `${BASE_URL}?limit=${LIMIT}&cursor=${encodeURIComponent(cursor)}`
      : `${BASE_URL}?limit=${LIMIT}`;
    https.get(url, { headers: { "Accept": "application/json", "User-Agent": "Mozilla/5.0" } }, (res) => {
      let data = "";
      res.on("data", (chunk) => data += chunk);
      res.on("end", () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`Parse error: ${e.message}\nData: ${data.slice(0, 200)}`)); }
      });
    }).on("error", reject);
  });
}

async function fetchAll() {
  const allServers = new Map(); // name → server (latest only)
  let cursor = null;
  let page = 0;
  let totalFetched = 0;

  console.log("Récupération du registre MCP...");

  do {
    page++;
    process.stdout.write(`  Page ${page}... `);
    const data = await fetchPage(cursor);
    const servers = data.servers || [];
    totalFetched += servers.length;
    process.stdout.write(`${servers.length} entrées\n`);

    for (const entry of servers) {
      const s = entry.server || entry;
      const name = s.name;
      const isLatest = entry._meta?.["io.modelcontextprotocol.registry/official"]?.isLatest;

      // Ne garder que la version latest, ou si pas d'info, garder si pas encore vu
      if (isLatest === true || isLatest === undefined) {
        allServers.set(name, { server: s, meta: entry._meta });
      } else if (!allServers.has(name)) {
        allServers.set(name, { server: s, meta: entry._meta });
      }
    }

    cursor = (data.metadata && data.metadata.nextCursor) || null;

    // Petite pause pour ne pas surcharger l'API
    if (cursor) await new Promise(r => setTimeout(r, 300));

  } while (cursor);

  console.log(`\nTotal brut : ${totalFetched} entrées`);
  console.log(`Serveurs uniques (latest) : ${allServers.size}`);
  return allServers;
}

function formatOutput(servers) {
  const date = new Date().toISOString().slice(0, 10);
  const lines = [];

  lines.push("=".repeat(80));
  lines.push("REGISTRE DES SERVEURS MCP (Model Context Protocol)");
  lines.push("Source  : registry.modelcontextprotocol.io");
  lines.push(`Extrait : ${date}`);
  lines.push(`Total   : ${servers.size} serveurs uniques`);
  lines.push("=".repeat(80));
  lines.push("");
  lines.push("LÉGENDE DES COLONNES");
  lines.push("  NOM       : identifiant unique du serveur (éditeur/nom)");
  lines.push("  VERSION   : dernière version publiée");
  lines.push("  TYPE      : http (distant) ou stdio (local)");
  lines.push("  REPO      : dépôt source GitHub/autre");
  lines.push("  DESC      : description courte");
  lines.push("");
  lines.push("=".repeat(80));
  lines.push("");

  // Trier par nom
  const sorted = [...servers.entries()].sort((a, b) => a[0].localeCompare(b[0]));

  let i = 1;
  for (const [name, { server: s, meta }] of sorted) {
    const version = s.version || "—";
    const desc = s.description || "—";
    const repoUrl = s.repository?.url || "—";
    const remoteUrl = (s.remotes && s.remotes[0]?.url) || "—";
    const type = (s.remotes && s.remotes[0]?.type) ? "http" : "stdio";
    const publishedAt = meta?.["io.modelcontextprotocol.registry/official"]?.publishedAt?.slice(0, 10) || "—";

    lines.push(`${String(i).padStart(4, " ")}. ${name}`);
    lines.push(`      Version : ${version}   |   Type : ${type}   |   Publié : ${publishedAt}`);
    lines.push(`      Desc    : ${desc.slice(0, 100)}${desc.length > 100 ? "…" : ""}`);
    lines.push(`      Repo    : ${repoUrl}`);
    if (remoteUrl !== "—") lines.push(`      URL MCP : ${remoteUrl}`);
    lines.push("");
    i++;
  }

  lines.push("=".repeat(80));
  lines.push("RESSOURCES");
  lines.push("  Registre web  : https://registry.modelcontextprotocol.io/");
  lines.push("  Dépôt GitHub  : https://github.com/modelcontextprotocol/servers");
  lines.push("  API           : https://registry.modelcontextprotocol.io/v0.1/servers?limit=96");
  lines.push("  Documentation : https://modelcontextprotocol.io/docs");
  lines.push("");
  lines.push("INSTALLATION DANS CLAUDE CODE");
  lines.push("  claude mcp add <nom> <commande>                     (serveur stdio)");
  lines.push("  claude mcp add --transport http <nom> <url>          (serveur http)");
  lines.push("  claude mcp list                                      (lister)");
  lines.push("  claude mcp remove <nom>                              (supprimer)");
  lines.push("=".repeat(80));

  return lines.join("\n");
}

(async () => {
  try {
    const servers = await fetchAll();
    const content = formatOutput(servers);
    fs.writeFileSync(OUT_PATH, content, "utf8");
    const kb = Math.round(fs.statSync(OUT_PATH).size / 1024);
    console.log(`\n✅ Fichier généré : ${OUT_PATH}`);
    console.log(`   Taille : ${kb} Ko | Serveurs uniques : ${servers.size}`);
  } catch (err) {
    console.error("❌ Erreur :", err.message);
    process.exit(1);
  }
})();
