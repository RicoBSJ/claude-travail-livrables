# CLAUDE.md — Instructions permanentes pour Claude Code

## Contexte professionnel

Je travaille dans le secteur médico-social français, au sein d'établissements de type ESSMS
(foyer de vie, FAM, MAS, SAVS, SAMSAH). Mes productions servent à la formation professionnelle
des équipes et à la démarche qualité.

Les thématiques récurrentes incluent :
- RBPP HAS/ANESM : bientraitance, autodétermination, habitat, troubles du comportement
- Thérapies non médicamenteuses (TNmP) : Snoezelen, PBS, NPI-ES, CMAI
- Droits des personnes accompagnées (TDI/TSA et autres vulnérabilités)
- Qualité de vie au travail (QVT) et prévention de la maltraitance

---

## Structure du projet

```
Claude_Travail/
├── CLAUDE.md               ← ce fichier
├── jobs_config.json        ← configuration des jobs planifiés (CronCreate)
├── Sources/
│   ├── RBPP/               ← PDFs HAS/ANESM bruts (sous-dossier par RBPP)
│   ├── TNmP/               ← fichiers Excel TNmP
│   ├── QVCT/               ← documents QVCT
│   └── Veille/             ← toutes les veilles produites (SERAFIN, RBPP, HAS, NO-CODE+IA)
├── Templates/
│   ├── quiz_style.js       ← template quiz PowerPoint (multi-palette RBPP/CNT/TNmP)
│   ├── infographie_style.js← template infographies (format pétale et cartes)
│   └── word_style.js       ← template documents Word
├── En_cours/               ← scripts temporaires + node_modules (à nettoyer après chaque tâche)
├── Livrables/
│   ├── Quiz/               ← convention : quiz_[type]_[slug]_YYYY-MM-DD.pptx
│   ├── Infographies/       ← convention : infographie_[type]_[slug]_YYYY-MM-DD.pptx
│   ├── Leçons/             ← leçons Word hebdomadaires (NO-CODE+IA)
│   └── Documents/          ← documents Word divers
├── NotebookLM/             ← notebooks thématiques (RBPP, HAS, SERAFIN-PH, Formation, CPOM)
│   ├── README.md           ← architecture, workflow, limites NotebookLM
│   ├── RBPP/               ← Sources_PDF/ + Prompts/notebook_guide_RBPP.md
│   ├── Evaluation_HAS/     ← Sources_PDF/ + Prompts/notebook_guide_Evaluation_HAS.md
│   ├── SERAFIN-PH/         ← Sources_PDF/ + Prompts/notebook_guide_SERAFIN-PH.md
│   ├── Formation_Equipe/   ← Sources_PDF/ + Prompts/notebook_guide_Formation_Equipe.md
│   └── CPOM/               ← Sources_PDF/ + Prompts/notebook_guide_CPOM.md
├── Prompts/                ← prompts réutilisables (Claude.ai, Claude Code, NotebookLM)
│   └── workflow_5etapes_claudeai.md
├── Ressources/             ← documentation de référence externe (MCP, outils, guides)
└── Prompt/
    ├── session_YYYY-MM-DD_prompts.txt  ← logs de sessions actives
    └── Archives/           ← anciens prompts .rtf
```

### Conventions de nommage des livrables

| Type | Format | Exemple |
|------|--------|---------|
| Veille | `YYYY-MM-DD_veille_[sujet].docx` | `2026-04-06_veille_SERAFIN-PH.docx` |
| Quiz | `quiz_[type]_[slug]_YYYY-MM-DD.pptx` | `quiz_rbpp_projet-personnalise_2026-04-06.pptx` |
| Infographie | `infographie_[type]_[slug]_YYYY-MM-DD.pptx` | `infographie_rbpp_tsa-enfant-adolescent_2026-02-12.pptx` |
| Leçon NO-CODE+IA | `YYYY-MM-DD_lecon-nocode-ia_NN_[slug].docx` | `2026-04-10_lecon-nocode-ia_01_ia-agentique-production.docx` |

---

## Stack technique

- **Runtime** : Node.js
- **Librairie PPTX** : pptxgenjs
- **Librairie Word** : docx (npm)
- **Librairie PDF** : pdf-parse (lecture), pdfkit (création)
- **Langue des scripts** : JavaScript (Node.js)
- Toujours vérifier si `node_modules` existe avant d'installer des dépendances
- Toujours utiliser `npm install` dans `En_cours/` pour les scripts temporaires

