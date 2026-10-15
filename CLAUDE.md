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
│   │   ├── stoicisme/ · hypnose/ · placement-financier/ · astrologie-karmique/   ← parcours actifs
│   │   ├── psychopathologie/ · enneagramme/ · dzogchen/   ← CLOS 20/20, jobs supprimés le 15/10/2026
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

## Parcours clos — rien à produire

**`psychopathologie` · `dzogchen` · `enneagramme`** : 20/20, bilans livrés les 12, 13 et 14/10/2026, jobs supprimés le **15/10/2026**. Les 60 leçons sont conservées. Créneaux libérés : **lundi 8h03, mardi 8h03, mercredi 9h03**.

`appli-ia` (12/12, job supprimé le 04/10/2026, projet fil rouge conservé dans `livrables/projets/appli-ia/`) · `revenus-passifs` (11 leçons, supprimé le 04/10/2026) · `nocode-ia` (16 leçons) · `entretien-motivationnel`. Détail et commits des prompts : `outils/scripts/JOBS.md`.

## Jobs planifiés

**9 jobs** hebdomadaires via **launchd** (app fermée) : launchd → `outils/scripts/run_job.sh <job_id>` → `claude -p` headless.

### Invariants — à ne pas réapprendre

| Règle | Détail |
|---|---|
| Source de vérité des **prompts** | `jobs_config.json`. `run_job.sh` le relit à chaque run → **aucun reload launchd pour un changement de prompt** |
| Source de vérité des **plafonds** | `run_job.sh`, bloc `case "$JOB_ID"`. Cumul **32 $/semaine** sur 9 jobs (42 → 32 le 15/10/2026, trois parcours clos supprimés) |
| Le plafond s'applique **par tentative** | pas au cumul : un job à 3 tentatives peut dépenser 3× son plafond. Un dépassement coupe les tentatives |
| `TOURS_MINI=7` | un `exit 0` obtenu en moins de 7 tours **après un échec** n'est pas publié → **exit 7** |
| Mémoire d'échec sur disque | `outils/scripts/logs/.echec_<job>`, gitignoré, **72 h**. Un `exit 7` la maintient, seul un `exit 0` franc la lève |
| `setup_launchd.sh` | synchronise les **créneaux SEULEMENT**. À relancer uniquement après création, suppression, renommage ou changement de `cron` |
| Auto-push | **liste blanche stricte** : `sources/veille/` + `livrables/{lecons,quiz,infographies,projets,controles,documents}`. **Jamais `git add -A`**. Hors publication auto : `contexte/`, `sources/{rbpp,tnmp,qvct}`, `en_cours/`, `ressources/`, `outils/`, `NotebookLM/` |
| Clause de fermeture | tout parcours fermé porte **⛔ PARCOURS FERMÉ — N LEÇONS** + la limite sur la numérotation. `controle_clauses_parcours.py` **refuse** un parcours arrivé à sa limite sans clause |
| Toute création/suppression de job | se répercute **ici ET dans `jobs_config.json`** |

**Huit jobs supprimés à ce jour** : `rgpd-veille`, `nocode-ia-veille`, `entretien-motivationnel-lecon`, `revenus-passifs-lecon`, `appli-ia-lecon`, puis **`psychopathologie-lecon`, `dzogchen-lecon` et `enneagramme-lecon` le 15/10/2026** (parcours clos 20/20, bilans livrés les 12, 13 et 14/10). `astrologie-karmique-lecon` suivra après sa leçon 12 du 22/10. **Les prompts restent récupérables dans l'historique git** — les trois derniers par `git show 4b697a6:jobs_config.json` (63 560, 48 272 et 41 350 octets).

