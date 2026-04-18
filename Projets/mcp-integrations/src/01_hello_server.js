/**
 * SESSION 01 — Premier serveur MCP stdio
 * Projet : Claude_Travail — Intégrations MCP
 * Date : 2026-04-11
 *
 * Démonstration minimale : un outil hello_world qui répond depuis MCP.
 * Transport : stdio (compatible Claude Code directement).
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

// Création du serveur MCP
const server = new McpServer({
  name: 'claude-travail',
  version: '0.1.0'
});

/**
 * Outil : hello_world
 * Paramètre : name (string) — le prénom à saluer
 * Retourne  : un message de bienvenue depuis MCP
 */
server.tool(
  'hello_world',
  'Salue une personne depuis le serveur MCP Claude Travail',
  { name: z.string().describe('Prénom ou nom à saluer') },
  async ({ name }) => ({
    content: [
      {
        type: 'text',
        text: `Bonjour ${name} depuis MCP ! Le serveur claude-travail v0.1.0 est opérationnel.`
      }
    ]
  })
);

/**
 * Outil : get_project_info
 * Retourne les informations du projet Claude_Travail
 */
server.tool(
  'get_project_info',
  'Retourne les informations générales du projet Claude_Travail',
  {},
  async () => ({
    content: [
      {
        type: 'text',
        text: JSON.stringify({
          projet: 'Claude_Travail',
          secteur: 'Médico-social français (ESSMS)',
          repertoire: '/Users/utilisateur/kDrive/Claude_Travail/',
          serveur_mcp: 'claude-travail v0.1.0',
          session_courante: '01/10 — Premier serveur MCP stdio',
          outils_disponibles: ['hello_world', 'get_project_info']
        }, null, 2)
      }
    ]
  })
);

// Connexion via transport stdio
const transport = new StdioServerTransport();
await server.connect(transport);
