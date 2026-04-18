/**
 * SESSION 03 — Prompts MCP
 * Projet : Claude_Travail — Intégrations MCP
 * Date : 2026-04-16
 *
 * Expose des templates de prompts réutilisables via le protocole MCP.
 * Ces prompts permettent à Claude Code d'analyser des RBPP, générer des
 * quiz, synthétiser des veilles et produire des bilans hebdomadaires.
 *
 * Transport : stdio (compatible Claude Code directement).
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import fs from 'fs';
import path from 'path';

// Répertoire racine du projet
const PROJECT_ROOT = '/Users/utilisateur/kDrive/Claude_Travail';

// ─── Création du serveur MCP ───────────────────────────────────────────────
const server = new McpServer({
  name: 'claude-travail-prompts',
  version: '0.3.0'
});

// ─── TOOLS hérités des sessions précédentes ───────────────────────────────

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
        text: `Bonjour ${name} depuis MCP ! Serveur claude-travail-prompts v0.3.0 opérationnel.`
      }
    ]
  })
);

/**
 * Outil : get_project_info (hérité session 02)
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
          serveur_mcp: 'claude-travail-prompts v0.3.0',
          session_courante: '03/10 — Prompts MCP',
          prompts_disponibles: [
            'analyser_rbpp',
            'generer_quiz',
            'synthese_veille',
            'bilan_semaine',
            'analyser_temoignage',
            'rediger_fiche_rbpp',
            'evaluer_pratique'
          ]
        }, null, 2)
      }
    ]
  })
);

// ─── PROMPTS MCP ───────────────────────────────────────────────────────────

/**
 * Prompt : analyser_rbpp
 * Analyse une RBPP HAS à partir de son URL et extrait les éléments clés
 * pour les professionnels du médico-social.
 */
server.prompt(
  'analyser_rbpp',
  {
    url: z.string().url().describe('URL de la RBPP HAS à analyser'),
    public_cible: z.string().optional().describe('Public cible spécifique (ex: FAM, MAS, SAVS)')
  },
  ({ url, public_cible }) => ({
    messages: [
      {
        role: 'user',
        content: {
          type: 'text',
          text: `Tu es un expert des recommandations de bonnes pratiques professionnelles (RBPP) de la HAS, spécialisé dans le secteur médico-social français (ESSMS : foyers de vie, FAM, MAS, SAVS, SAMSAH).

Analyse la RBPP disponible à cette URL : ${url}

${public_cible ? `Public cible prioritaire pour cette analyse : ${public_cible}` : ''}

Produis une analyse structurée en suivant exactement ce plan :

## 1. Identification
- Titre complet de la RBPP
- Date de publication
- Organisme(s) émetteur(s) (HAS, ANESM, etc.)
- Public(s) cible(s) officiel(s)
- Thématique principale (bientraitance / autodétermination / habitat / troubles du comportement / autre)

## 2. Résumé exécutif (5-7 lignes)
Synthèse accessible, registre professionnel médico-social.

## 3. Recommandations principales
Tableau : N° | Libellé de la recommandation | Grade (A/B/C/AE) | Niveau de preuve

## 4. Points de vigilance pour ESSMS
Tableau : ⚠️ Point de vigilance | Contexte pratique | Risque si non appliqué

## 5. Implications concrètes par type d'établissement
- Foyer de vie / FAM : [implications]
- MAS : [implications]
- SAVS / SAMSAH : [implications]

## 6. Indicateurs de mise en œuvre
Liste de 5-8 indicateurs mesurables permettant d'évaluer l'application de la RBPP.

## 7. Ressources complémentaires
Autres RBPP liées, outils HAS associés, liens utiles.

Format de réponse : markdown structuré, registre professionnel, sans jargon excessif.`
        }
      }
    ]
  })
);

/**
 * Prompt : generer_quiz
 * Génère des questions QCM sur un thème médico-social donné
 */
