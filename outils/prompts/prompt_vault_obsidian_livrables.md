# Prompt — Construire un vault Obsidian par-dessus les livrables

**Produit le 14/08/2026** par reverse engineering, à l'issue de la session qui a
réellement construit ce vault (95 fiches, automatisation, garde-fous).

Ce prompt est **autonome** : collé seul dans une session neuve, il doit produire
le même résultat en une passe. Il intègre les décisions qui, ce jour-là, ont
demandé un aller-retour — et surtout le piège de numérotation qui a failli
corrompre les neuf parcours.

**Usage** : rejouer l'opération sur un autre dépôt, ou la reprendre à zéro ici
après un incident. Pour ajouter les fiches manquantes au fil de l'eau, il n'y a
rien à relancer : `outils/scripts/fiches_obsidian.py` s'en charge, appelé par
`run_job.sh` après chaque job réussi.

---

## Le prompt

```text
Tu es expert Obsidian et gestion de connaissances personnelle.

CONTEXTE
Dépôt /Users/utilisateur/kDrive/Claude_Travail, versionné sur GitHub (dépôt public).
- livrables/lecons/ contient ~95 leçons .docx produites depuis avril 2026 par des
  jobs planifiés (launchd), répartis en une douzaine de parcours thématiques.
  Nommage : YYYY-MM-DD_lecon-<parcours>_NN_<slug>.docx
  Exception historique : YYYY-MM-DD_leconNN_<slug>.docx (3 leçons d'avril).
- jobs_config.json définit les jobs ; outils/scripts/run_job.sh les exécute puis
  auto-commite et pousse une liste blanche de dossiers.
- outils/scripts/extract_docx.py extrait le texte d'un .docx.
Je suis chef de service en ESSMS : certains parcours servent mon métier, d'autres
relèvent d'un intérêt personnel ou patrimonial.

OBJECTIF
Construire un vault Obsidian exploitable par-dessus ces leçons, sans jamais lire,
modifier ni déplacer un seul .docx.

1. UNE FICHE MARKDOWN PAR LEÇON, même nom, même dossier, créée seulement si absente.
   Frontmatter : type, source (nom exact du .docx), date_creation, date_lecon,
   parcours, numero, statut (parcours-actif si un job du même nom existe encore
   dans jobs_config.json, parcours-archive sinon), tags.
   Corps : titre H1, ligne "Document source : [[nom_exact.docx]]",
   section "## Résumé", section "## Notes liées".

2. CLASSER, RÉSUMER, RELIER après lecture réelle des documents.
   Méthode obligatoire en DEUX PASSES : d'abord lire chaque parcours et produire
   un index compact (une ligne par leçon : concepts, auteurs, notions) ; ensuite
   calculer les liens depuis cet index seul. Sans cela les liens se fondent sur
   les titres et sonnent creux.

   Tags hiérarchiques Obsidian (axe/valeur) :
   - parcours/<nom> et registre/<pro|perso|mixte|prive> sur toutes les fiches.
     mixte = parcours personnel comportant des applications professionnelles
     explicites, ou l'inverse.
   - module/<niveau> selon la progression interne du parcours.
   - un axe secondaire ADAPTÉ AU DOMAINE, pas un axe unique : trouble/ et
     classification/ en clinique, technique/ en hypnose, enveloppe/ et actif/ en
     finance, type/ et centre/ en typologie, pratique/ et texte/ en spiritualité,
     outil/ et notion/ en informatique.

   Résumés : 3 à 4 paragraphes, une idée forte par fiche mise en gras, en français,
   registre professionnel. Résumer le document, pas le paraphraser.

   Liens : séquentiels (précédente/suivante), intra-parcours, et surtout
   TRANSVERSAUX entre parcours. Chaque lien porte une justification d'une à trois
   lignes. Privilégie les rapprochements qui apprennent quelque chose, y compris
   les DÉSACCORDS entre deux sources — pas seulement les convergences.

3. CLOISONNEMENT GIT (impératif)
   - Ajouter ':(exclude)livrables/lecons/*.md' au git add de run_job.sh, pour que
     mes annotations personnelles ne partent jamais seules sur le dépôt public.
     Ne pas élargir : PROJET.md, SPEC.md et les veilles .md doivent rester couverts.
   - Ignorer .obsidian/ et *.canvas dans .gitignore.
   - Committer les fiches manuellement, une fois renseignées.

4. AUTOMATISER LA SUITE
   Script outils/scripts/fiches_obsidian.py, idempotent, appelé par run_job.sh
   après un job réussi : il crée la fiche VIDE (tags "a-classer", sections vides)
   de toute leçon qui n'en a pas. Ce qui est déductible du nom de fichier est
   pré-rempli, le reste suppose la lecture. Son échec ne doit pas affecter le
   livrable. Ignorer les fichiers temporaires Office (~$…).

⚠️ PIÈGE À NEUTRALISER AVANT TOUTE CHOSE
Les prompts des jobs comptent leurs leçons avec `ls | grep lecon-<parcours>`.
Ajouter un .md par .docx DOUBLE ce compte et fausse la numérotation de toutes les
leçons suivantes, sur tous les parcours. Corrige d'abord ces commandes dans
jobs_config.json pour qu'elles filtrent sur `.*\.docx$`, insère une note
explicative dans chaque prompt, puis vérifie parcours par parcours que le compte
attendu est retrouvé.

VÉRIFICATIONS ATTENDUES, à me montrer
- tous les liens wiki pointent vers un fichier existant (aucun lien cassé) ;
- aucune fiche restée "a-classer" ;
- `git add --dry-run` prouve que les .md de lecons sont exclus, y compris après
  modification d'une fiche ;
- un job réellement exécuté produit le BON numéro et sa fiche automatique.

Ne modifie aucun .docx. N'écrase aucune fiche existante. Montre-moi la taxonomie
obtenue et la carte des ponts entre parcours à la fin.
```

---

## Ce que ce prompt ne remplace pas

Trois choses ont exigé un aller-retour réel le 14/08, et aucun prompt initial ne
les couvre :

1. **L'arbitrage sur le tag `mixte`.** Il a fallu voir le pilote pour constater
   que les leçons 01 et 02 de stoïcisme contenaient des sections « pont pro
   ESSMS ». La décision appartenait à l'utilisateur.

2. **Le pilote lui-même.** Lancer sur 95 fiches sans juger le format sur 10
   aurait été un pari. Faire valider la longueur des résumés, la taxonomie et la
   pertinence des liens sur un seul parcours a coûté dix minutes et évité un
   retraitement complet.

3. **Le piège de numérotation.** Il figure ici parce qu'il est désormais connu.
   Il a été découvert en préparant un lancement de test — pas par raisonnement a
   priori. Un prompt écrit la veille l'aurait manqué.

C'est la limite de l'exercice : **le prompt parfait contient ce que seule
l'exécution a révélé.**

---

## Résultat obtenu le 14/08/2026

| | |
|---|---|
| Fiches | 97, aucune restée « a-classer » |
| Liens | 324, aucun cassé |
| Ponts entre parcours | 35 |
| Tags distincts | 381, sur quatre axes |
| Registres | 43 mixte · 21 pro · 21 perso · 12 privé |
| Statuts | 67 actifs · 30 archivés |
| Automatisation | validée sur deux jobs réellement exécutés |

Commits de référence : `146133c` (les 95 fiches), `ed3e078` (automatisation),
`dfb0bf8` (correction de la numérotation), `afa8edb` (exclusion de l'auto-push).
