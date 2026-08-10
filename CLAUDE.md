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
├── CLAUDE.md               ← ce fichier (instructions projet, auto-chargé)
├── jobs_config.json        ← configuration des jobs planifiés (source de vérité)
├── .gitignore
│
├── sources/                ← ENTRÉES
│   ├── rbpp/               ← PDFs HAS/ANESM bruts (un sous-dossier par RBPP)
│   ├── tnmp/               ← fichiers Excel TNmP
│   ├── qvct/               ← documents QVCT
│   └── veille/             ← veilles produites (SERAFIN, RBPP, HAS, ESSMS…)
│       └── imac/ (actif) · ai-act/ · rgpd/ (archives, jobs supprimés le 20/07/2026)
│
├── livrables/              ← SORTIES
│   ├── lecons/             ← leçons Word hebdomadaires (parcours d'apprentissage)
│   ├── quiz/               ← quiz_[type]_[slug]_YYYY-MM-DD.pptx
│   ├── infographies/       ← infographie_[type]_[slug]_YYYY-MM-DD.pptx
│   ├── documents/          ← documents Word divers, fiches synthèse
│   ├── controles/          ← notes de contrôle qualité hebdomadaires (job controle-livrables)
│   └── projets/appli-ia/   ← projet fil rouge du parcours appli-ia (code + PROJET.md)
│
├── outils/                 ← OUTILLAGE
│   ├── scripts/            ← run_job.sh, setup/teardown_launchd.sh, logs/ (gitignorés)
│   ├── templates/          ← quiz_style.js, infographie_style.js, word_style.js
│   └── prompts/            ← prompts réutilisables + archives/
│
├── ressources/             ← docs de référence (MCP, CLI, vim, bonnes pratiques…)
│
├── contexte/               ← instructions thématiques (chaque sous-dossier garde son CLAUDE.md auto-chargé)
│   ├── cpom/ · serafin-ph/ · formations-rbpp/ · archives/
│   └── emails/             ← CLAUDE.md + outil-anonymisation.html
│
└── en_cours/               ← temporaire (scripts jetables + node_modules ; nettoyer après chaque tâche)
```

### Conventions de nommage des livrables

| Type | Format | Exemple |
|------|--------|---------|
| Veille | `YYYY-MM-DD_veille_[sujet].docx` | `2026-04-06_veille_SERAFIN-PH.docx` |
| Quiz | `quiz_[type]_[slug]_YYYY-MM-DD.pptx` | `quiz_rbpp_projet-personnalise_2026-04-06.pptx` |
| Infographie | `infographie_[type]_[slug]_YYYY-MM-DD.pptx` | `infographie_rbpp_tsa-enfant-adolescent_2026-02-12.pptx` |
| Leçon (parcours) | `YYYY-MM-DD_lecon-[parcours]_NN_[slug].docx` | `2026-08-07_lecon-appli-ia_01_cadrage-specification.docx` |

---

## Stack technique

- **Runtime** : Node.js
- **Librairie PPTX** : pptxgenjs
- **Librairie Word** : docx (npm)
- **Librairie PDF** : pdf-parse (lecture), pdfkit (création)
- **Langue des scripts** : JavaScript (Node.js)
- Toujours vérifier si `node_modules` existe avant d'installer des dépendances
- Toujours utiliser `npm install` dans `en_cours/` pour les scripts temporaires

---

## Règles générales

- Lire le fichier source en entier avant de commencer à générer quoi que ce soit.
- Utiliser les templates existants dans `outils/templates/` si disponibles.
- Sauvegarder les livrables finaux dans le bon sous-dossier de `livrables/`.
- Utiliser `en_cours/` pour les scripts et fichiers intermédiaires.
- Nettoyer `en_cours/` après chaque tâche terminée.
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
- Livrable → `livrables/quiz/`

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

pres.writeFile({ fileName: "livrables/quiz/quiz_output.pptx" });
console.log("✅ Quiz généré avec succès.");
```

---

## Infographies PowerPoint (format pétale)

- Fleur avec 6 à 8 pétales selon le nombre de thèmes
- Disposition radiale, centrée, pétales symétriques
- Fond blanc, couleurs distinctes par pétale (palette harmonieuse)
- Police Calibri, format 16:9
- Titre au centre de la fleur
- Livrable → `livrables/infographies/`

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
- Livrable → `livrables/documents/` (documents divers) ou `livrables/lecons/` (leçons hebdomadaires)

---

## Veille HAS/ANESM

- Source : https://www.has-sante.fr
- Résumé d'une page max : titre, date, public cible, points clés
- Nom du fichier : `YYYY-MM-DD_veille_HAS.md`
- Livrable → `sources/veille/`

## Leçon Développement d'applications avec l'IA (hebdomadaire, vendredi 8h03)

- Parcours **fermé de 12 leçons**, JavaScript/TypeScript, avec **projet fil rouge** : « Portail Livrables » (application web locale qui liste, recherche et filtre les livrables produits par les jobs).
- Sources : documentation officielle en priorité (developer.mozilla.org, nodejs.org, typescriptlang.org, react.dev, nextjs.org, docs.claude.com, cnil.fr).
- Format : leçon active (20% théorie / 80% pratique), **code complet et exécutable** à chaque incrément.
- Nom du fichier : `YYYY-MM-DD_lecon-appli-ia_NN_[slug].docx`
- Livrables → `livrables/lecons/` (la leçon) **et** `livrables/projets/appli-ia/` (le code + `PROJET.md`).
- **`PROJET.md` est la mémoire du parcours** : le job le lit au début de chaque leçon et le met à jour à la fin. Sans lui, pas de continuité du fil rouge.
- Garde-fou spécifique : ne jamais écrire de version de bibliothèque ni de signature d'API de mémoire (écosystème très mouvant) → vérifier à la doc officielle.

> Historique : ce job remplace `nocode-ia-veille` (supprimé le 02/08/2026). Les **16 leçons NO-CODE + IA** déjà produites (`lecon-nocode-ia_01` à `_16`) sont conservées dans `livrables/lecons/`.

---

## Jobs planifiés — Double mécanisme (session + système macOS)

Tous les jobs récurrents sont définis dans **`jobs_config.json`** (source de vérité unique : `id`, `cron`, `prompt`…). Deux moyens de les exécuter automatiquement :

### A. Planificateur de session (CronCreate) — Claude Code ouvert
- Skill **`/restaurer-jobs`** : recrée tous les crons de la session depuis `jobs_config.json`.
- Limites : crons liés à la session (disparaissent à la fermeture), auto-expiration à 7 jours, ne se déclenchent que si l'app est **ouverte et idle**.
- Usage : `/restaurer-jobs` au démarrage de session.

### B. Planificateur système (launchd) — **app fermée, autonomie réelle** ✅
- Un agent launchd par job (`~/Library/LaunchAgents/com.claudetravail.<job_id>.plist`) exécute les jobs **même Claude Code fermé**.
- Chaîne : agent launchd → `outils/scripts/run_job.sh <job_id>` → `claude -p` headless (lit `jobs_config.json`, exécute le job).
- Modèle forcé : **sonnet** · **plafond de coût par-job** (défini dans `run_job.sh`, modifiable) : `rbpp-pipeline` **4 $**, `imac-veille` **3,50 $**, tous les autres jobs **2 $** (défaut). Les jobs multi-sources dépassaient le plafond fixe de 2 $ → `claude -p` sortait en erreur, les 3 tentatives échouaient et le créneau hebdo était perdu (ex. RGPD du 05/07/2026, iMac du 19/07/2026).
- **Retry intégré** : jusqu'à **3 tentatives** (backoff 90s → 180s) en cas d'échec transitoire (timeout réseau/API au réveil du Mac). Un skip pour doublon (exit 0) n'est jamais retenté. Sans ce garde-fou, un job hebdo qui rate son unique créneau perdait 7 jours.
- ⚙️ **Authentification headless (jeton longue durée)** : le jeton OAuth du **Keychain** (login de l'app) expire ~chaque semaine et **ne se rafraîchit pas** en contexte launchd → **401 sur tous les jobs** (panne réelle du 09→15/07/2026). Solution : générer un jeton longue durée via `claude setup-token` (adossé à l'abonnement Pro, sans facturation API) et le placer dans **`outils/scripts/claude_auth.env`** (gitignoré, `chmod 600`, modèle : `claude_auth.env.example`). `run_job.sh` le source automatiquement (`CLAUDE_CODE_OAUTH_TOKEN`, ou à défaut `ANTHROPIC_API_KEY`). **Fail-fast** : sur une erreur d'auth (401), le runner arrête immédiatement les tentatives (inutile de réessayer un échec non transitoire) et logue la marche à suivre.
- launchd **rattrape** une tâche manquée au réveil du Mac (mieux que crontab). Mac éteint = tâche sautée.
- ⚙️ **Prérequis d'exécution à l'heure (veille macOS)** : un job **ne s'exécute PAS pendant la veille** — il n'est rattrapé qu'au réveil, et le Mac peut se rendormir avant un job de milieu de matinée (les créneaux s'étalent de dim 7h03 à jeu 9h33). Sur un iMac de bureau toujours branché, désactiver la veille système sur secteur pour que tous les jobs tournent à l'heure : `sudo pmset -c sleep 0 displaysleep 20` (l'écran s'éteint quand même ; vérifier avec `pmset -g custom` ; revenir en arrière avec `sudo pmset -c sleep 30`). Ce sont des **LaunchAgents** → **la session utilisateur doit rester ouverte** (ils ne tournent pas sur l'écran de connexion). Mac totalement éteint = jobs sautés (`poweron` non garanti sur tous les modèles).
- ✅ **Tous les jobs sont 100% headless** : aucune dépendance Chrome MCP. Les sources dynamiques/bloquées (ATIH, listing HAS) sont récupérées via **WebSearch + WebFetch** ; toute source inaccessible est marquée ⛔ et le job continue.