server.prompt(
  'generer_quiz',
  {
    theme: z.string().describe('Thème du quiz (ex: bientraitance, autodétermination, PBS)'),
    nb: z.number().int().min(5).max(100).default(10).describe('Nombre de questions à générer'),
    niveau: z.enum(['debutant', 'intermediaire', 'expert']).default('intermediaire').describe('Niveau de difficulté'),
    source: z.string().optional().describe('Source RBPP ou document de référence')
  },
  ({ theme, nb, niveau, source }) => ({
    messages: [
      {
        role: 'user',
        content: {
          type: 'text',
          text: `Tu es un formateur expert en médico-social, spécialisé dans la formation des professionnels d'ESSMS (foyers de vie, FAM, MAS, SAVS, SAMSAH).

Génère ${nb} questions QCM sur le thème : **${theme}**

Niveau de difficulté : ${niveau}
${source ? `Source de référence : ${source}` : 'Base-toi sur les RBPP HAS/ANESM en vigueur.'}

**Format obligatoire pour chaque question :**

Q[N]. [Intitulé de la question, formulé clairement]
A. [Proposition A]
B. [Proposition B]
C. [Proposition C]
D. [Proposition D]
Réponse : [Lettre de la bonne réponse]
Explication : [Explication courte (2-3 phrases) justifiant la bonne réponse et précisant les erreurs fréquentes]
Référence : [RBPP ou source citée si applicable]

**Consignes de conception :**
- Couverture équilibrée : répartis les questions sur tous les sous-thèmes du domaine
- Niveau ${niveau} : ${niveau === 'debutant' ? 'notions fondamentales, vocabulaire de base' : niveau === 'intermediaire' ? 'application pratique, cas concrets du quotidien professionnel' : 'expertise clinique, situations complexes, analyse critique'}
- Évite les propositions ambiguës ou trop proches
- Intègre des cas pratiques contextualisés (ex: "Un résident de FAM refuse de participer à...")
- Répartis les bonnes réponses (pas toujours A ou B)
- Chaque question doit apporter un enseignement, même en cas d'erreur

Commence directement avec Q1.`
        }
      }
    ]
  })
);

/**
 * Prompt : synthese_veille
 * Synthétise des sources de veille en un document structuré
 */
server.prompt(
  'synthese_veille',
  {
    sources: z.array(z.string()).min(1).describe('Liste des URLs ou textes sources à synthétiser'),
    domaine: z.enum(['has-rbpp', 'serafin-ph', 'tnmp', 'qvct', 'legislation', 'general']).default('general').describe('Domaine thématique de la veille'),
    format: z.enum(['court', 'complet']).default('complet').describe('Format de la synthèse')
  },
  ({ sources, domaine, format }) => ({
    messages: [
      {
        role: 'user',
        content: {
          type: 'text',
          text: `Tu es un chargé de veille documentaire spécialisé dans le secteur médico-social français, expert des publications HAS, CNSA, DGCS et ATIH.

Domaine de veille : ${domaine === 'has-rbpp' ? 'Recommandations de Bonnes Pratiques HAS/ANESM' : domaine === 'serafin-ph' ? 'Réforme SERAFIN-PH (financement ESSMS)' : domaine === 'tnmp' ? 'Thérapies Non Médicamenteuses (Snoezelen, PBS, NPI-ES)' : domaine === 'qvct' ? 'Qualité de Vie et Conditions de Travail' : domaine === 'legislation' ? 'Législation et droits des personnes accompagnées' : 'Médico-social général'}

Sources à analyser :
${sources.map((s, i) => `${i + 1}. ${s}`).join('\n')}

${format === 'court' ? `Produis une synthèse courte (1 page max) :
## En bref
[3-5 points clés en bullets]
## Ce qui change pour les ESSMS
[2-3 implications pratiques]
## Agenda
[Échéances à retenir]` : `Produis une synthèse complète structurée :

## 1. Tableau de bord
| Thème | Nouveauté | Impact | Urgence |
|-------|-----------|--------|---------|

## 2. Analyse par source
Pour chaque source : titre, date, résumé (5-7 lignes), points clés

## 3. Synthèse transversale
Tendances émergentes, cohérence avec les politiques nationales

## 4. Points de vigilance pour les directions
Tableau : ⚠️ Point | Détail pratique | Action recommandée

## 5. Agenda — Prochains rendez-vous
Dates d'échéance, consultations publiques, publications attendues

## 6. Pour aller plus loin
Ressources complémentaires, contacts institutionnels`}

Registre : professionnel médico-social, accessible aux cadres de direction et chefs de service.`
        }
      }
    ]
  })
);

/**
 * Prompt : bilan_semaine
 * Génère un bilan hebdomadaire des livrables produits
 */
