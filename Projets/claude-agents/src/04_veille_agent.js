/**
 * Session 04 — Agent de veille autonome
 * Récupère des articles depuis des sources web, extrait les titres/résumés,
 * génère une synthèse et la sauvegarde automatiquement.
 *
 * Outils ajoutés :
 *   - fetch_url(url)               : récupère le texte d'une page web
 *   - save_summary(filename, text) : sauvegarde le résumé en fichier .md
 *
 * Usage : node src/04_veille_agent.js
 * Prérequis : .env avec ANTHROPIC_API_KEY
 */

"use strict";

require("dotenv").config();
const Anthropic  = require("@anthropic-ai/sdk");
const { execSync } = require("child_process");
const https      = require("https");
const http       = require("http");
const fs         = require("fs");
const path       = require("path");
const url        = require("url");

const client = new Anthropic.default();

const BASE = "/Users/utilisateur/kDrive/Claude_Travail";

// ─── Outils ──────────────────────────────────────────────────────────────────

const TOOLS = [
  {
    name: "fetch_url",
    description:
      "Récupère le contenu textuel d'une URL (page web, RSS, blog). " +
      "Retourne jusqu'à 6000 caractères de texte brut. " +
      "Ne fonctionne pas sur les sites nécessitant une authentification.",
    input_schema: {
      type: "object",
      properties: {
        url_str: { type: "string", description: "URL complète à récupérer (https://…)" },
        max_chars: { type: "number", description: "Nombre max de caractères (défaut : 6000)" },
      },
      required: ["url_str"],
    },
  },
  {
    name: "save_summary",
    description: "Sauvegarde un texte dans un fichier Markdown dans le répertoire Sources/Veille/.",
    input_schema: {
      type: "object",
      properties: {
        filename: { type: "string", description: "Nom du fichier sans extension (ex: veille_ia_2026-04-24)" },
        content:  { type: "string", description: "Contenu Markdown à écrire" },
      },
      required: ["filename", "content"],
    },
  },
  {
    name: "bash",
    description: "Exécute une commande shell simple. Timeout 10 s.",
    input_schema: {
      type: "object",
      properties: { cmd: { type: "string" } },
      required: ["cmd"],
    },
  },
];

// ─── Implémentations ─────────────────────────────────────────────────────────

function tool_fetch_url({ url_str, max_chars = 6000 }) {
  return new Promise((resolve) => {
    try {
      const parsed = new URL(url_str);
      const lib    = parsed.protocol === "https:" ? https : http;

      const req = lib.get(
        url_str,
        { headers: { "User-Agent": "Mozilla/5.0 (compatible; AgentVeille/1.0)", Accept: "text/html,application/xml,text/plain" }, timeout: 12000 },
        (res) => {
          // Suivre les redirections (max 2)
          if ((res.statusCode === 301 || res.statusCode === 302) && res.headers.location) {
            resolve(tool_fetch_url({ url_str: res.headers.location, max_chars }));
            return;
          }
          if (res.statusCode !== 200) {
            resolve({ error: `HTTP ${res.statusCode} pour ${url_str}` });
            return;
          }
          let data = "";
          res.on("data", (chunk) => { data += chunk; });
          res.on("end", () => {
            // Nettoyer le HTML basiquement
            const text = data
              .replace(/<script[\s\S]*?<\/script>/gi, " ")
              .replace(/<style[\s\S]*?<\/style>/gi, " ")
              .replace(/<[^>]+>/g, " ")
              .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
              .replace(/\s{2,}/g, " ")
              .trim();
            const truncated = text.length > max_chars ? text.slice(0, max_chars) + "\n[... tronqué]" : text;
            resolve({ content: truncated, length: text.length, url: url_str });
          });
        }
      );
      req.on("error", (e) => resolve({ error: e.message }));
      req.on("timeout", () => { req.destroy(); resolve({ error: "Timeout 12 s" }); });
    } catch (e) {
      resolve({ error: e.message });
    }
  });
}

function tool_save_summary({ filename, content }) {
  try {
    const dir  = path.join(BASE, "Sources", "Veille");
    const safe = filename.replace(/[^a-zA-Z0-9_\-]/g, "_") + ".md";
    const dest = path.join(dir, safe);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(dest, content, "utf8");
    return { success: true, path: dest, bytes: Buffer.byteLength(content, "utf8") };
  } catch (e) {
    return { error: e.message };
  }
}

function tool_bash({ cmd }) {
  try {
    const out = execSync(cmd, { timeout: 10000, encoding: "utf8" });
    return { success: true, output: out.trim() };
  } catch (e) {
    return { success: false, output: e.stdout?.trim() || "", stderr: e.message };
  }
}

