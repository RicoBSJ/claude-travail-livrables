/**
 * SESSION 02 — Resources MCP
 * Projet : Claude_Travail — Intégrations MCP
 * Date : 2026-04-13
 *
 * Expose les livrables du projet Claude_Travail comme ressources MCP.
 * Chaque catégorie est accessible via une URI livrables://<categorie>.
 * Transport : stdio (compatible Claude Code directement).
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import fs from 'fs';
import path from 'path';

// Répertoire racine du projet
const PROJECT_ROOT = '/Users/utilisateur/kDrive/Claude_Travail';

// Mapping des catégories de ressources
const CATEGORIES = {
  quiz: {
    dir: path.join(PROJECT_ROOT, 'Livrables', 'Quiz'),
    extensions: ['.pptx'],
    description: 'Quiz PowerPoint RBPP/TNmP/CNT'
  },
  infographies: {
    dir: path.join(PROJECT_ROOT, 'Livrables', 'Infographies'),
    extensions: ['.pptx'],
    description: 'Infographies PowerPoint (format pétale)'
  },
  lecons: {
    dir: path.join(PROJECT_ROOT, 'Livrables', 'Leçons'),
    extensions: ['.docx'],
    description: 'Leçons hebdomadaires NO-CODE + IA'
  },
  veilles: {
    dir: path.join(PROJECT_ROOT, 'Sources', 'Veille'),
    extensions: ['.docx', '.md'],
    description: 'Veilles HAS/ANESM et SERAFIN-PH'
  },
  documents: {
    dir: path.join(PROJECT_ROOT, 'Livrables', 'Documents'),
    extensions: ['.docx', '.pdf'],
    description: 'Documents Word et PDF divers'
  }
};

/**
 * Scanne un répertoire et retourne les métadonnées des fichiers
 * @param {string} dir - Chemin du répertoire
 * @param {string[]} extensions - Extensions à inclure (ex: ['.pptx', '.docx'])
 * @returns {Array} - Liste d'objets { name, path, size, date, extension }
 */
function scanDirectory(dir, extensions) {
  if (!fs.existsSync(dir)) {
    return [];
  }

  const files = fs.readdirSync(dir);
  return files
    .filter(f => extensions.some(ext => f.toLowerCase().endsWith(ext)))
    .map(f => {
      const fullPath = path.join(dir, f);
      const stats = fs.statSync(fullPath);
      return {
        name: f,
        path: fullPath,
        size: stats.size,
        size_kb: Math.round(stats.size / 1024),
        date: stats.mtime.toISOString().split('T')[0],
        extension: path.extname(f).toLowerCase()
      };
    })
    .sort((a, b) => b.date.localeCompare(a.date)); // Plus récent en premier
}

// ─── Création du serveur MCP ───────────────────────────────────────────────
const server = new McpServer({
  name: 'claude-travail-resources',
  version: '0.2.0'
});

// ─── RESOURCES : une par catégorie de livrables ───────────────────────────

/**
 * Resource : livrables://quiz
 * Retourne la liste des quiz PowerPoint disponibles
 */
server.resource(
  'livrables-quiz',
  'livrables://quiz',
  async (uri) => {
    const cat = CATEGORIES.quiz;
    const files = scanDirectory(cat.dir, cat.extensions);
    const content = JSON.stringify({
      categorie: 'quiz',
      description: cat.description,
      repertoire: cat.dir,
      total: files.length,
      fichiers: files
    }, null, 2);
    return {
      contents: [{ uri: uri.href, mimeType: 'application/json', text: content }]
    };
  }
);

/**
 * Resource : livrables://infographies
 * Retourne la liste des infographies PowerPoint disponibles
 */
server.resource(
  'livrables-infographies',
  'livrables://infographies',
  async (uri) => {
    const cat = CATEGORIES.infographies;
    const files = scanDirectory(cat.dir, cat.extensions);
    const content = JSON.stringify({
      categorie: 'infographies',
      description: cat.description,
      repertoire: cat.dir,
      total: files.length,
      fichiers: files
    }, null, 2);
    return {
      contents: [{ uri: uri.href, mimeType: 'application/json', text: content }]
    };
  }
);

/**
 * Resource : livrables://lecons
 * Retourne la liste des leçons NO-CODE + IA disponibles
 */
server.resource(
  'livrables-lecons',
  'livrables://lecons',
  async (uri) => {
    const cat = CATEGORIES.lecons;
    const files = scanDirectory(cat.dir, cat.extensions);
    const content = JSON.stringify({
      categorie: 'lecons',
      description: cat.description,
      repertoire: cat.dir,
      total: files.length,
      fichiers: files
    }, null, 2);
    return {
      contents: [{ uri: uri.href, mimeType: 'application/json', text: content }]
    };
  }
);

/**
 * Resource : livrables://veilles
 * Retourne la liste des veilles disponibles (HAS, SERAFIN-PH, etc.)
 */
server.resource(
  'livrables-veilles',
  'livrables://veilles',
  async (uri) => {
    const cat = CATEGORIES.veilles;
    const files = scanDirectory(cat.dir, cat.extensions);
    const content = JSON.stringify({
      categorie: 'veilles',
      description: cat.description,
      repertoire: cat.dir,
      total: files.length,
      fichiers: files
    }, null, 2);
    return {
      contents: [{ uri: uri.href, mimeType: 'application/json', text: content }]
    };
  }
);

/**
 * Resource : livrables://documents
 * Retourne la liste des documents Word/PDF divers
 */
server.resource(
  'livrables-documents',
  'livrables://documents',
  async (uri) => {
    const cat = CATEGORIES.documents;
    const files = scanDirectory(cat.dir, cat.extensions);
    const content = JSON.stringify({
      categorie: 'documents',
      description: cat.description,
      repertoire: cat.dir,
      total: files.length,
      fichiers: files
    }, null, 2);
    return {
      contents: [{ uri: uri.href, mimeType: 'application/json', text: content }]
    };
  }
);

// ─── TOOLS : outils complémentaires aux resources ─────────────────────────

/**
 * Outil : hello_world (hérité session 01)
 */
server.tool(
  'hello_world',
  'Salue une personne depuis le serveur MCP Claude Travail',
  { name: z.string().describe('Prénom ou nom à saluer') },
  async ({ name }) => ({
    content: [
      {
        type: 'text',
        text: `Bonjour ${name} depuis MCP ! Le serveur claude-travail-resources v0.2.0 est opérationnel.`
      }
    ]
  })
);

/**
 * Outil : list_all_livrables
 * Retourne un résumé de toutes les catégories en une seule requête
 */
server.tool(
  'list_all_livrables',
  'Retourne un résumé de tous les livrables disponibles par catégorie',
  {},
  async () => {
    const summary = {};
    for (const [key, cat] of Object.entries(CATEGORIES)) {
      const files = scanDirectory(cat.dir, cat.extensions);
      summary[key] = {
        description: cat.description,
        total: files.length,
        dernier: files[0]?.name ?? 'aucun',
        date_dernier: files[0]?.date ?? null
      };
    }
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(summary, null, 2)
        }
      ]
    };
  }
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
          repertoire: PROJECT_ROOT,
          serveur_mcp: 'claude-travail-resources v0.2.0',
          session_courante: '02/10 — Resources MCP',
          resources_disponibles: [
            'livrables://quiz',
            'livrables://infographies',
            'livrables://lecons',
            'livrables://veilles',
            'livrables://documents'
          ],
          outils_disponibles: ['hello_world', 'list_all_livrables', 'get_project_info']
        }, null, 2)
      }
    ]
  })
);

// ─── Connexion via transport stdio ────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);