🔴 **⚠️ SUPPRIMER UN JOB DEMANDE QUATRE GESTES, PAS UN — mesuré le 15/10/2026.** `setup_launchd.sh` porte sa **propre liste de créneaux en dur** et ne lit **pas** `jobs_config.json` : le lancer après avoir retiré un job de la config **le réinstalle**, et il n'a jamais su retirer un `.plist` orphelin. Un job supprimé restait donc **planifié indéfiniment**, à appeler un id que `run_job.sh` ne connaît plus. La séquence complète :
> ① retirer le job de `jobs_config.json` · ② retirer son `case BUDGET` de `run_job.sh` · ③ retirer sa ligne de la liste `JOBS` de `setup_launchd.sh`, puis le relancer · ④ `launchctl unload` **et** `rm` le `.plist`. Puis ⑤ le skill `.claude/skills/lancer-job/SKILL.md`, qui porte sa propre table de correspondance.
>
> `setup_launchd.sh` **nomme désormais les orphelins** avec les deux commandes à passer.
> ✅ **Les huit suppressions ont été vérifiées le 15/10/2026 sur onze emplacements : aucun orphelin de planification.** 9 `.plist`, 9 chargés, aucun `case BUDGET`, aucune ligne `JOBS`, `rattrapage_jobs.sh` commenté aux dates, `restaurer-jobs` et `maj_xlsx_jobs.py` qui relisent la config, rien dans `/Library/Launch*`, coffre Obsidian à 9/9. **Le défaut est réel — je l'ai reproduit — mais il n'a jamais mordu en production.** ⛔ **Un seul vrai orphelin, et il n'est pas dans la planification** : `livrables/documents/2026-08-09_Les 14 Jobs.xlsx` porte encore **5 jobs supprimés** et s'intitule « Tes 14 jobs » pour 9 jobs réels. `maj_xlsx_jobs.py` y écrit après chaque job réussi mais **ne met à jour qu'une colonne** — il n'ajoute ni ne retire jamais de ligne, donc rien ne le corrigera tout seul. 📌 Piste bornée : lui faire lire `JOBS` depuis `jobs_config.json` — déclaré « source de vérité unique des jobs », il ne l'est pas pour les créneaux, et c'est tout le défaut.

### Les contrôles — appelés par les prompts, jamais copiés

| Script | Rôle |
|---|---|
| `controle_attributions.py` | passes A, A2–A6, B, B-FR (㉖), B-NOM (㉙), C, C2, D, ㉜ (ouvrage sans page), ㉞ (HTTP 000), ㉟ (locale des nombres). Exit 1 = bloquant, 3 = pages non lues, 0 = propre |
| `controle_decompte.py` | décompte des éditions d'une série de veille |
| `controle_edition_precedente.py` | relit une veille à l'**édition précédente et à sa fiche**. 3 motifs ; ① seul est bloquant |
| `controle_clauses_parcours.py` | annoncé vs réel vs clause vs limite |
| `controle_astrologie_karmique.py` · `controle_psychopathologie.py` · `controle_ai_act.py` | étapes **5 bis** sorties des prompts (7, 4 et 11 motifs). ⚠️ `controle_psychopathologie.py` est **conservé** après la suppression de son job : il garde un témoin et une mutation du harnais |
| `audit_vault.py` | 9 contrôles du coffre Obsidian après chaque job |
| `aspirer.py` + `chercher.py` | 🆕 15/10/2026 — **vérifier une citation sans faire entrer la page dans le contexte**. Voir « Calibrage » ci-dessous |

### Le harnais — `outils/scripts/non_regression.sh`

`--docs` (secondes, **porte des pushs de job**) · défaut (~90 s) · `--complet` (+ aspiration, ~25 min) · `--accepter`.
Le hook `outils/scripts/hooks/pre-push` le lance et **refuse le push** si un verdict a changé (`git config core.hooksPath outils/scripts/hooks`, une fois par clone). Détection `--diff-filter=AMR` — sans le `R`, un `git mv` publiait sans contrôle.

⚠️ **La référence (`reference/passe_A.tsv`) ne stocke que le nombre de problèmes BLOQUANTS des passes A/A2/A3/A4.** Les passes B, C2, D, A6, ㉜, ㉞, ㉟, les étapes 5 bis et la relecture d'édition sont **invisibles au diff**. D'où la règle qui suit.

### Règles de méthode — chacune payée par un incident

