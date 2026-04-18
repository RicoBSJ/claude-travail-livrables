/**
 * Session 03 — Agent basique
 * Boucle agentique autonome avec outils bash, lecture/écriture fichiers, listing.
 *
 * Ce script illustre :
 *   1. La classe Agent encapsulant la boucle agentique complète
 *   2. Quatre outils locaux : bash, read_file, write_file, list_files
 *   3. La gestion de l'historique de conversation (multiturns)
 *   4. Un exemple concret : lire les leçons .docx et créer un résumé Markdown
 *
 * Usage : node src/03_agent.js
 * Prérequis : .env avec ANTHROPIC_API_KEY
 */

"use strict";

require("dotenv").config();
const Anthropic = require("@anthropic-ai/sdk");
const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const client = new Anthropic.default();

// ─────────────────────────────────────────────
// Définitions des outils
// ─────────────────────────────────────────────

const AGENT_TOOLS = [
  {
    name: "bash",
    description:
      "Exécute une commande shell et retourne stdout + stderr. " +
      "Utiliser pour des opérations système simples (ls, date, wc, etc.). " +
      "IMPORTANT : commandes non interactives uniquement. Timeout 10 s.",
    input_schema: {
      type: "object",
      properties: {
        cmd: {
          type: "string",
          description: "Commande shell à exécuter.",
        },
      },
      required: ["cmd"],
    },
  },
  {
    name: "read_file",
    description:
      "Lit le contenu d'un fichier texte. Retourne le contenu ou une erreur.",
    input_schema: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description: "Chemin absolu ou relatif du fichier à lire.",
        },
        max_chars: {
          type: "number",
          description: "Nombre maximum de caractères à retourner (défaut : 5000).",
        },
      },
      required: ["path"],
    },
  },
  {
    name: "write_file",
    description:
      "Écrit du contenu dans un fichier texte. Crée les répertoires parents si nécessaire.",
    input_schema: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description: "Chemin absolu ou relatif du fichier de destination.",
        },
        content: {
          type: "string",
          description: "Contenu textuel à écrire.",
        },
      },
      required: ["path", "content"],
    },
  },
  {
    name: "list_files",
    description:
      "Liste les fichiers d'un répertoire (récursivement optionnel). " +
      "Retourne un tableau d'objets { name, path, size, isDir }.",
    input_schema: {
      type: "object",
      properties: {
        dir: {
          type: "string",
          description: "Chemin du répertoire à lister.",
        },
        recursive: {
          type: "boolean",
          description: "Si true, liste récursivement (défaut : false).",
        },
        extension: {
          type: "string",
          description: "Filtre par extension (ex: '.docx'). Optionnel.",
        },
      },
      required: ["dir"],
    },
  },
];

// ─────────────────────────────────────────────
// Implémentations locales des outils
// ─────────────────────────────────────────────

function tool_bash({ cmd }) {
  try {
    const output = execSync(cmd, {
      timeout: 10000,
      encoding: "utf8",
      stdio: ["pipe", "pipe", "pipe"],
    });
    return { success: true, output: output.trim() };
  } catch (err) {
    return {
      success: false,
      output: (err.stdout || "").trim(),
      stderr: (err.stderr || err.message || "").trim(),
    };
  }
}

function tool_read_file({ path: filePath, max_chars = 5000 }) {
  try {
    const resolved = path.resolve(filePath);
    if (!fs.existsSync(resolved)) {
      return { error: `Fichier introuvable : ${resolved}` };
    }
    const raw = fs.readFileSync(resolved, "utf8");
    const content =
      raw.length > max_chars ? raw.slice(0, max_chars) + "\n[... tronqué]" : raw;
    return { content, size: raw.length, path: resolved };
  } catch (err) {
    return { error: `Lecture impossible : ${err.message}` };
  }
}

function tool_write_file({ path: filePath, content }) {
  try {
    const resolved = path.resolve(filePath);
    fs.mkdirSync(path.dirname(resolved), { recursive: true });
    fs.writeFileSync(resolved, content, "utf8");
    return { success: true, path: resolved, bytes: Buffer.byteLength(content, "utf8") };
  } catch (err) {
    return { error: `Écriture impossible : ${err.message}` };
  }
}

function tool_list_files({ dir, recursive = false, extension = null }) {
  try {
    const resolved = path.resolve(dir);
    if (!fs.existsSync(resolved)) {
      return { error: `Répertoire introuvable : ${resolved}` };
    }

    const results = [];

    function scan(currentDir) {
      const entries = fs.readdirSync(currentDir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);
        if (extension && !entry.name.endsWith(extension) && !entry.isDirectory()) continue;
        const stat = fs.statSync(fullPath);
        results.push({
          name: entry.name,
          path: fullPath,
          size: stat.size,
          isDir: entry.isDirectory(),
        });
        if (recursive && entry.isDirectory()) {
          scan(fullPath);
        }
      }
    }

    scan(resolved);
    return { files: results, count: results.length };
  } catch (err) {
    return { error: `Listing impossible : ${err.message}` };
  }
}

// ─────────────────────────────────────────────
// Dispatcher
// ─────────────────────────────────────────────

function executeTool(name, input) {
  switch (name) {
    case "bash":       return tool_bash(input);
    case "read_file":  return tool_read_file(input);
    case "write_file": return tool_write_file(input);
    case "list_files": return tool_list_files(input);
    default:           return { error: `Outil inconnu : ${name}` };
  }
}

