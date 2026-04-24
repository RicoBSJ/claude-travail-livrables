/**
 * Session 04 — Serveur MCP HTTP (streamable-http)
 * Transport : StreamableHTTPServerTransport sur port 3001
 * Route : POST /mcp
 *
 * Outils exposés :
 *   - hello_world(name)  : salutation (hérité session 01)
 *   - ping()             : vérifie que le serveur répond
 *   - get_date()         : retourne la date du jour
 *   - echo(message)      : répète le message (test de roundtrip)
 *
 * Usage :
 *   node src/04_http_server.js
 *   # Écoute sur http://localhost:3001/mcp
 *
 * Config Claude Code (à ajouter dans ~/.claude/claude.json) :
 *   "mcpServers": {
 *     "claude-travail-http": {
 *       "transport": "http",
 *       "url": "http://localhost:3001/mcp"
 *     }
 *   }
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express from "express";
import { z } from "zod";

// ─── Serveur MCP ──────────────────────────────────────────────────────────────

const server = new McpServer({
  name:    "claude-travail-http",
  version: "0.4.0",
});

// ── Outil 1 : hello_world (hérité session 01) ──
server.tool(
  "hello_world",
  "Retourne un message de bienvenue personnalisé.",
  { name: z.string().describe("Prénom ou identifiant de l'appelant") },
  async ({ name }) => ({
    content: [{ type: "text", text: `Bonjour ${name} ! Serveur MCP HTTP claude-travail v0.4.0 opérationnel.` }],
  })
);

// ── Outil 2 : ping ──
server.tool(
  "ping",
  "Vérifie que le serveur MCP HTTP répond correctement.",
  {},
  async () => ({
    content: [{ type: "text", text: `pong — ${new Date().toISOString()}` }],
  })
);

// ── Outil 3 : get_date ──
server.tool(
  "get_date",
  "Retourne la date et l'heure actuelles du serveur.",
  { format: z.enum(["iso", "fr", "date_only"]).optional().describe("Format : 'iso' (défaut), 'fr' (dd/mm/yyyy hh:mm), 'date_only' (yyyy-mm-dd)") },
  async ({ format = "iso" }) => {
    const now = new Date();
    let result;
    if (format === "fr") {
      result = now.toLocaleString("fr-FR", { timeZone: "Europe/Paris" });
    } else if (format === "date_only") {
      result = now.toISOString().slice(0, 10);
    } else {
      result = now.toISOString();
    }
    return { content: [{ type: "text", text: result }] };
  }
);

// ── Outil 4 : echo ──
server.tool(
  "echo",
  "Répète le message reçu — utile pour tester le roundtrip HTTP et mesurer la latence.",
  {
    message:   z.string().describe("Message à répéter"),
    uppercase: z.boolean().optional().describe("Si true, retourne en majuscules"),
  },
  async ({ message, uppercase = false }) => {
    const out = uppercase ? message.toUpperCase() : message;
    return {
      content: [{ type: "text", text: out }],
    };
  }
);

// ─── Serveur Express ──────────────────────────────────────────────────────────

const app  = express();
const PORT = 3001;

app.use(express.json());

// Stockage des transports par session (clé = session ID)
const transports = new Map();

// Route principale MCP : POST /mcp
app.post("/mcp", async (req, res) => {
  try {
    // Récupérer ou créer un transport pour cette session
    const sessionId = req.headers["mcp-session-id"];

    let transport;
    if (sessionId && transports.has(sessionId)) {
      transport = transports.get(sessionId);
    } else {
      // Nouveau transport HTTP streamable
      transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: () => crypto.randomUUID(),
        onsessioninitialized: (id) => {
          transports.set(id, transport);
          console.log(`[MCP] Nouvelle session : ${id}`);
        },
      });

      // Nettoyage à la fermeture
      transport.onclose = () => {
        if (transport.sessionId) {
          transports.delete(transport.sessionId);
          console.log(`[MCP] Session fermée : ${transport.sessionId}`);
        }
      };

      await server.connect(transport);
    }

    await transport.handleRequest(req, res, req.body);
  } catch (err) {
    console.error("[MCP] Erreur :", err.message);
    if (!res.headersSent) {
      res.status(500).json({ error: "Erreur interne du serveur MCP", message: err.message });
    }
  }
});

// Route GET /mcp pour SSE (events serveur → client)
app.get("/mcp", async (req, res) => {
  const sessionId = req.headers["mcp-session-id"];
  if (!sessionId || !transports.has(sessionId)) {
    res.status(400).json({ error: "Session inconnue" });
    return;
  }
  const transport = transports.get(sessionId);
  await transport.handleRequest(req, res);
});

// Route DELETE /mcp pour fermer une session
app.delete("/mcp", async (req, res) => {
  const sessionId = req.headers["mcp-session-id"];
  if (!sessionId || !transports.has(sessionId)) {
    res.status(404).json({ error: "Session introuvable" });
    return;
  }
  const transport = transports.get(sessionId);
  await transport.handleRequest(req, res);
});

// Route de santé (utile pour monitoring)
app.get("/health", (_req, res) => {
  res.json({
    status:    "ok",
    server:    "claude-travail-http",
    version:   "0.4.0",
    sessions:  transports.size,
    timestamp: new Date().toISOString(),
  });
});

// Démarrage
app.listen(PORT, () => {
  console.log(`\n🚀 Serveur MCP HTTP démarré`);
  console.log(`   URL MCP  : http://localhost:${PORT}/mcp`);
  console.log(`   Santé    : http://localhost:${PORT}/health`);
  console.log(`   Sessions : 0 active(s)`);
  console.log(`\n   Config Claude Code :`);
  console.log(`   "claude-travail-http": {`);
  console.log(`     "transport": "http",`);
  console.log(`     "url": "http://localhost:${PORT}/mcp"`);
  console.log(`   }`);
  console.log(`\n   Outils disponibles : hello_world, ping, get_date, echo\n`);
});