---

## Règles générales

- Lire le fichier source en entier avant de commencer à générer quoi que ce soit.
- Utiliser les templates existants dans `Templates/` si disponibles.
- Sauvegarder les livrables finaux dans le bon sous-dossier de `Livrables/`.
- Utiliser `En_cours/` pour les scripts et fichiers intermédiaires.
- Nettoyer `En_cours/` après chaque tâche terminée.
- Pour toute action irréversible (suppression, écrasement), demander confirmation d'abord.
- Afficher un plan structuré avant de générer un fichier long (>20 slides ou >10 pages).

---

## Quiz PowerPoint

- ~100 questions QCM par quiz
- Alternance stricte : slide question / slide réponse
- Slide question : question + 4 propositions (A, B, C, D)
- Slide réponse : bonne réponse mise en évidence + explication courte
- Style : fond bleu marine `#1B3A6B`, texte blanc, police Calibri
- Couverture équilibrée de l'ensemble du document source
- Niveau adapté aux professionnels du médico-social
- Livrable → `Livrables/Quiz/`

### Script type (pptxgenjs)
```javascript
const pptx = require("pptxgenjs");
const fs = require("fs");

// Charger les questions depuis un JSON généré au préalable
const questions = JSON.parse(fs.readFileSync("questions.json", "utf8"));

let pres = new pptx.default();
pres.layout = "LAYOUT_WIDE"; // 16:9

questions.forEach((q, i) => {
  // Slide question
  let slideQ = pres.addSlide();
  slideQ.background = { color: "1B3A6B" };
  slideQ.addText(`Q${i + 1}. ${q.question}`, {
    x: 0.5, y: 0.5, w: "90%", fontSize: 24, color: "FFFFFF", bold: true
  });
  q.options.forEach((opt, j) => {
    slideQ.addText(`${["A", "B", "C", "D"][j]}. ${opt}`, {
      x: 0.5, y: 2 + j * 0.8, w: "90%", fontSize: 18, color: "FFFFFF"
    });
  });

  // Slide réponse
  let slideR = pres.addSlide();
  slideR.background = { color: "1B3A6B" };
  slideR.addText(`✅ Réponse : ${q.answer}`, {
    x: 0.5, y: 0.5, w: "90%", fontSize: 24, color: "00FF99", bold: true
  });
  slideR.addText(q.explanation, {
    x: 0.5, y: 2, w: "90%", fontSize: 18, color: "FFFFFF"
  });
});

pres.writeFile({ fileName: "Livrables/Quiz/quiz_output.pptx" });
console.log("✅ Quiz généré avec succès.");
```

---

## Infographies PowerPoint (format pétale)

- Fleur avec 6 à 8 pétales selon le nombre de thèmes
- Disposition radiale, centrée, pétales symétriques
- Fond blanc, couleurs distinctes par pétale (palette harmonieuse)
- Police Calibri, format 16:9
- Titre au centre de la fleur
- Livrable → `Livrables/Infographies/`

### ⚠️ Règle critique 1 — Lignes de connexion radiales (dimensions positives)

PowerPoint refuse d'ouvrir un PPTX si une forme a une dimension négative (`cx="-..."`).
Lors du dessin de lignes du centre vers des pétales positionnés à gauche ou au-dessus,
`w = x2 - x1` ou `h = y2 - y1` peut devenir négatif.

**Toujours utiliser ce helper** :
```javascript
function addLine(slide, x1, y1, x2, y2, color, width = 2) {
  const x = Math.min(x1, x2);
  const y = Math.min(y1, y2);
  const w = Math.max(Math.abs(x2 - x1), 0.01);
  const h = Math.max(Math.abs(y2 - y1), 0.01);
  slide.addShape("line", {
    x, y, w, h,
    line: { color, width },
    flipH: x2 < x1,
    flipV: y2 < y1
  });
}
```

### ⚠️ Règle critique 2 — Géométrie elliptique (éviter les chevauchements)

Slide LAYOUT_WIDE = 13.33 × 7.5". Plus large que haut → disposition CIRCULAIRE génère du
chevauchement avec titre/footer. Utiliser une ELLIPSE (Rx > Ry).