**Scripts (`outils/scripts/`) :**
| Script | Rôle |
|--------|------|
| `run_job.sh <job_id>` | Exécute un job en headless (logs → `outils/scripts/logs/`), puis **auto-commit + push** des livrables si succès (portée stricte, liste blanche explicite : `sources/veille/` (récursif) + `livrables/{lecons,quiz,infographies,projets,controles,documents}` ; jamais `git add -A` ; SSH non-interactif via `GIT_SSH_COMMAND`). **Push durci** : `git rebase --abort` propre si le `pull --rebase` échoue (évite de bloquer les jobs suivants), **3 tentatives de push** avec backoff réseau, et log du nombre de commits en avance sur `origin/main` en cas d'échec |
| `rattrapage_jobs.sh [job_id…]` | Rejoue une liste de jobs manqués via `run_job.sh` (anti-doublon de chaque job actif → aucun doublon). Sans argument : liste par défaut (`revenus-passifs-lecon` + `stoicisme-lecon`, `appli-ia-lecon`, `placement-financier-lecon`, `astrologie-karmique-lecon`) |
| `setup_launchd.sh` | Génère + charge tous les agents depuis la liste `JOBS` (idempotent ; relancer après modif d'horaire) |
| `teardown_launchd.sh` | Décharge + supprime tous les agents |

**Commandes utiles :**
```bash
launchctl list | grep claudetravail        # voir les agents actifs
bash outils/scripts/setup_launchd.sh              # (ré)installer / mettre à jour
bash outils/scripts/run_job.sh revenus-passifs-lecon   # test manuel d'un job
bash outils/scripts/teardown_launchd.sh           # tout désactiver
```

**Horaires (= champ `cron`) :** revenus-passifs-lecon (dim. 7h03) · imac-veille (dim. 8h03) · hypnose-lecon (mar 9h03) · psychopathologie-lecon (lun 8h03) · rbpp-pipeline (lun 8h30) · dzogchen-lecon (mar 8h03) · serafin-ph-veille (mer 8h03) · enneagramme-lecon (mer 9h03) · stoicisme-lecon (jeu 8h03) · appli-ia-lecon (ven 8h03) · placement-financier-lecon (sam 8h03) · astrologie-karmique-lecon (jeu 9h33) · controle-livrables (dim. 11h03).

> Historique : `astrologie-karmique-lecon` (créé le 10/08/2026) reprend le créneau de `entretien-motivationnel-lecon`, supprimé le même jour. Les **11 leçons d'entretien motivationnel** déjà produites (`lecon-entretien-motivationnel_01` à `_11`) sont conservées dans `livrables/lecons/`.
>
> Garde-fous spécifiques à ce parcours : les données astronomiques se vérifient **exclusivement** auprès de sources d'astronomie (IMCCE, Observatoire de Paris, NASA), jamais d'un site d'astrologie ; toute affirmation d'interprétation est **attribuée à son auteur** (Schulman, Spiller, Greene) ; chaque leçon comporte un encadré distinguant fait observable, convention du corpus et état de la recherche ; **aucun usage professionnel** n'est suggéré — le parcours est un intérêt personnel et ne touche jamais à l'accompagnement des personnes.

**Veille hebdomadaire à sous-dossier dédié dans `sources/veille/` :** `iMac/` (veille marché comparative tout-en-un : iMac M4/M5 + PC Windows équivalents) — 1 CR Word/semaine, déduplication sur la date du jour, règle anti-redondance (CR allégé 🟢 si aucune nouveauté depuis le CR précédent). L'auto-push couvre tout `sources/veille/` (récursif).

> Règle : après tout ajout/modif de job dans `jobs_config.json`, relancer `bash outils/scripts/setup_launchd.sh` pour synchroniser launchd. Les logs `outils/scripts/logs/` et `node_modules` sont gitignorés.

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
- Guides : `NotebookLM/[nom]/outils/prompts/notebook_guide_[nom].md`
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

Prompt de référence complet → `outils/prompts/workflow_5etapes_claudeai.md`

---

## Ce que je n'aime pas

- Slides surchargées en texte
- Formulations trop académiques ou trop familières
- Fichiers intermédiaires oubliés dans `en_cours/`
- Actions irréversibles sans confirmation préalable
- Scripts qui écrasent un livrable existant sans prévenir
