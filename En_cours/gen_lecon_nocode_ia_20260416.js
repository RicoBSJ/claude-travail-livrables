const {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  AlignmentType, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, ExternalHyperlink,
  UnderlineType, PageBreak, Header, Footer
} = require("docx");
const fs = require("fs");
const path = require("path");

// ─── Palette ───────────────────────────────────────────────────────────────
const BLEU = "1B3A6B";
const BLANC = "FFFFFF";
const GRIS_CLAIR = "EEF2F7";
const LIEN = "1155CC";
const JAUNE_CALLOUT = "FFF8E1";
const JAUNE_BORDER = "F59E0B";
const VERT_CALLOUT = "E8F5E9";
const VERT_BORDER = "22C55E";
const ROUGE_CALLOUT = "FDE8E8";
const ROUGE_BORDER = "EF4444";
const BLEU_CALLOUT = "E8F0FE";

// ─── Helpers ────────────────────────────────────────────────────────────────
function titre(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({
    heading: level,
    spacing: { before: 260, after: 120 },
    children: [
      new TextRun({
        text,
        bold: true,
        color: BLEU,
        font: "Times New Roman",
        size: level === HeadingLevel.HEADING_1 ? 28 : 24,
      }),
    ],
  });
}

function corps(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 100 },
    children: [
      new TextRun({
        text,
        font: "Times New Roman",
        size: 22,
        color: "1F2937",
        bold: opts.bold || false,
        italics: opts.italic || false,
      }),
    ],
  });
}

function lien(texte, url) {
  return new ExternalHyperlink({
    link: url,
    children: [
      new TextRun({
        text: texte,
        font: "Times New Roman",
        size: 22,
        color: LIEN,
        underline: { type: UnderlineType.SINGLE },
      }),
    ],
  });
}

function articleParagraph(titre_art, url, date_art, resume) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [
      new TextRun({ text: "→ ", font: "Times New Roman", size: 22, color: BLEU, bold: true }),
      lien(titre_art, url),
      new TextRun({ text: ` (${date_art}) — `, font: "Times New Roman", size: 22, color: "6B7280", italics: true }),
      new TextRun({ text: resume, font: "Times New Roman", size: 22, color: "1F2937" }),
    ],
  });
}

function callout(lines, bgColor, borderColor, emoji = "💡") {
  const children = lines.map((line, i) =>
    new TextRun({
      text: (i === 0 ? emoji + " " : "    ") + line,
      font: "Times New Roman",
      size: 21,
      color: "1F2937",
      bold: i === 0,
      break: i > 0 ? 1 : 0,
    })
  );
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    indent: { left: 400, right: 400 },
    shading: { type: ShadingType.CLEAR, fill: bgColor },
    border: {
      left: { style: BorderStyle.THICK, size: 12, color: borderColor },
    },
    children,
  });
}

function separateur() {
  return new Paragraph({
    spacing: { before: 200, after: 200 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "D1D5DB" } },
    children: [],
  });
}

function tableauEntetes(headers) {
  return new TableRow({
    tableHeader: true,
    children: headers.map(h =>
      new TableCell({
        shading: { type: ShadingType.CLEAR, fill: BLEU },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({
          children: [new TextRun({ text: h, bold: true, color: BLANC, font: "Times New Roman", size: 20 })]
        })],
      })
    ),
  });
}

function tableauLigne(cells, pair = false) {
  return new TableRow({
    children: cells.map(c =>
      new TableCell({
        shading: { type: ShadingType.CLEAR, fill: pair ? GRIS_CLAIR : BLANC },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        children: [new Paragraph({
          children: [new TextRun({ text: c, font: "Times New Roman", size: 20, color: "1F2937" })]
        })],
      })
    ),
  });
}

function bullet(text, indent = 360) {
  return new Paragraph({
    bullet: { level: 0 },
    indent: { left: indent },
    spacing: { after: 80 },
    children: [new TextRun({ text, font: "Times New Roman", size: 22, color: "1F2937" })],
  });
}