**Paramètres validés** pour 6 à 8 pétales :
```javascript
const CX = 6.665, CY = 4.10;       // centre légèrement décalé
const Rx = 3.40, Ry = 2.00;        // ellipse : Rx > Ry
const R_CENTER = 1.05;              // cercle central
const PETALE_W = 2.40, PETALE_H = 1.30;  // pétales compacts

// Zones occupées :
// Titre principal     : y ∈ [0.20, 0.75]  (fontSize 28)
// Sous-titre          : y ∈ [0.78, 1.10]  (fontSize 16)
// Zone pétales/centre : y ∈ [1.20, 7.00]
// Pied de page        : y ∈ [7.15, 7.40]  (fontSize 10)
```

**Vérification post-génération** :
```bash
unzip -p [fichier].pptx ppt/slides/slide1.xml | grep -c '<a:ext cx="-'
# doit retourner 0
```

---

## Documents Word

- Style professionnel, structuré avec titres et sous-titres
- Français, registre professionnel médico-social
- Livrable → `Livrables/Documents/` (documents divers) ou `Livrables/Leçons/` (leçons hebdomadaires)

---

## Veille HAS/ANESM

- Source : https://www.has-sante.fr
- Résumé d'une page max : titre, date, public cible, points clés
- Nom du fichier : `YYYY-MM-DD_veille_HAS.md`
- Livrable → `Sources/Veille/`

## Veille NO-CODE + IA (hebdomadaire, vendredi 8h03)

- Sources : the-decoder.com, huggingface.co/blog/feed.xml, simonwillison.net, openai.com/blog/rss.xml, make.com/en/blog, blog.n8n.io, zapier.com/blog, webflow.com/blog
- Format : leçon active (20% théorie / 80% pratique) avec hyperliens cliquables
- Nom du fichier : `YYYY-MM-DD_lecon-nocode-ia_NN_[slug].docx`
- Livrable → `Livrables/Leçons/`
- Note : openai.com/news retourne 403 → utiliser openai.com/blog/rss.xml
- Note : huggingface.co/blog retourne 500 (rendu JS) → utiliser huggingface.co/blog/feed.xml

---

## Jobs planifiés — Double mécanisme (session + système macOS)

Tous les jobs récurrents sont définis dans **`jobs_config.json`** (source de vérité unique : `id`, `cron`, `prompt`…). Deux moyens de les exécuter automatiquement :

### A. Planificateur de session (CronCreate) — Claude Code ouvert
- Skill **`/restaurer-jobs`** : recrée tous les crons de la session depuis `jobs_config.json`.
- Limites : crons liés à la session (disparaissent à la fermeture), auto-expiration à 7 jours, ne se déclenchent que si l'app est **ouverte et idle**.
- Usage : `/restaurer-jobs` au démarrage de session.

### B. Planificateur système (launchd) — **app fermée, autonomie réelle** ✅
- 8 agents `~/Library/LaunchAgents/com.claudetravail.<job_id>.plist` exécutent les jobs **même Claude Code fermé**.
- Chaîne : agent launchd → `scripts/run_job.sh <job_id>` → `claude -p` headless (lit `jobs_config.json`, exécute le job).
- Modèle forcé : **sonnet** · plafond **2 $/exécution** (modifiable dans `run_job.sh`).
- launchd **rattrape** une tâche manquée au réveil du Mac (mieux que crontab). Mac éteint = tâche sautée.
- ✅ **Tous les jobs sont 100% headless** : aucune dépendance Chrome MCP. Les sources dynamiques/bloquées (ATIH, listing HAS) sont récupérées via **WebSearch + WebFetch** ; toute source inaccessible est marquée ⛔ et le job continue.