// ─────────────────────────────────────────────
// Classe Agent
// ─────────────────────────────────────────────

class Agent {
  /**
   * @param {object} options
   * @param {string} options.systemPrompt   - Prompt système de l'agent
   * @param {string} [options.model]        - Modèle Claude à utiliser
   * @param {number} [options.maxTokens]    - Max tokens par appel
   * @param {number} [options.maxIter]      - Nombre max d'itérations (sécurité anti-boucle)
   */
  constructor({
    systemPrompt = "Tu es un agent autonome capable de lire, analyser et écrire des fichiers.",
    model = "claude-opus-4-5",
    maxTokens = 4096,
    maxIter = 20,
  } = {}) {
    this.systemPrompt = systemPrompt;
    this.model = model;
    this.maxTokens = maxTokens;
    this.maxIter = maxIter;
    this.messages = [];
  }

  /**
   * addMessage(role, content)
   * Ajoute un message dans l'historique de la conversation.
   */
  addMessage(role, content) {
    this.messages.push({ role, content });
  }

  /**
   * callTool(name, params)
   * Exécute un outil localement et retourne le résultat JSON stringifié.
   */
  callTool(name, params) {
    console.log(`    [Outil] ${name}(${JSON.stringify(params).slice(0, 80)}...)`);
    const result = executeTool(name, params);
    const resultStr = JSON.stringify(result, null, 2);
    console.log(`    [Résultat] ${resultStr.slice(0, 120)}${resultStr.length > 120 ? "..." : ""}`);
    return resultStr;
  }

  /**
   * run(task)
   * Lance l'agent sur une tâche donnée.
   * Boucle : envoyer → recevoir → si tool_use → exécuter → continuer
   * S'arrête quand stop_reason !== "tool_use" ou que maxIter est atteint.
   *
   * @param {string} task - Description de la tâche à réaliser
   * @returns {string} - Réponse finale de l'agent
   */
  async run(task) {
    console.log("\n" + "=".repeat(60));
    console.log("TACHE :", task);
    console.log("=".repeat(60));

    // Initialiser la conversation avec la tâche
    this.addMessage("user", task);

    let iteration = 0;

    while (iteration < this.maxIter) {
      iteration++;
      console.log(`\n[Itération ${iteration}/${this.maxIter}] Appel API Claude...`);

      const response = await client.messages.create({
        model: this.model,
        max_tokens: this.maxTokens,
        system: this.systemPrompt,
        tools: AGENT_TOOLS,
        messages: this.messages,
      });

      console.log(`  stop_reason : ${response.stop_reason}`);
      console.log(
        `  usage : ${response.usage.input_tokens} in / ${response.usage.output_tokens} out`
      );

      // Ajouter la réponse de l'assistant dans l'historique
      this.addMessage("assistant", response.content);

      // Si Claude a terminé (pas d'outil à appeler)
      if (response.stop_reason !== "tool_use") {
        const textBlock = response.content.find((b) => b.type === "text");
        const finalText = textBlock ? textBlock.text : "(pas de réponse textuelle)";
        console.log("\n[Agent terminé — Réponse finale]\n");
        return finalText;
      }

      // Claude veut appeler un ou plusieurs outils
      const toolResults = [];

      for (const block of response.content) {
        if (block.type !== "tool_use") continue;

        const toolResultText = this.callTool(block.name, block.input);

        toolResults.push({
          type: "tool_result",
          tool_use_id: block.id,
          content: toolResultText,
        });
      }

      // Ajouter les résultats dans l'historique (rôle "user")
      this.addMessage("user", toolResults);
    }

    throw new Error(
      `Agent : limite de ${this.maxIter} itérations atteinte sans réponse finale.`
    );
  }
}

// ─────────────────────────────────────────────
// Tâche de démonstration
// ─────────────────────────────────────────────

async function main() {
  console.log("=== Session 03 — Agent basique ===\n");

  const BASE = "/Users/utilisateur/kDrive/Claude_Travail";
  const OUTPUT = `${BASE}/En_cours/session03_resume_lecons.md`;

  const agent = new Agent({
    systemPrompt: `Tu es un agent autonome expert en formation médico-sociale.
Tu travailles sur le projet Claude_Travail situé dans ${BASE}.
Tu peux utiliser les outils bash, read_file, write_file, list_files pour accomplir tes tâches.
Réponds toujours en français professionnel.
Quand tu as terminé une tâche, conclus par une confirmation courte.`,
    maxIter: 25,
  });

  const tache = `Ta mission autonome :
1. Liste tous les fichiers .docx dans le répertoire ${BASE}/Livrables/Leçons/ (outil list_files).
2. Pour chaque fichier listé, utilise bash pour obtenir sa taille et sa date de modification (commande ls -lh).
3. Produis un résumé synthétique en Markdown avec :
   - Un titre "# Résumé des leçons NO-CODE + IA"
   - La date de génération (outil bash : date '+%d/%m/%Y %H:%M')
   - Un tableau Markdown avec colonnes : N° | Titre | Date | Taille
   - Un paragraphe de conclusion sur la progression des leçons
4. Sauvegarde ce résumé dans le fichier : ${OUTPUT}
5. Confirme le chemin et la taille du fichier créé.`;

  try {
    const reponse = await agent.run(tache);
    console.log(reponse);
    console.log("\n=== Session 03 terminée avec succès ===");
  } catch (err) {
    console.error("\nErreur :", err.message);
    process.exit(1);
  }
}

main();