function checkitem(text) {
  return new Paragraph({
    spacing: { after: 80 },
    indent: { left: 360 },
    children: [
      new TextRun({ text: "☐  ", font: "Times New Roman", size: 22, color: BLEU }),
      new TextRun({ text, font: "Times New Roman", size: 22, color: "1F2937" }),
    ],
  });
}

// ─── Document ───────────────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [{
      reference: "default-bullets",
      levels: [{ level: 0, format: "bullet", text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 360, hanging: 180 } } } }],
    }],
  },
  sections: [{
    properties: { page: { margin: { top: 720, bottom: 720, left: 900, right: 900 } } },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "NO-CODE + IA — Leçon 03 | 16 avril 2026", font: "Times New Roman", size: 18, color: "9CA3AF", italics: true })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Produit le 16 avril 2026 — Sources : the-decoder.com · openai.com · n8n.io · make.com · huggingface.co · simonwillison.net · zapier.com · webflow.com", font: "Times New Roman", size: 16, color: "9CA3AF", italics: true })],
        })],
      }),
    },
    children: [

      // ══ TITRE PRINCIPAL ══
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 80 },
        shading: { type: ShadingType.CLEAR, fill: BLEU },
        children: [
          new TextRun({ text: "NO-CODE + IA", font: "Times New Roman", size: 40, bold: true, color: BLANC }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 60 },
        shading: { type: ShadingType.CLEAR, fill: BLEU },
        children: [
          new TextRun({ text: "Leçon 03 — Agents IA & SDK : construire et déployer des agents avec les outils no-code en 2026", font: "Times New Roman", size: 26, color: BLANC }),
        ],
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 300 },
        shading: { type: ShadingType.CLEAR, fill: BLEU },
        children: [
          new TextRun({ text: "Vendredi 16 avril 2026  ·  Règle 20% théorie / 80% pratique", font: "Times New Roman", size: 20, color: "A5C4F0", italics: true }),
        ],
      }),

      // ══ SECTION 1 : ACTU DE LA SEMAINE ══
      titre("📰 Actu de la semaine — Ce que les sources disent"),

      corps("Sources IA", { bold: true }),
      articleParagraph(
        "The next evolution of the Agents SDK",
        "https://openai.com/index/the-next-evolution-of-the-agents-sdk",
        "15 avr. 2026",
        "OpenAI enrichit son Agents SDK avec l'exécution native en sandbox et un harness intégré au modèle, permettant de construire des agents sécurisés et durables manipulant fichiers et outils."
      ),
      articleParagraph(
        "Codex for (almost) everything",
        "https://openai.com/index/codex-for-almost-everything",
        "16 avr. 2026",
        "L'app Codex pour macOS et Windows intègre désormais le computer use, la navigation web, la génération d'images et la mémoire — un outil tout-en-un pour les développeurs."
      ),
      articleParagraph(
        "India's 1.5 million annual IT graduates face an industry that's moving on without them",
        "https://the-decoder.com/indias-1-5-million-annual-it-graduates-face-an-industry-thats-moving-on-without-them/",
        "16 avr. 2026",
        "L'IA agentique bouleverse le secteur IT en Inde : Infosys requalifie ses nouvelles recrues car les universités n'ont pas suivi le rythme de transformation technologique."
      ),
      articleParagraph(
        "Qwen3.6-35B-A3B on my laptop drew a better pelican than Claude Opus 4.7",
        "https://simonwillison.net/2026/Apr/16/qwen-beats-opus/",
        "16 avr. 2026",
        "Simon Willison compare les résultats d'illustration entre le modèle Alibaba Qwen3.6-35B-A3B et Claude Opus 4.7 — un signe que les modèles open-source locaux deviennent sérieusement compétitifs."
      ),

      corps("Sources NO-CODE", { bold: true }),
      articleParagraph(
        "We need to re-learn what AI agent development tools are in 2026",
        "https://blog.n8n.io/we-need-re-learn-what-ai-agent-development-tools-are-in-2026/",
        "avr. 2026",
        "n8n analyse comment la définition même des outils de développement d'agents IA a changé en 2026, entre orchestration, chorégraphie et automatisation classique."
      ),
      articleParagraph(
        "Workflow Automation vs. Orchestration: Architectural Differences That Matter at Scale",
        "https://blog.n8n.io/workflow-vs-orchestration/",
        "14 avr. 2026",
        "L'automatisation de workflow gère des tâches individuelles ; l'orchestration coordonne plusieurs tâches en processus bout-en-bout — une distinction clé pour choisir son outil."
      ),
      articleParagraph(
        "The real reason your AI projects stall — and what hundreds of companies taught us",
        "https://www.make.com/en/blog/the-real-reason-your-ai-projects-stall",
        "14 avr. 2026",
        "Make partage les obstacles récurrents à l'implémentation IA dans des centaines d'organisations et propose le Make AI Playbook comme ressource pratique."
      ),
      articleParagraph(
        "Introducing Webflow AEO: an agentic, closed-loop system for AI discovery",
        "https://webflowmarketingmain.com/blog/introducing-webflow-aeo",
        "avr. 2026",
        "Webflow lance AEO, un système agentique en boucle fermée qui mesure comment votre marque apparaît dans les réponses des IA et formule des recommandations directement dans l'interface."
      ),

      separateur(),

      // ══ SECTION 2 : THÉORIE ══
      titre("🔬 Théorie (20%) — Agents IA : définitions et architecture 2026"),

      callout([
        "À retenir : un agent IA = modèle + outils + boucle d'exécution + mémoire",
        "Ce n'est pas juste un chatbot. C'est un système qui perçoit, décide et agit de façon autonome.",
      ], BLEU_CALLOUT, BLEU, "🤖"),

      corps("Les trois couches d'un agent en 2026", { bold: true }),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: [
          tableauEntetes(["Couche", "Rôle", "Exemple d'outil"]),
          tableauLigne(["Perception", "Lire l'environnement (fichiers, web, API)", "WebFetch, read_file, MCP resource"], false),
          tableauLigne(["Décision", "Raisonner et choisir l'action suivante", "LLM (GPT-5, Claude, Qwen)"], true),
          tableauLigne(["Action", "Exécuter : écrire, envoyer, déclencher", "write_file, HTTP POST, n8n webhook"], false),
        ],
      }),

      corps(""),
      corps("Orchestration vs Chorégraphie vs Automatisation", { bold: true }),
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        rows: [
          tableauEntetes(["Approche", "Principe", "Outil typique"]),
          tableauLigne(["Automatisation classique", "Si A alors B (règle fixe)", "Zapier, Make"], false),
          tableauLigne(["Orchestration", "Un chef d'orchestre dirige des sous-agents", "OpenAI Agents SDK, n8n"], true),
          tableauLigne(["Chorégraphie", "Chaque agent décide lui-même de son prochain rôle", "Multi-agents distribués"], false),
        ],
      }),

      corps(""),
      callout([
        "Pourquoi les projets IA stagnent (Make, avr. 2026) :",
        "1. Objectif flou — on automatise pour automatiser, pas pour résoudre un problème réel",
        "2. Données mal structurées — l'agent ne sait pas quoi chercher",
        "3. Absence de boucle de feedback — l'agent n'apprend pas de ses erreurs",
      ], JAUNE_CALLOUT, JAUNE_BORDER, "⚠️"),

      separateur(),

      // ══ SECTION 3 : EXERCICES ══
      titre("🛠️ Exercices pratiques (80%)"),

      // Exercice 1
      titre("Exercice 1 — Créer son premier agent n8n avec boucle d'orchestration", HeadingLevel.HEADING_2),
      corps("Durée estimée : 25 min | Niveau : débutant-intermédiaire | Outil : n8n (self-hosted ou cloud)"),
      corps(""),
      callout([
        "Objectif : construire un agent n8n qui lit un dossier, résume chaque fichier texte et envoie le résumé par webhook.",
      ], VERT_CALLOUT, VERT_BORDER, "🎯"),
      corps(""),
      corps("Étapes :", { bold: true }),
      checkitem("Ouvrir n8n → New Workflow → ajouter un nœud « Manual Trigger »"),
      checkitem("Ajouter un nœud « Read/Write Files from Disk » → chemin : /data/docs/"),
      checkitem("Ajouter un nœud « AI Agent » → choisir le modèle (GPT-5 mini ou Claude claude-haiku-4-5)"),
      checkitem("Dans le prompt système : « Tu es un assistant de synthèse. Résume ce document en 5 points clés. »"),
      checkitem("Ajouter un nœud « HTTP Request » → POST vers votre webhook (ex. webhook.site)"),
      checkitem("Exécuter le workflow et vérifier la réception des résumés"),
      corps(""),
      corps("Variante avancée :", { bold: true }),
      bullet("Remplacer le webhook par un nœud « Write to File » pour sauvegarder les résumés en .txt"),
      bullet("Ajouter un nœud « If » pour ignorer les fichiers de moins de 100 mots"),

      corps(""),
      // Exercice 2
      titre("Exercice 2 — Construire un agent Make avec le AI Playbook comme guide", HeadingLevel.HEADING_2),
      corps("Durée estimée : 30 min | Niveau : intermédiaire | Outil : Make.com"),
      corps(""),
      callout([
        "Objectif : créer un scénario Make qui détecte une nouvelle publication sur un blog RSS, la résume avec l'IA et l'enregistre dans une Google Sheet.",
      ], VERT_CALLOUT, VERT_BORDER, "🎯"),
      corps(""),
      checkitem("Dans Make → Créer un scénario → ajouter module « RSS Feed » → URL : https://blog.n8n.io/feed/"),
      checkitem("Ajouter module « OpenAI » ou « Anthropic » → action : Create a completion"),
      checkitem("Prompt : « Résume cet article en 3 phrases et donne-lui une note d'intérêt /5 : {{title}} — {{description}} »"),
      checkitem("Ajouter module « Google Sheets » → Add a Row → colonnes : Titre | URL | Résumé | Note | Date"),
      checkitem("Planifier le scénario : toutes les 24h"),
      checkitem("Tester manuellement avec le bouton « Run once »"),
      corps(""),
      corps("Points de vigilance Make :", { bold: true }),
      bullet("Vérifier les quotas API de votre abonnement Make (opérations/mois)"),
      bullet("Utiliser « Error Handler » pour capturer les timeouts de l'API IA"),

      corps(""),
      // Exercice 3
      titre("Exercice 3 — Tester l'OpenAI Agents SDK en local (Node.js)", HeadingLevel.HEADING_2),
      corps("Durée estimée : 35 min | Niveau : intermédiaire-avancé | Outil : Node.js + OpenAI SDK"),
      corps(""),
      callout([
        "Objectif : reproduire localement l'architecture Agents SDK présentée par OpenAI cette semaine — un agent avec sandbox et outil de lecture de fichier.",
      ], VERT_CALLOUT, VERT_BORDER, "🎯"),
      corps(""),
      corps("Code de base (à saisir dans agent_sdk_test.js) :", { bold: true }),
      new Paragraph({
        spacing: { before: 100, after: 100 },
        shading: { type: ShadingType.CLEAR, fill: "F3F4F6" },
        children: [
          new TextRun({ text: "import OpenAI from 'openai';", font: "Courier New", size: 18, color: "1F2937", break: 0 }),
          new TextRun({ text: "import fs from 'fs';", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "", break: 1 }),
          new TextRun({ text: "const client = new OpenAI();", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "", break: 1 }),
          new TextRun({ text: "// Définir l'outil read_file", font: "Courier New", size: 18, color: "6B7280", break: 1 }),
          new TextRun({ text: "const tools = [{ type: 'function', function: {", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "  name: 'read_file',", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "  description: 'Lit le contenu d un fichier local',", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "  parameters: { type: 'object', properties: {", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    path: { type: 'string', description: 'Chemin du fichier' }", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "  }, required: ['path'] }", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "}}];", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "", break: 1 }),
          new TextRun({ text: "// Boucle agentique", font: "Courier New", size: 18, color: "6B7280", break: 1 }),
          new TextRun({ text: "async function runAgent(task) {", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "  const messages = [{ role: 'user', content: task }];", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "  while (true) {", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    const res = await client.chat.completions.create({", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "      model: 'gpt-4.5-mini', messages, tools });", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    const choice = res.choices[0];", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    if (choice.finish_reason === 'stop') {", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "      return choice.message.content; }", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    // Exécuter l outil", font: "Courier New", size: 18, color: "6B7280", break: 1 }),
          new TextRun({ text: "    const call = choice.message.tool_calls[0];", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    const { path } = JSON.parse(call.function.arguments);", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    const content = fs.readFileSync(path, 'utf8');", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    messages.push(choice.message,", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "      { role: 'tool', tool_call_id: call.id, content });", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "  }", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "}", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "", break: 1 }),
          new TextRun({ text: "runAgent('Lis le fichier README.md et fais-en un résumé').then(console.log);", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
        ],
      }),
      corps(""),
      checkitem("Installer : npm install openai"),
      checkitem("Configurer OPENAI_API_KEY dans .env"),
      checkitem("Créer un fichier README.md de test dans le même dossier"),
      checkitem("Exécuter : node agent_sdk_test.js"),
      checkitem("Observer dans le terminal les tool_calls et la réponse finale"),
      corps(""),
      callout([
        "Sandbox OpenAI (nouveauté avr. 2026) : dans l'interface Codex, vous pouvez tester vos agents directement sans déployer — idéal pour valider la boucle avant production.",
      ], BLEU_CALLOUT, BLEU, "🆕"),

      separateur(),

      // ══ SECTION 4 : CHALLENGE ══
      titre("🎯 Challenge de la semaine — Agent de veille no-code autonome"),

      callout([
        "Niveau : avancé | Durée : 60 à 90 min | Combinaison : n8n + IA + webhook + fichier",
      ], GRIS_CLAIR, BLEU, "⏱️"),

      corps("Objectif final :", { bold: true }),
      corps("Construire un agent no-code complet qui, chaque vendredi, récupère les 3 derniers articles de n8n.io et the-decoder.com, les résume avec un LLM, et génère un fichier Markdown de veille horodaté."),
      corps(""),
      corps("Architecture cible :", { bold: true }),

      new Paragraph({
        spacing: { before: 80, after: 80 },
        shading: { type: ShadingType.CLEAR, fill: "F3F4F6" },
        children: [
          new TextRun({ text: "Trigger (Cron vendredi 8h) → RSS Fetch (n8n + The Decoder)", font: "Courier New", size: 18, color: "1F2937", break: 0 }),
          new TextRun({ text: "    → LLM Summarize (prompt: 3 points clés + note /5)", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    → Merge Results → Format Markdown", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    → Write File (YYYY-MM-DD_veille_challenge.md)", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
          new TextRun({ text: "    → Notify (webhook ou email)", font: "Courier New", size: 18, color: "1F2937", break: 1 }),
        ],
      }),

      corps(""),
      corps("Critères de réussite :", { bold: true }),
      checkitem("Le fichier Markdown est créé avec la date du jour dans le nom"),
      checkitem("Chaque article a un résumé de 3 points clés et une note /5"),
      checkitem("L'agent s'exécute sans intervention manuelle"),
      checkitem("En cas d'erreur RSS, l'agent envoie une alerte et ne plante pas"),
      checkitem("BONUS : ajouter une section 'À surveiller la semaine prochaine'"),

      corps(""),
      callout([
        "Inspiration : ce challenge reproduit exactement le job 'nocode-ia-veille' de ce projet — vous avez déjà le modèle sous les yeux !",
      ], VERT_CALLOUT, VERT_BORDER, "💡"),

      separateur(),

      // ══ SECTION 5 : RESSOURCES ══
      titre("📚 Ressources de référence"),

      new Paragraph({
        spacing: { after: 100 },
        children: [
          new TextRun({ text: "OpenAI Agents SDK — documentation officielle : ", font: "Times New Roman", size: 22, color: "1F2937" }),
          lien("platform.openai.com/docs/agents", "https://platform.openai.com/docs/agents"),
        ],
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [
          new TextRun({ text: "n8n — Guide Workflow vs Orchestration : ", font: "Times New Roman", size: 22, color: "1F2937" }),
          lien("blog.n8n.io/workflow-vs-orchestration", "https://blog.n8n.io/workflow-vs-orchestration/"),
        ],
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [
          new TextRun({ text: "Make AI Playbook : ", font: "Times New Roman", size: 22, color: "1F2937" }),
          lien("make.com/en/blog/the-real-reason-your-ai-projects-stall", "https://www.make.com/en/blog/the-real-reason-your-ai-projects-stall"),
        ],
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [
          new TextRun({ text: "Webflow AEO (IA Discovery) : ", font: "Times New Roman", size: 22, color: "1F2937" }),
          lien("webflowmarketingmain.com/blog/introducing-webflow-aeo", "https://webflowmarketingmain.com/blog/introducing-webflow-aeo"),
        ],
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [
          new TextRun({ text: "Simon Willison — Qwen vs Claude Opus 4.7 : ", font: "Times New Roman", size: 22, color: "1F2937" }),
          lien("simonwillison.net/2026/Apr/16/qwen-beats-opus", "https://simonwillison.net/2026/Apr/16/qwen-beats-opus/"),
        ],
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [
          new TextRun({ text: "Hugging Face Blog : ", font: "Times New Roman", size: 22, color: "1F2937" }),
          lien("huggingface.co/blog", "https://huggingface.co/blog"),
        ],
      }),

      separateur(),

      // ══ SECTION 6 : À SURVEILLER ══
      titre("🔜 À surveiller la semaine prochaine"),

      bullet("L'évolution de l'OpenAI Agents SDK : nouveaux outils natifs annoncés (computer use, mémoire longue)"),
      bullet("La réponse de Anthropic à la vague Agents SDK : mise à jour du Claude Agent SDK"),
      bullet("n8n vs Make 2026 : la bataille des plateformes d'orchestration no-code s'intensifie"),
      bullet("AEO (Agent Engine Optimization) : nouveau champ de la visibilité IA pour les sites web"),
      bullet("Les modèles locaux (Qwen, Mistral) qui dépassent les modèles cloud sur certaines tâches"),

      corps(""),
      callout([
        "La semaine prochaine : Leçon 04 — à définir selon l'actualité du vendredi 23 avril 2026.",
        "Restez attentif à : openai.com/blog · the-decoder.com · blog.n8n.io",
      ], GRIS_CLAIR, BLEU, "📅"),

    ],
  }],
});

// ─── Export ─────────────────────────────────────────────────────────────────
Packer.toBuffer(doc).then(buffer => {
  const outputPath = "/Users/utilisateur/kDrive/Claude_Travail/Livrables/Leçons/2026-04-16_lecon-nocode-ia_03_agents-sdk-no-code-2026.docx";
  fs.writeFileSync(outputPath, buffer);
  const size = Math.round(buffer.length / 1024);
  console.log("Leçon générée : " + outputPath);
  console.log("Taille : " + size + " Ko");
}).catch(err => {
  console.error("Erreur :", err);
  process.exit(1);
});