**Scripts (`scripts/`) :**
| Script | Rôle |
|--------|------|
| `run_job.sh <job_id>` | Exécute un job en headless (logs → `scripts/logs/`) |
| `setup_launchd.sh` | Génère + charge les 8 agents (idempotent ; relancer après modif d'horaire) |
| `teardown_launchd.sh` | Décharge + supprime tous les agents |

**Commandes utiles :**
```bash
launchctl list | grep claudetravail        # voir les agents actifs
bash scripts/setup_launchd.sh              # (ré)installer / mettre à jour
bash scripts/run_job.sh ai-act-veille      # test manuel d'un job
bash scripts/teardown_launchd.sh           # tout désactiver
```

**Horaires (= champ `cron`) :** ai-act-veille (quotidien 7h03) · rgpd-veille (quotidien 7h33) · rbpp-pipeline (lun 8h30) · dzogchen-lecon (mar 8h03) · serafin-ph-veille (mer 8h03) · enneagramme-lecon (mer 9h03) · stoicisme-lecon (jeu 8h03) · nocode-ia-veille (ven 8h03).

**Veilles quotidiennes (sous-dossiers dédiés dans `Sources/Veille/`) :** `AI-Act/` et `RGPD/` — 1 CR Word/jour, déduplication sur la date du jour, règle anti-redondance (CR allégé 🟢 si aucune nouveauté < 24h).

> Règle : après tout ajout/modif de job dans `jobs_config.json`, relancer `bash scripts/setup_launchd.sh` pour synchroniser launchd. Les logs `scripts/logs/` et `node_modules` sont gitignorés.

---

## NotebookLM

5 notebooks thématiques, chacun avec un Notebook Guide dédié à coller dans l'interface.

| Notebook | Usage principal |
|---|---|
| **RBPP** | Interrogation recommandations · Auto-diagnostic écart · Livrables formation |
| **Evaluation_HAS** | Préparation évaluation externe · Grilles · Argumentaires preuves |
| **SERAFIN-PH** | Anticipation bascule 2027 · Veille réglementaire CNSA |
| **Formation_Equipe** | Formation AES/ME/ES · Onboarding · Cas pratiques |
| **CPOM** | Préparation contractuelle · Suivi indicateurs · Bilans ARS |

- Sources acceptées : **PDF uniquement** (convertir DOCX/PPTX via Office 365 → Exporter → PDF)
- Guides : `NotebookLM/[nom]/Prompts/notebook_guide_[nom].md`
- Dépôt des PDFs : `NotebookLM/[nom]/Sources_PDF/`
- Workflow complet : voir `NotebookLM/README.md`

---

## Workflow 5 étapes — Analyse experte médico-social

Quand une demande d'analyse, de production ou de recherche est formulée, appliquer ce workflow dans l'ordre. Annoncer chaque étape avec son numéro et son intitulé.

**ÉTAPE 1 — CLARIFICATION**
Poser 3 à 5 questions ciblées AVANT toute production. Ne pas produire sans avoir clarifié : destinataire, livrable attendu, RBPP concernée, contexte, contraintes.

**ÉTAPE 2 — PRODUCTION**
Produire le livrable demandé parmi :
- `CHECK` → fiche check-list opérationnelle terrain
- `SYNTHESE` → note de cadrage structurée (direction, ARS)
- `FORMATION` → contenu pédagogique (plan, quiz, fiche)
- `ANALYSE` → analyse critique d'un document existant

Format adapté au destinataire déclaré. Titres, listes, tableaux — pas de prose continue.

**ÉTAPE 3 — SOURCES**
Lister toutes les sources mobilisées :
- Référence exacte (nom RBPP, article de loi, publication HAS, date)
- Niveau : haute (source officielle vérifiable) / moyenne (usage courant) / incertaine (à vérifier)
- Signaler chaque affirmation sans source identifiable

**ÉTAPE 4 — CRITIQUE ET AMÉLIORATION**
Identifier 3 à 5 faiblesses (angles morts, limites d'applicabilité, risques terrain, biais).
Produire une version améliorée en indiquant explicitement ce qui a changé.

**ÉTAPE 5 — REVERSE ENGINEERING**
Générer le prompt parfait autonome qui aurait produit ce résultat final dès le départ.
Critères : autonome · réutilisable · complet (rôle + contexte + contraintes + format) · compact.
Le présenter dans un bloc de code prêt à copier-coller.

Prompt de référence complet → `Prompts/workflow_5etapes_claudeai.md`

---

## Ce que je n'aime pas

- Slides surchargées en texte
- Formulations trop académiques ou trop familières
- Fichiers intermédiaires oubliés dans `En_cours/`
- Actions irréversibles sans confirmation préalable
- Scripts qui écrasent un livrable existant sans prévenir
