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
│       └── imac/ · ai-act/ (actifs) · rgpd/ (archive, job supprimé le 25/07/2026)
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

## Quiz et infographies PowerPoint

Produits par le seul job `rbpp-pipeline`. Livrables → `livrables/quiz/` et `livrables/infographies/`.

> 📄 **Format, style, script type et les deux règles critiques (dimensions négatives, géométrie elliptique) sont dans `outils/templates/REGLES_PPTX.md`** — à lire avant toute génération PPTX. Ces deux règles viennent de bugs qui rendaient le fichier inouvrable par PowerPoint. Le prompt de `rbpp-pipeline` porte l'instruction explicite de lire ce fichier, puisqu'il n'est plus chargé à chaque session.

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

## Jobs planifiés

14 jobs hebdomadaires tournent en autonomie via **launchd** (app fermée) : agent launchd → `outils/scripts/run_job.sh <job_id>` → `claude -p` headless.

- **`jobs_config.json` est la source de vérité unique** des jobs (`id`, `cron`, `livrable`, `prompt`). `run_job.sh` en extrait le seul prompt du job : le fichier n'entre plus en contexte.
- **`run_job.sh` est la source de vérité des plafonds de coût** (bloc `case "$JOB_ID"`). Cumul actuel : **46 $/semaine** — une somme de plafonds, *pas* une dépense (voir `outils/scripts/JOBS.md`).
- **L'auto-push suit une liste blanche stricte** — `sources/veille/` + `livrables/{lecons,quiz,infographies,projets,controles,documents}`. **Jamais `git add -A`** : `contexte/`, `sources/rbpp`, `sources/tnmp`, `sources/qvct`, `en_cours/`, `ressources/`, `outils/` et `NotebookLM/` restent hors publication automatique.
- **`setup_launchd.sh` ne synchronise que les CRÉNEAUX, pas les prompts** (précisé le 11/09/2026) : le `.plist` ne porte que `run_job.sh` + l'`id` du job, et le prompt est relu dans `jobs_config.json` à chaque exécution. À relancer **seulement** après création, suppression, renommage d'un job ou changement de son `cron` — **pas** pour un durcissement de prompt : recharger tue le job en vol (le script refuse si l'un tourne, `--force` passe outre).
- Toute création, suppression ou recréation de job se répercute **ici et dans `jobs_config.json`** : les deux se relisent ensemble.
- **Les contrôles communs** (`outils/scripts/controle_attributions.py`, `controle_decompte.py`) sont appelés par les prompts, jamais copiés. **Toute retouche se rejoue avec `outils/scripts/non_regression.sh`** (90 s, diff des verdicts sur les 221 documents) avant d'être poussée — le hook `outils/scripts/hooks/pre-push` (`git config core.hooksPath outils/scripts/hooks`, une fois par clone) le lance et **refuse le push** si un verdict a changé ; les pushs des jobs ne le déclenchent pas.

> 📄 **Tout le reste — horaires des 14 créneaux, plafonds détaillés et leurs justifications, authentification headless, retry, veille macOS, garde-fous des cinq familles, et l'historique daté des incidents — est dans `outils/scripts/JOBS.md`.** Lis-le avant toute intervention sur la planification, les prompts de job ou les coûts.

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
