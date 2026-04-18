/**
 * src/lib/tools.js
 * Session 02 — Tool use
 *
 * Définitions réutilisables des outils pour le SDK Anthropic.
 * Chaque outil comprend :
 *   - la définition JSON envoyée à l'API (name, description, input_schema)
 *   - la fonction d'exécution locale correspondante
 */

"use strict";

const fs = require("fs");
const path = require("path");

// ─────────────────────────────────────────────
// 1. Définitions des outils (format API Anthropic)
// ─────────────────────────────────────────────

const TOOL_DEFINITIONS = [
  {
    name: "get_date",
    description:
      "Retourne la date et l'heure actuelles au format ISO 8601. Utile pour horodater des fichiers ou vérifier le contexte temporel.",
    input_schema: {
      type: "object",
      properties: {
        format: {
          type: "string",
          description:
            "Format de sortie : 'iso' (défaut), 'fr' (JJ/MM/AAAA HH:MM), 'date_only'",
          enum: ["iso", "fr", "date_only"],
        },
      },
      required: [],
    },
  },
  {
    name: "read_file",
    description:
      "Lit le contenu d'un fichier texte sur le disque. Retourne le contenu brut ou une erreur si le fichier n'existe pas.",
    input_schema: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description: "Chemin absolu ou relatif du fichier à lire.",
        },
        max_chars: {
          type: "number",
          description:
            "Nombre maximum de caractères à retourner (défaut : 4000).",
        },
      },
      required: ["path"],
    },
  },
  {
    name: "write_file",
    description:
      "Écrit du contenu dans un fichier texte. Crée le fichier s'il n'existe pas, l'écrase sinon.",
    input_schema: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description: "Chemin absolu ou relatif du fichier à écrire.",
        },
        content: {
          type: "string",
          description: "Contenu textuel à écrire dans le fichier.",
        },
      },
      required: ["path", "content"],
    },
  },
];

// ─────────────────────────────────────────────
// 2. Implémentations locales des outils
// ─────────────────────────────────────────────

/**
 * get_date({ format? })
 * Retourne la date courante dans le format demandé.
 */
function get_date({ format = "iso" } = {}) {
  const now = new Date();
  if (format === "fr") {
    const jj = String(now.getDate()).padStart(2, "0");
    const mm = String(now.getMonth() + 1).padStart(2, "0");
    const aaaa = now.getFullYear();
    const hh = String(now.getHours()).padStart(2, "0");
    const min = String(now.getMinutes()).padStart(2, "0");
    return `${jj}/${mm}/${aaaa} ${hh}:${min}`;
  }
  if (format === "date_only") {
    return now.toISOString().split("T")[0];
  }
  // iso par défaut
  return now.toISOString();
}

/**
 * read_file({ path, max_chars? })
 * Lit un fichier texte et retourne son contenu (tronqué si besoin).
 */
function read_file({ path: filePath, max_chars = 4000 }) {
  try {
    const resolved = path.resolve(filePath);
    if (!fs.existsSync(resolved)) {
      return { error: `Fichier introuvable : ${resolved}` };
    }
    const raw = fs.readFileSync(resolved, "utf8");
    const content = raw.length > max_chars ? raw.slice(0, max_chars) + "\n[... tronqué]" : raw;
    return { content, size: raw.length, path: resolved };
  } catch (err) {
    return { error: `Impossible de lire le fichier : ${err.message}` };
  }
}

/**
 * write_file({ path, content })
 * Écrit du texte dans un fichier (crée les répertoires parents si besoin).
 */
function write_file({ path: filePath, content }) {
  try {
    const resolved = path.resolve(filePath);
    fs.mkdirSync(path.dirname(resolved), { recursive: true });
    fs.writeFileSync(resolved, content, "utf8");
    return { success: true, path: resolved, bytes: Buffer.byteLength(content, "utf8") };
  } catch (err) {
    return { error: `Impossible d'écrire le fichier : ${err.message}` };
  }
}

// ─────────────────────────────────────────────
// 3. Dispatcher : exécute un outil par son nom
// ─────────────────────────────────────────────

/**
 * executeTool(name, input)
 * Reçoit le nom et les paramètres d'un tool_use block et retourne le résultat JSON.
 */
function executeTool(name, input) {
  switch (name) {
    case "get_date":
      return get_date(input);
    case "read_file":
      return read_file(input);
    case "write_file":
      return write_file(input);
    default:
      return { error: `Outil inconnu : ${name}` };
  }
}

module.exports = {
  TOOL_DEFINITIONS,
  executeTool,
  get_date,
  read_file,
  write_file,
};
