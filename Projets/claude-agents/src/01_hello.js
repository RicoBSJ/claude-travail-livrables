/**
 * Session 01 — Hello Claude API
 * Premier message simple avec le SDK Anthropic.
 *
 * Usage : node src/01_hello.js
 * Prérequis : fichier .env avec ANTHROPIC_API_KEY=sk-ant-...
 */

require("dotenv").config();
const Anthropic = require("@anthropic-ai/sdk");

async function main() {
  // Initialisation du client (la clé est lue depuis process.env.ANTHROPIC_API_KEY)
  const client = new Anthropic.default();

  console.log("Envoi du message à Claude...\n");

  const message = await client.messages.create({
    model: "claude-opus-4-5",
    max_tokens: 512,
    messages: [
      {
        role: "user",
        content:
          "Bonjour Claude ! En 3 phrases, explique ce qu'est un agent IA autonome.",
      },
    ],
  });

  // La réponse se trouve dans message.content[0].text
  const reponse = message.content[0].text;

  console.log("Réponse de Claude :\n");
  console.log(reponse);
  console.log("\n--- Métadonnées ---");
  console.log(`Modèle      : ${message.model}`);
  console.log(`Tokens in   : ${message.usage.input_tokens}`);
  console.log(`Tokens out  : ${message.usage.output_tokens}`);
  console.log(`Stop reason : ${message.stop_reason}`);
}

main().catch((err) => {
  console.error("Erreur :", err.message);
  process.exit(1);
});