server.prompt(
  'bilan_semaine',
  {},
  () => {
    // Scan dynamique des livrables de la semaine
    const today = new Date();
    const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);
    const weekAgoStr = weekAgo.toISOString().split('T')[0];

    const livrables = [];
    const dirs = [
      { path: path.join(PROJECT_ROOT, 'Livrables', 'Quiz'), type: 'Quiz' },
      { path: path.join(PROJECT_ROOT, 'Livrables', 'Infographies'), type: 'Infographie' },
      { path: path.join(PROJECT_ROOT, 'Livrables', 'Leçons'), type: 'Leçon' },
      { path: path.join(PROJECT_ROOT, 'Sources', 'Veille'), type: 'Veille' },
      { path: path.join(PROJECT_ROOT, 'Livrables', 'Documents'), type: 'Document' }
    ];

    for (const { path: dir, type } of dirs) {
      if (!fs.existsSync(dir)) continue;
      const files = fs.readdirSync(dir);
      for (const f of files) {
        const stats = fs.statSync(path.join(dir, f));
        const dateStr = stats.mtime.toISOString().split('T')[0];
        if (dateStr >= weekAgoStr) {
          livrables.push({ type, nom: f, date: dateStr, taille_ko: Math.round(stats.size / 1024) });
        }
      }
    }

    const livrablesText = livrables.length > 0
      ? livrables.map(l => `- [${l.type}] ${l.nom} (${l.date}, ${l.taille_ko} Ko)`).join('\n')
      : '(aucun livrable détecté cette semaine)';

    return {
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: `Tu es un assistant de synthèse pour le projet Claude_Travail, dédié à la formation professionnelle médico-sociale.

Génère le bilan hebdomadaire du projet pour la semaine du ${weekAgoStr} au ${today.toISOString().split('T')[0]}.

**Livrables produits cette semaine (détectés automatiquement) :**
${livrablesText}

Produis un bilan structuré :

## Bilan de la semaine — ${today.toISOString().split('T')[0]}

### Production de la semaine
Tableau récapitulatif : Type | Nombre | Détail

### Points forts
[Ce qui a bien fonctionné, contenus particulièrement utiles]

### Points d'amélioration
[Ce qui peut être optimisé la semaine prochaine]

### Agenda de la semaine prochaine
Rappel des jobs planifiés :
- Lundi 8h30 : Pipeline RBPP HAS
- Mercredi 8h03 : Veille SERAFIN-PH
- Vendredi 8h03 : Leçon NO-CODE + IA
- Vendredi 8h20 : Projet Web App
- Vendredi 8h35 : Projet Agents Claude
- Vendredi 8h50 : Projet MCP

### Progression des projets progressifs
- Web App Next.js : [NN]/10 sessions
- Agents Claude : [NN]/10 sessions
- Intégrations MCP : [NN]/10 sessions

Ton de la synthèse : factuel, orienté action, adapté à un usage interne de direction d'ESSMS.`
          }
        }
      ]
    };
  }
);

/**
 * Prompt : analyser_temoignage
 * Analyse un témoignage ou incident pour identifier des pistes d'amélioration
 */
server.prompt(
  'analyser_temoignage',
  {
    temoignage: z.string().min(20).describe('Texte du témoignage ou description de la situation'),
    type: z.enum(['incident', 'bientraitance', 'maltraitance', 'reclamation', 'evenement_indesirable']).describe('Type de situation'),
    etablissement: z.string().optional().describe('Type d\'établissement (FAM, MAS, SAVS, etc.)')
  },
  ({ temoignage, type, etablissement }) => ({
    messages: [
      {
        role: 'user',
        content: {
          type: 'text',
          text: `Tu es un expert en analyse des pratiques professionnelles dans le secteur médico-social, formé aux approches de bientraitance selon les RBPP HAS/ANESM.

${etablissement ? `Contexte : établissement de type ${etablissement}` : ''}

Type de situation : ${type === 'incident' ? 'Incident / événement indésirable' : type === 'bientraitance' ? 'Exemple de bientraitance' : type === 'maltraitance' ? 'Situation de maltraitance avérée ou suspectée' : type === 'reclamation' ? 'Réclamation d\'un résident ou de sa famille' : 'Événement indésirable grave (EIG)'}

Témoignage / situation à analyser :
---
${temoignage}
---

Produis une analyse structurée selon la méthode RBPP :

## 1. Identification de la situation
- Type : [classification précise]
- Gravité : [faible / modérée / grave / critique]
- Personnes impliquées : [catégories, sans données nominatives]

## 2. Analyse factuelle
Ce qui s'est passé (faits objectifs, chronologie si applicable)

## 3. Facteurs contributifs identifiés
Tableau : Facteur | Type (humain/organisationnel/environnemental) | Poids

## 4. Références RBPP applicables
Quelles recommandations HAS/ANESM sont pertinentes ici ?

## 5. Pistes d'amélioration
Actions correctives immédiates / Actions préventives à moyen terme / Axes de formation

## 6. Points de vigilance
Ce que cette situation révèle sur les pratiques collectives

## 7. Éléments à documenter
Ce qui doit figurer dans le registre FAVI / rapport d'incident / DUERP

Approche : bienveillante, non culpabilisante, orientée amélioration des pratiques.`
        }
      }
    ]
  })
);

