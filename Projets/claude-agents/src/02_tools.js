/**
 * Session 02 — Tool use
 * Démonstration complète du mécanisme tool_use de l'API Anthropic.
 *
 * Ce script illustre :
 *   1. Comment déclarer des outils dans la requête API
 *   2. La boucle de réponse : message → tool_call → résultat → message final
 *   3. Un exemple concret : Claude lit un fichier et en produit un résumé
 *
 * Usage : node src/02_tools.js
 * Prérequis : .env avec ANTHROPIC_API_KEY
 */

"use strict";

require("dotenv").config();
const Anthropic = require("@anthropic-ai/sdk");
const { TOOL_DEFINITIONS, executeTool } = require("./lib/tools");

const client = new Anthropic.default();

// ─────────────────────────────────────────────
// Boucle tool_use générique
// ─────────────────────────────────────────────

/**
 * runWithTools(messages, systemPrompt?)
 *
 * Envoie les messages à Claude avec les outils disponibles.
 * Si Claude répond avec un ou plusieurs tool_use blocks, exécute chaque outil
 * localement, ajoute les résultats comme tool_result et renvoie la requête.
 * Répète jusqu'à obtenir une réponse texte finale (stop_reason !== "tool_use").
 *
 * @param {Array}  messages      - Historique de conversation Anthropic
 * @param {string} systemPrompt  - Prompt système optionnel
 * @returns {string}             - Texte final de Claude
 */
async function runWithTools(messages, systemPrompt = "") {
  let iteration = 0;
  const MAX_ITERATIONS = 10; // sécurité anti-boucle infinie

  while (iteration < MAX_ITERATIONS) {
    iteration++;
    console.log(`\n[Itération ${iteration}] Envoi à Claude...`);

    const params = {
      model: "claude-opus-4-5",
      max_tokens: 1024,
      tools: TOOL_DEFINITIONS,
      messages,
    };
    if (systemPrompt) params.system = systemPrompt;

    const response = await client.messages.create(params);

    console.log(`  stop_reason : ${response.stop_reason}`);
    console.log(`  content blocks : ${response.content.length}`);

    // Ajouter la réponse de l'assistant à l'historique
    messages.push({ role: "assistant", content: response.content });

    // Si Claude a fini de répondre (pas d'outil à appeler), on s'arrête
    if (response.stop_reason !== "tool_use") {
      // Extraire le texte final
      const textBlock = response.content.find((b) => b.type === "text");
      return textBlock ? textBlock.text : "(pas de texte)";
    }

    // --- Claude veut utiliser un ou plusieurs outils ---
    const toolResults = [];

    for (const block of response.content) {
      if (block.type !== "tool_use") continue;

      const toolName = block.name;
      const toolInput = block.input;

      console.log(`  --> Appel outil : ${toolName}`);
      console.log(`      Paramètres : ${JSON.stringify(toolInput)}`);

      const result = executeTool(toolName, toolInput);
      const resultText = JSON.stringify(result, null, 2);

      console.log(`      Résultat   : ${resultText.slice(0, 120)}...`);

      toolResults.push({
        type: "tool_result",
        tool_use_id: block.id,
        content: resultText,
      });
    }

    // Ajouter les résultats des outils dans l'historique
    messages.push({ role: "user", content: toolResults });
  }

  throw new Error(`Boucle tool_use : limite de ${MAX_ITERATIONS} itérations atteinte.`);
}

// ─────────────────────────────────────────────
// Démonstration 1 : get_date
// ─────────────────────────────────────────────

async function demo_date() {
  console.log("\n========================================");
  console.log("DÉMO 1 — Obtenir la date courante");
  console.log("========================================");

  const messages = [
    {
      role: "user",
      content:
        "Quelle est la date d'aujourd'hui ? Utilise l'outil get_date pour obtenir la réponse exacte, au format français.",
    },
  ];

  const reponse = await runWithTools(messages);
  console.log("\n[Réponse finale de Claude]");
  console.log(reponse);
}

// ─────────────────────────────────────────────
// Démonstration 2 : read_file + résumé
// ─────────────────────────────────────────────

async function demo_lire_et_resumer() {
  console.log("\n========================================");
  console.log("DÉMO 2 — Lire un fichier et le résumer");
  console.log("========================================");

  // On utilise le script lui-même comme cobaye (pas de données sensibles)
  const filePath = __filename;

  const messages = [
    {
      role: "user",
      content: `Lis le fichier suivant avec l'outil read_file, puis fais-en un résumé de 3 à 5 phrases en français, en expliquant ce que ce script fait :
Fichier : ${filePath}`,
    },
  ];

  const systemPrompt =
    "Tu es un assistant technique expert Node.js et API Claude. Tu réponds toujours en français professionnel.";

  const reponse = await runWithTools(messages, systemPrompt);
  console.log("\n[Résumé produit par Claude]");
  console.log(reponse);
}

// ─────────────────────────────────────────────
// Démonstration 3 : write_file (écriture d'un résumé)
// ─────────────────────────────────────────────

async function demo_ecrire_fichier() {
  console.log("\n========================================");
  console.log("DÉMO 3 — Écrire un résumé dans un fichier");
  console.log("========================================");

  const outputPath = "/Users/utilisateur/kDrive/Claude_Travail/En_cours/session02_note.txt";

  const messages = [
    {
      role: "user",
      content: `D'abord, utilise get_date (format 'fr') pour obtenir la date et l'heure actuelles.
Ensuite, utilise write_file pour créer un fichier à ce chemin : ${outputPath}
Le contenu du fichier doit être :
---
Note de session — Tool use
Créée le : [date obtenue avec get_date]

Ce fichier démontre l'outil write_file :
Claude peut lire et écrire des fichiers sur le système de fichiers local
grâce aux outils définis dans src/lib/tools.js.

Prochaine session : Agent basique (boucle agentique autonome).
---

Remplace [date obtenue avec get_date] par la valeur réelle.
Confirme ensuite le chemin et la taille du fichier créé.`,
    },
  ];

  const reponse = await runWithTools(messages);
  console.log("\n[Confirmation de Claude]");
  console.log(reponse);
}

// ─────────────────────────────────────────────
// Exécution des 3 démos
// ─────────────────────────────────────────────

async function main() {
  console.log("=== Session 02 — Tool use ===");
  console.log("Outils disponibles :", TOOL_DEFINITIONS.map((t) => t.name).join(", "));

  try {
    await demo_date();
    await demo_lire_et_resumer();
    await demo_ecrire_fichier();

    console.log("\n=== Session 02 terminée avec succès ===");
  } catch (err) {
    console.error("\nErreur :", err.message);
    if (err.status) console.error("Code HTTP :", err.status);
    process.exit(1);
  }
}

main();