🔧 **Outillage**
- Un motif **non bloquant** ou post-aspiration se garde par une **EXIGENCE DE LIGNE** sur un témoin figé, **jamais par un code de sortie seul**.
- Un motif qu'on **RESSERRE** a besoin d'un témoin qui doit être **ACCEPTÉ** (convention `0:motif` en section 5 ter) — sinon rien n'empêche de le réélargir demain.
- **Un balayage rétrospectif ne valide pas un motif bloquant.** Les 73 éditions du 12/10 précédaient toutes le contrôle ; la 74ᵉ l'a cassé en 48 h. Avant de rendre un motif bloquant en `--docs`, le faire tourner en **AVERTISSEMENT** sur des éditions neuves.
- **Une mutation doit tomber là où le motif regarde** : un paragraphe ajouté en fin de document n'atteint pas un motif qui n'examine que les paragraphes liés.
- **Un test qui teste une COPIE de la logique ne garde rien** (15/10/2026 : l'auto-test de `chercher.py` réimplémentait sa cascade — un sabotage du vrai chemin passait).
- **Un garde qui ne fait pas sortir en 1 est décoratif** (15/10/2026 : `cmd | tail -1` teste le code de `tail`).
- **En production, un faux refus coûte un livrable non publié ; un vrai manqué ne coûte qu'une relecture humaine.** C'est pourquoi ㉜, D, ㉞ et ㉟ ne sont pas bloquants.

🔍 **Mesure**
- **NE JAMAIS lancer plusieurs contrôles en parallèle.** `classics.mit.edu`, `wikipedia.org`, `has-sante.fr` limitent le débit : 11 contrôles en parallèle ont fait basculer **4 documents sains en « bloquant »**. Un verdict « ABSENTE » **ne vaut que rejoué seul**, avec 15 s d'intervalle.
- **Une page tronquée rend indiscernables une citation absente et une citation non lue.** Plancher : **3 000 caractères utiles** = façade ou page rendue en JS.
- **Une détection ㉜ n'est pas une propriété du document** mais de l'état de lecture des pages : une page non lue gonfle ㉜. Un décompte ㉜ sans le décompte des pages lues ne veut rien dire.
- **Chercher la variante de graphie AVANT de conclure à l'absence** — `chercher.py` le rend mécanique.
- **Le champ « Last update » d'une page institutionnelle n'est pas citable entre guillemets** : il change et périme le témoin.
- **Quand la page d'une citation est intermittente, le littéral va dans le MARQUEUR et le corps reste en style indirect.**

✍️ **Normalisation**
- **NFC d'abord** : les marqueurs sont écrits tantôt « é » précomposé, tantôt « e » + U+0301. `\[Corrigé le` ne trouve alors **rien** ; `MARQUEUR` n'y survit que parce qu'il liste aussi `Corrige`, `Precise`, `Ajoute` — ce ne sont **pas** des redondances.
- **Un jeton se cherche ponctuation CONSERVÉE** : avec une clé qui l'écrase, « 1 338 » s'apparie à « 1 338,23 ».
- **`re.escape` échappe l'espace en Python 3.9** : toute substitution dans un motif échappé a besoin d'un `\\?` devant la classe, sinon elle produit un crochet littéral. Bug de la passe D (10/10), reproduit à l'identique le 15/10.
- **Le point n'est JAMAIS un séparateur de milliers** : dans un texte anglais c'est la décimale. Le chercher ainsi déclare **présent un nombre absent** — la pire direction.
- **Un correcteur écrit dans la même langue que les motifs** : un titre entre guillemets à côté d'un domaine est une citation attribuée (㉖) ; une date `JJ/MM` dans une veille est lue comme un décompte.

### Doctrine des ordres

| Ordre | Ce qu'il déclenche |
|---|---|
| **« écris la fiche X »** | Audit **standard** (voir « Calibrage ») puis une fiche `.md` : frontmatter, `# nom`, `Document source : [[X.docx]]`, `## Résumé` (paragraphes denses ouvrant chacun sur une phrase d'attaque en gras), `## Notes liées` (⬅️ Précédente / ➡️ Suivante / 🔗 Pont / 🗂️ Dossier) |
| **« corrige X »** | Sauvegarde dans le scratchpad **d'abord**. Patch du XML `.docx`, édits **par position, de la fin vers le début**, échanges **locaux à un run**, marqueur gris italique daté `[Corrigé le JJ/MM/AAAA : …]`, libellé d'origine conservé dans un **📝 Journal des corrections** final avant `<w:sectPr>`. Puis fiche + `JOBS.md` + commit + push |
| **« porte / apprends … une règle »** | Mesurer l'incident réel, **borner** la règle, valider **dans les deux sens** sous `env -i`, câbler un **témoin avec exigence de ligne**, consigner ici et dans `JOBS.md` |

> 📄 **Tout le reste — horaires des 14 créneaux, plafonds détaillés et leurs justifications, authentification headless, retry, veille macOS, garde-fous des cinq familles, et l'historique daté des incidents — est dans `outils/scripts/JOBS.md`.** Lis-le avant toute intervention sur la planification, les prompts de job ou les coûts.

---

## Calibrage de la consommation — décidé le 15/10/2026

Le constat qui fonde cette section : **une seule page aspirée dans le contexte pèse plus que tout le reste d'une session.** Les fiches du Minor Planet Center font 600 000 à 900 000 caractères, `growingself.com` 744 580 octets. Les contrôles du dépôt aspirent 394 hôtes sans qu'une page entre jamais en contexte — ils ne rendent que des verdicts. Le gaspillage venait de **moi**, qui rouvrais les pages à la main pour vérifier une citation.

### ① Vérifier une citation sans faire entrer la page dans le contexte

```bash
aspirer.py <url>…                    # → disque. Rend : HTTP, octets, caractères utiles, chemin
chercher.py "<texte>" <page.txt>…    # → ① LITTÉRAL ② GRAPHIE ③ LOCALE ④ ABSENT
chercher.py --fichier requetes.txt <page.txt>…    # un lot de requêtes
```

**C'est plus fiable, pas seulement moins cher** : les quatre quasi-fausses accusations des 13-14/10/2026 — « left prefrontal » / « left **side of the** prefrontal cortex », « neuf facteurs » / « moins de **9** facteurs », « Acceptation » / « outil d'**acceptation** », « identify their type » / « able to accurately **predict** » — venaient toutes d'une lecture à l'œil d'un dump. Le degré ④ est **tenu de montrer ce que la page écrit à la place**. 21 auto-tests, 9 mutations, câblés dans **tous** les modes du harnais (0,1 s, aucun appel réseau).

⚠️ Le degré ② (accents, casse et ponctuation pliés) **suffit pour « la source le dit », PAS pour une citation entre guillemets** — une citation se prouve au degré ①. Et ② est **interdit aux chiffres** : la clé écrase la ponctuation, donc « 1 338 » s'y apparierait à « 1,338 ».

### ② Profondeur par défaut de « écris la fiche X » : **STANDARD**

| | **Standard** (défaut) | Rapide (sur demande) | Audit complet (sur demande) |
|---|---|---|---|
| Sources | aspirées, vérifiées par **appariement exact** | non rouvertes | rouvertes **et lues** |
| Citations, chiffres, dates | `chercher.py`, degré exigé ① | non garanties — **la fiche le dit** | lecture intégrale |
| Tests mécaniques du job | rejoués verbatim sous `env -i` | contrôles communs seuls | rejoués |
| Continuité N-1 **et leçons du parcours** | oui | non | oui |
| Pages en contexte | **aucune** | aucune | toutes |

**Ce que « standard » perd, et il faut le dire** : la lecture au jugé d'une page entière repère parfois un défaut qu'on ne cherchait pas — l'appariement exact ne trouve que ce qu'on lui demande. → Donc toute fiche **liste les requêtes passées**, pour qu'on voie ce qui n'a pas été interrogé.

### ③ Modèle

**Sonnet en routine** (fiches, corrections `.docx`, rejeu de tests, balayages) · **Opus sur demande** pour ce que la semaine du 12-15/10 a montré que seul lui attrape : qu'un bilan contredit sa propre leçon 9, qu'une borne « OU » va casser en production, qu'une liste de chantiers repose sur une prémisse fausse. Bascule par `/model`.

### ④ Rapports

**Un écran par défaut** : verdict · défauts mesurés · mesures du job (coût, tours, exit) · une ligne d'avocat du diable. Le détail sur demande. ⚠️ **Ce qui ne se raccourcit jamais** : un défaut mesuré, un faux positif d'un contrôle, et mes propres erreurs.

### ⑤ Hygiène

- **Ne jamais relire un fichier qu'on vient d'éditer** pour vérifier : l'édit aurait échoué.
- Lectures **ciblées** (`sed -n`, `grep -n`) plutôt que fichiers entiers — `JOBS.md` fait 780 ko.
- Du harnais, lire la **dernière ligne** et les `✗`, pas les 100 lignes.
- Grouper les lectures de fichiers indépendantes en un seul appel. ⚠️ **Jamais les contrôles réseau** — règle du 12/10.

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
