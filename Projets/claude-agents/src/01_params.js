/**
 * Session 01 — Jouer avec les paramètres
 * Démontre l'effet de temperature, max_tokens et system prompt
 * en envoyant la même question avec 3 configurations différentes.
 *
 * Usage : node src/01_params.js
 * Prérequis : fichier .env avec ANTHROPIC_API_KEY=sk-ant-...
 */

require("dotenv").config();
const Anthropic = require("@anthropic-ai/sdk");

const client = new Anthropic.default();

/**
 * Envoie un message avec des paramètres personnalisés et affiche la réponse.
 * @param {string} label       - Libellé de la configuration pour l'affichage
 * @param {object} params      - Paramètres de l'appel API
 */
async function testerConfig(label, params) {
  console.log(`\n${"=".repeat(60)}`);
  console.log(`CONFIG : ${label}`);
  console.log("=".repeat(60));

  const message = await client.messages.create({
    model: "claude-opus-4-5",
    messages: [
      {
        role: "user",
        content: "Décris l'IA agentique en 2 phrases maximum.",
      },
    ],
    ...params,
  });

  console.log("\nRéponse :");
  console.log(message.content[0].text);
  console.log(
    `\n[temperature=${params.temperature ?? "(défaut)"}  max_tokens=${params.max_tokens}  system="${(params.system ?? "").slice(0, 40)}..."]`
  );
  console.log(
    `[Tokens : in=${message.usage.input_tokens}, out=${message.usage.output_tokens}]`
  );
}

async function main() {
  // --- Configuration 1 : réponse précise (temperature basse) ---
  await testerConfig("Précis (temperature=0.1)", {
    max_tokens: 150,
    temperature: 0.1,
    system:
      "Tu es un expert en IA. Réponds de façon technique et concise en français.",
  });

  // --- Configuration 2 : réponse créative (temperature haute) ---
  await testerConfig("Créatif (temperature=1.0)", {
    max_tokens: 150,
    temperature: 1.0,
    system: "Tu es un vulgarisateur enthousiaste. Utilise des métaphores simples.",
  });

  // --- Configuration 3 : réponse très courte (max_tokens limité) ---
  await testerConfig("Ultra-concis (max_tokens=30)", {
    max_tokens: 30,
    temperature: 0.5,
    system: "Réponds en une seule phrase très courte.",
  });

  console.log("\n✅ Démonstration des paramètres terminée.");
}

main().catch((err) => {
  console.error("Erreur :", err.message);
  process.exit(1);
});
