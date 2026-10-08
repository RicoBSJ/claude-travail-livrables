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
│   └── veille/             ← veilles produites — UN SOUS-DOSSIER PAR SÉRIE, racine vide
│       ├── serafin-ph/ · has-actualite/ · rbpp/ · imac/ · ai-act/   ← séries actives
│       └── rgpd/ (archive, job supprimé le 25/07/2026) · archives/ (séries sans job : nocode-ia, essms)
│
├── livrables/              ← SORTIES
│   ├── lecons/             ← leçons Word — UN SOUS-DOSSIER PAR PARCOURS, racine vide
│   │   ├── psychopathologie/ · enneagramme/ · dzogchen/ · stoicisme/ · hypnose/   ← parcours actifs
│   │   ├── placement-financier/ · astrologie-karmique/   ← parcours actifs
│   │   ├── appli-ia/   ← parcours TERMINÉ 12/12 (job supprimé le 04/10/2026)
│   │   ├── revenus-passifs/   ← parcours CLOS (job supprimé le 04/10/2026, 11 leçons conservées)
│   │   └── nocode-ia/ · entretien-motivationnel/ (parcours clos) · archives/ (leçons Claude Code d'avril)
│   ├── quiz/               ← quiz_[type]_[slug]_YYYY-MM-DD.pptx
│   ├── infographies/       ← infographie_[type]_[slug]_YYYY-MM-DD.pptx
│   ├── documents/          ← documents Word divers, fiches synthèse
│   ├── controles/          ← notes de contrôle qualité hebdomadaires (job controle-livrables)
│   └── projets/appli-ia/   ← projet fil rouge du parcours appli-ia, CONSERVÉ (code + PROJET.md)
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
| Leçon (parcours) | `[parcours]/YYYY-MM-DD_lecon-[parcours]_NN_[slug].docx` | `appli-ia/2026-08-07_lecon-appli-ia_01_cadrage-specification.docx` |

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
- Livrable → `livrables/documents/` (documents divers) ou `livrables/lecons/[parcours]/` (leçons hebdomadaires)

---

## Veille HAS/ANESM

- Source : https://www.has-sante.fr
- Résumé d'une page max : titre, date, public cible, points clés
- Nom du fichier : `YYYY-MM-DD_veille_HAS.md`
- Livrable → `sources/veille/has-actualite/`

## Leçon Développement d'applications avec l'IA — PARCOURS TERMINÉ, job supprimé le 04/10/2026

> ⛔ **Le job `appli-ia-lecon` a été supprimé le 04/10/2026** : les **12 leçons** du parcours fermé ont toutes été livrées, bilan compris (leçon 12, « maintenance-evolution-bilan », 02/10/2026). **Le créneau du vendredi 8h03 est libre.** Les leçons et le projet fil rouge sont conservés ; son prompt de **121 604 octets — le plus gros du dépôt** — reste lisible par `git show 14541bb:jobs_config.json`. Ce qui suit décrit le parcours tel qu'il a été produit.

- Parcours **fermé de 12 leçons**, JavaScript/TypeScript, avec **projet fil rouge** : « Portail Livrables » (application web locale qui liste, recherche et filtre les livrables produits par les jobs).
- Sources : documentation officielle en priorité (developer.mozilla.org, nodejs.org, typescriptlang.org, react.dev, nextjs.org, docs.claude.com, cnil.fr).
- Format : leçon active (20% théorie / 80% pratique), **code complet et exécutable** à chaque incrément.
- Nom du fichier : `YYYY-MM-DD_lecon-appli-ia_NN_[slug].docx`
- Livrables → `livrables/lecons/appli-ia/` (la leçon) **et** `livrables/projets/appli-ia/` (le code + `PROJET.md`).
- **`PROJET.md` est la mémoire du parcours** : le job le lit au début de chaque leçon et le met à jour à la fin. Sans lui, pas de continuité du fil rouge.
- Garde-fou spécifique : ne jamais écrire de version de bibliothèque ni de signature d'API de mémoire (écosystème très mouvant) → vérifier à la doc officielle.

> Historique : ce job remplace `nocode-ia-veille` (supprimé le 02/08/2026). Les **16 leçons NO-CODE + IA** déjà produites (`lecon-nocode-ia_01` à `_16`) sont conservées dans `livrables/lecons/nocode-ia/`.

---

## Jobs planifiés

**12 jobs** hebdomadaires tournent en autonomie via **launchd** (app fermée) : agent launchd → `outils/scripts/run_job.sh <job_id>` → `claude -p` headless.

- **`jobs_config.json` est la source de vérité unique** des jobs (`id`, `cron`, `livrable`, `prompt`). `run_job.sh` en extrait le seul prompt du job : le fichier n'entre plus en contexte.
- **`run_job.sh` est la source de vérité des plafonds de coût** (bloc `case "$JOB_ID"`). Cumul actuel : **42 $/semaine** sur 12 jobs — recompté le 08/10/2026 (12 `case`, 12 plafonds, aucun job au défaut). Deux suppressions le 04/10/2026 avaient fait passer le cumul de 45 à 40 $ (`revenus-passifs` à 3 $ et `appli-ia` à 5 $, leurs `case` retirés avec eux — le plafond d'appli-ia venait d'être relevé de 3 à 5 $ le 27/09/2026, huit jours avant la fin du parcours) ; le **08/10/2026, `astrologie-karmique-lecon` passe de 3 à 5 $** après le dépassement de son créneau (3,0218 $ pour 3,00 $, exit 1 en pleine vérification, livrable complet laissé sur le disque sans contrôle ni commit). Son prompt pesait 61 543 octets et son étape 5 bis réouvre chacune des pages listées — dix sur la leçon 10, dont quatre fiches du Minor Planet Center de 600 000 à 900 000 caractères. Il reste deux leçons à produire (11 le 15/10, 12 — le BILAN — le 22/10), après quoi le job sera supprimable — une somme de plafonds, *pas* une dépense (voir `outils/scripts/JOBS.md`). ⚠️ Le plafond s'applique **par tentative, pas au cumul** : un job à 3 tentatives peut dépenser trois fois son plafond. Depuis le 27/09/2026, un dépassement coupe les tentatives (fail-fast élargi à `error_max_budget_usd`) et un `exit 0` obtenu en moins de **7 tours** après un échec **n'est plus publié** — le runner sort en **exit 7** et laisse le travail sur le disque. ⚠️ **Depuis le 29/09/2026 cette mémoire d'échec survit au processus** : un run qui échoue pose `outils/scripts/logs/.echec_<job>` (gitignoré, valable **72 h**), relu au démarrage du suivant. Sans cela, `rattrapage_jobs.sh` repartait vierge — incident `hypnose-lecon` du 29/09 : le run de 9h03 meurt sur la limite d'usage après avoir écrit la leçon (exit 1, non contrôlée, non commitée), le rattrapage de 19h18 s'arrête sur le doublon en **2 tours**, rend exit 0, et **publie un livrable que personne n'avait vérifié**. Un `exit 7` **maintient** la marque ; seul un `exit 0` franc la lève. Témoin **S15** et trois mutations dans `non_regression_runner.sh`.
- **L'auto-push suit une liste blanche stricte** — `sources/veille/` + `livrables/{lecons,quiz,infographies,projets,controles,documents}`. **Jamais `git add -A`** : `contexte/`, `sources/rbpp`, `sources/tnmp`, `sources/qvct`, `en_cours/`, `ressources/`, `outils/` et `NotebookLM/` restent hors publication automatique.
- ⛔ **`revenus-passifs-lecon` a été SUPPRIMÉ le 04/10/2026**, après avoir été arrêté le même jour. Le parcours avait été commandé en **10 leçons** ; le job en a produit une **onzième** le 04/10. Deux causes cumulées dans son prompt : la numérotation « NN = nombre de fichiers existants + 1 » était **sans limite**, et une ligne de sa feuille de route **lui ordonnait de continuer** — *« Si les 10 thèmes sont couverts, approfondis un thème sous un nouvel angle »*. ⚠️ **Et l'incident avait été prédit par écrit, avec sa date** : l'audit de la leçon 10, le **27/09/2026**, concluait dans `JOBS.md` « le prochain déclenchement est le dimanche 4 octobre 2026 à 7h03 : un onzième livrable sortira d'un parcours qui s'est déclaré fini ». Rien n'a été fait de la semaine. **Les 11 leçons produites sont conservées** dans `livrables/lecons/revenus-passifs/`, la 11e fichée — elle est juste sur le fond. **Le prompt de 62 425 octets reste récupérable dans l'historique git** : `git show d39b132:jobs_config.json`. C'est la quatrième suppression de job du dépôt, après `rgpd-veille` (25/07/2026), `nocode-ia-veille` (02/08/2026) et `entretien-motivationnel-lecon` (10/08/2026) — les deux parcours clos l'avaient été de la même façon. 🟢 **Le trou a été fermé le 04/10/2026 sur les deux autres parcours courts** : `appli-ia` (12/12) et `astrologie-karmique` (9/12) portent désormais la même clause **⛔ PARCOURS FERMÉ — 12 LEÇONS** et la limite `dans la limite de 12` sur la numérotation. `appli-ia` ne produira donc plus rien à partir du **vendredi 09/10/2026** : il s'exécute, compte 12, affiche son message et sort — c'est le comportement attendu. `astrologie-karmique` continue jusqu'à la leçon 12 du **22/10/2026**, la clause mordant pour la première fois le **29/10**.
- ⛔ **`appli-ia-lecon` a été SUPPRIMÉ le 04/10/2026**, le même jour que `revenus-passifs` et quelques heures après qu'une clause de fermeture y avait été posée — clause devenue sans objet. Le parcours était **fermé à 12 leçons**, les 12 sont livrées et la dernière est un bilan (02/10/2026). **Le créneau du vendredi 8h03 est désormais libre.** Conservés : les **12 leçons** dans `livrables/lecons/appli-ia/` et le **projet fil rouge** complet dans `livrables/projets/appli-ia/` (code, `PROJET.md`, `SPEC.md`, base SQLite). Son prompt de **121 604 octets**, le plus gros du dépôt, reste lisible par `git show 14541bb:jobs_config.json` — ⚠️ c'est là que vit l'original du bloc dont `controle_attributions.py` est la copie canonique, et le docstring du contrôle renvoie désormais à ce commit. **Cinquième suppression de job du dépôt.**
- 🧪 **`outils/scripts/controle_clauses_parcours.py` rend ce constat rejouable** : pour chaque job de leçon il compare le nombre annoncé par le prompt, le nombre réel de `.docx`, la présence de la clause et celle de la limite, et **refuse** un parcours arrivé à sa limite sans clause. Validé dans les deux sens le 04/10/2026 : exit 0 sur la config du dépôt, exit 1 avec la clause d'`appli-ia` retirée. Il accepte un chemin de config en argument, pour se tester sans toucher au dépôt.
- **`setup_launchd.sh` ne synchronise que les CRÉNEAUX, pas les prompts** (précisé le 11/09/2026) : le `.plist` ne porte que `run_job.sh` + l'`id` du job, et le prompt est relu dans `jobs_config.json` à chaque exécution. À relancer **seulement** après création, suppression, renommage d'un job ou changement de son `cron` — **pas** pour un durcissement de prompt : recharger tue le job en vol (le script refuse si l'un tourne, `--force` passe outre).
- Toute création, suppression ou recréation de job se répercute **ici et dans `jobs_config.json`** : les deux se relisent ensemble.
- **Les contrôles communs** (`outils/scripts/controle_attributions.py`, `controle_decompte.py`) sont appelés par les prompts, jamais copiés. 🆕 **Depuis le 08/10/2026, deux étapes 5 bis suivent la même règle** : `controle_astrologie_karmique.py` (7 motifs) et `controle_psychopathologie.py` (4 motifs) sont sortis de leurs prompts, où ils étaient inlinés et réémis à chaque tour — 12 398 et 5 520 octets. Les deux prennent le chemin du `.docx` en argument et ont été **validés dans les deux sens** contre leur version inlinée, verdicts identiques exit compris. ⚠️ **Ils ne sont pas encore câblés dans `non_regression.sh`** : une retouche de l'un des deux ne serait détectée par aucun harnais. **Toute retouche se rejoue avec `outils/scripts/non_regression.sh`** (90 s, diff des verdicts sur les 221 documents) avant d'être poussée — le hook `outils/scripts/hooks/pre-push` (`git config core.hooksPath outils/scripts/hooks`, une fois par clone) le lance et **refuse le push** si un verdict a changé — en mode `--complet` (aspiration, 4-5 min de plus) quand `controle_attributions.py` ou `extract_docx.py` est touché, puisque les passes B/C2/D ne s'exercent que là : témoins **conformes** (doivent sortir en 0, dont les copies figées de `non_regression/temoins_attributions_conformes/`) et témoins **d'avant correction** (doivent sortir en 1). Les pushs des jobs passent par le même hook en mode `--docs` (quelques secondes) : un livrable ou une veille qui régresse, ou un document nouveau qui bloque, **n'est pas publié** — le log du job dit pourquoi. Le hook détecte les fichiers **ajoutés, modifiés ET renommés** (`--diff-filter=AMR`) : sans le `R`, un `git mv` — y compris un renommage avec modification, que git compte encore comme `R` au-dessus de 50 % de similarité — publiait un document sans contrôle (23/09/2026).

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