async function executeTool(name, input) {
  switch (name) {
    case "fetch_url":    return await tool_fetch_url(input);
    case "save_summary": return tool_save_summary(input);
    case "bash":         return tool_bash(input);
    default:             return { error: `Outil inconnu : ${name}` };
  }
}

// ─── Agent ───────────────────────────────────────────────────────────────────

class VeilleAgent {
  constructor({ model = "claude-opus-4-5", maxIter = 30 } = {}) {
    this.model   = model;
    this.maxIter = maxIter;
    this.messages = [];
    this.totalIn  = 0;
    this.totalOut = 0;
  }

  async run(task) {
    console.log("\n" + "═".repeat(60));
    console.log("TÂCHE :", task.slice(0, 80) + (task.length > 80 ? "…" : ""));
    console.log("═".repeat(60));

    this.messages.push({ role: "user", content: task });

    for (let i = 0; i < this.maxIter; i++) {
      console.log(`\n[Itération ${i + 1}]`);

      const resp = await client.messages.create({
        model: this.model,
        max_tokens: 4096,
        system: `Tu es un agent de veille professionnelle autonome pour le projet Claude_Travail (secteur médico-social français).
Tu sais récupérer des pages web, extraire les informations pertinentes, synthétiser et sauvegarder automatiquement.
Date du jour : ${new Date().toISOString().slice(0, 10)}.
Réponds toujours en français professionnel. Quand tu as terminé, conclus avec "✅ Veille terminée."`,
        tools: TOOLS,
        messages: this.messages,
      });

      this.totalIn  += resp.usage.input_tokens;
      this.totalOut += resp.usage.output_tokens;
      console.log(`  stop: ${resp.stop_reason} | tokens: ${resp.usage.input_tokens}in/${resp.usage.output_tokens}out`);

      this.messages.push({ role: "assistant", content: resp.content });

      if (resp.stop_reason !== "tool_use") {
        const text = resp.content.find(b => b.type === "text")?.text ?? "(sans texte)";
        console.log("\n[Agent terminé]\n");
        console.log(`Total tokens : ${this.totalIn}in / ${this.totalOut}out`);
        return text;
      }

      const results = [];
      for (const block of resp.content) {
        if (block.type !== "tool_use") continue;
        console.log(`  → ${block.name}(${JSON.stringify(block.input).slice(0, 60)}…)`);
        const res     = await executeTool(block.name, block.input);
        const resStr  = JSON.stringify(res, null, 2);
        console.log(`    ← ${resStr.slice(0, 80)}${resStr.length > 80 ? "…" : ""}`);
        results.push({ type: "tool_result", tool_use_id: block.id, content: resStr });
      }
      this.messages.push({ role: "user", content: results });
    }
    throw new Error(`Limite de ${this.maxIter} itérations atteinte.`);
  }
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log("=== Session 04 — Agent de veille autonome ===\n");

  const today    = new Date().toISOString().slice(0, 10);
  const filename = `veille_ia_nocode_${today}`;

  const agent = new VeilleAgent({ maxIter: 30 });

  const task = `Ta mission : effectuer une veille de l'actualité IA et NO-CODE de la semaine et produire une synthèse.

Étape 1 — Récupère le contenu des 3 sources suivantes avec fetch_url :
  a) https://the-decoder.com
  b) https://openai.com/blog/rss.xml
  c) https://blog.n8n.io

Étape 2 — Pour chaque source, identifie les 3 articles les plus récents (titre, date, résumé en 2-3 phrases).

Étape 3 — Identifie le thème dominant de la semaine qui traverse les 3 sources.

Étape 4 — Rédige une synthèse Markdown avec cette structure exacte :
  # Veille IA + NO-CODE — ${today}

  ## Thème dominant
  [1 paragraphe]

  ## Articles clés
  ### The Decoder
  - **[Titre]** : [résumé 2 phrases]
  ### OpenAI Blog
  - **[Titre]** : [résumé 2 phrases]
  ### n8n Blog
  - **[Titre]** : [résumé 2 phrases]

  ## Points de vigilance pour les professionnels NO-CODE
  - [3 bullet points pratiques]

  ## À surveiller
  - [2 tendances à observer la semaine prochaine]

Étape 5 — Sauvegarde la synthèse avec save_summary (filename: "${filename}").

Confirme le chemin du fichier créé et la taille en octets.`;

  try {
    const result = await agent.run(task);
    console.log(result);
  } catch (err) {
    console.error("❌", err.message);
    process.exit(1);
  }
}

main();