/**
 * Prompt : rediger_fiche_rbpp
 * Rédige une fiche de synthèse pédagogique à partir d'une RBPP
 */
server.prompt(
  'rediger_fiche_rbpp',
  {
    titre_rbpp: z.string().describe('Titre de la RBPP à synthétiser'),
    url: z.string().url().optional().describe('URL de la RBPP (si disponible)'),
    public: z.enum(['professionnels', 'direction', 'residents', 'familles']).default('professionnels').describe('Public destinataire de la fiche')
  },
  ({ titre_rbpp, url, public: pub }) => ({
    messages: [
      {
        role: 'user',
        content: {
          type: 'text',
          text: `Tu es un formateur spécialisé en médico-social, expert en ingénierie pédagogique et en valorisation des recommandations HAS.

Rédige une fiche pédagogique synthétique sur la RBPP : **${titre_rbpp}**
${url ? `URL de référence : ${url}` : ''}

Public destinataire : ${pub === 'professionnels' ? 'Professionnels de terrain (AES, AS, IDE, éducateurs)' : pub === 'direction' ? 'Équipe de direction et cadres de service' : pub === 'residents' ? 'Personnes accompagnées (langage accessible, FALC si possible)' : 'Familles et proches aidants'}

**Structure de la fiche (format A4 recto-verso) :**

---
**FICHE RBPP — ${titre_rbpp.toUpperCase()}**
Date de publication HAS : [à compléter]
---

### En une phrase
[Résumé de la RBPP en 1 phrase, claire et mémorisable]

### Pourquoi cette recommandation ?
[Contexte, problématique identifiée, enjeux pour les personnes accompagnées]

### Les 5 points essentiels à retenir
1. [Point essentiel 1]
2. [Point essentiel 2]
3. [Point essentiel 3]
4. [Point essentiel 4]
5. [Point essentiel 5]

### Dans ma pratique quotidienne, cela signifie...
[3-5 exemples concrets, formulés à la 1ère personne professionnelle]

### Ce qui change par rapport aux anciennes pratiques
[Tableau : Avant | Maintenant]

### Pour aller plus loin
[Ressources, outils HAS associés, formations disponibles]

---
*Fiche produite dans le cadre de la démarche qualité — [Type d'établissement]*
---

Langue : français professionnel, accessible, sans jargon excessif.
${pub === 'residents' ? 'Attention : adapter le vocabulaire pour les personnes accompagnées (phrases courtes, mots simples, exemples du quotidien).' : ''}`
        }
      }
    ]
  })
);

/**
 * Prompt : evaluer_pratique
 * Évalue une pratique professionnelle au regard des RBPP
 */
server.prompt(
  'evaluer_pratique',
  {
    pratique: z.string().min(20).describe('Description de la pratique professionnelle à évaluer'),
    rbpp_reference: z.string().optional().describe('RBPP de référence spécifique à utiliser'),
    contexte: z.string().optional().describe('Contexte de l\'établissement ou de la situation')
  },
  ({ pratique, rbpp_reference, contexte }) => ({
    messages: [
      {
        role: 'user',
        content: {
          type: 'text',
          text: `Tu es un expert en évaluation des pratiques professionnelles (EPP) dans le secteur médico-social, formé aux méthodes d'évaluation HAS.

${contexte ? `Contexte : ${contexte}` : ''}
${rbpp_reference ? `RBPP de référence : ${rbpp_reference}` : 'Base-toi sur l\'ensemble des RBPP HAS/ANESM pertinentes.'}

Pratique professionnelle à évaluer :
---
${pratique}
---

Produis une évaluation structurée :

## 1. Conformité aux RBPP
Tableau :
| Critère RBPP | Niveau de conformité | Observations |
|---|---|---|
| [Critère 1] | ✅ Conforme / ⚠️ Partiel / ❌ Non conforme | [observation] |

## 2. Points forts de la pratique
[Ce qui est bien aligné avec les recommandations]

## 3. Axes d'amélioration prioritaires
[Par ordre de priorité, avec justification RBPP]

## 4. Recommandations opérationnelles
Actions concrètes, réalisables, avec responsable suggéré et délai

## 5. Score global de conformité
[Estimation en %, avec nuances qualitatives]

## 6. Formation recommandée
Besoins en formation identifiés pour améliorer cette pratique

Approche : constructive, basée sur les preuves, orientée amélioration continue.`
        }
      }
    ]
  })
);

// ─── Connexion via transport stdio ────────────────────────────────────────
const transport = new StdioServerTransport();
await server.connect(transport);
