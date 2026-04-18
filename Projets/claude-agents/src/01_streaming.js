/**
 * Session 01 — Hello Claude API (streaming)
 * Même prompt qu'01_hello.js, mais la réponse s'affiche mot par mot
 * grâce au streaming Server-Sent Events (SSE).
 *
 * Usage : node src/01_streaming.js
 * Prérequis : fichier .env avec ANTHROPIC_API_KEY=sk-ant-...
 */

require("dotenv").config();
const Anthropic = require("@anthropic-ai/sdk");

async function main() {
  const client = new Anthropic.default();

  console.log("Envoi du message à Claude (mode streaming)...\n");
  console.log("Réponse en cours :\n");

  // stream() retourne un AsyncIterable d'événements SSE
  const stream = client.messages.stream({
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

  // Affichage progressif : chaque delta de texte est écrit dans stdout
  for await (const event of stream) {
    if (
      event.type === "content_block_delta" &&
      event.delta.type === "text_delta"
    ) {
      process.stdout.write(event.delta.text);
    }
  }

  // Récupération du message final pour les métadonnées
  const finalMessage = await stream.finalMessage();

  console.log("\n\n--- Métadonnées ---");
  console.log(`Modèle      : ${finalMessage.model}`);
  console.log(`Tokens in   : ${finalMessage.usage.input_tokens}`);
  console.log(`Tokens out  : ${finalMessage.usage.output_tokens}`);
  console.log(`Stop reason : ${finalMessage.stop_reason}`);
}

main().catch((err) => {
  console.error("Erreur :", err.message);
  process.exit(1);
});
