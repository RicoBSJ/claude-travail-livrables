---
type: fiche-document
source: 2026-09-26_lecon-appli-ia_10_securite-donnees.docx
date_creation: 2026-09-26
date_lecon: 2026-09-26
parcours: appli-ia
numero: 10
statut: parcours-actif
tags:
  - parcours/appli-ia
  - registre/technique
  - projet/portail-livrables
  - techno/node
  - techno/sqlite
  - notion/secrets-environnement
  - notion/npm-audit
  - notion/entetes-securite
  - notion/rgpd
  - source/nodejs-org
  - source/docs-npmjs
  - source/cnil
  - source/owasp
  - theme/plafond-depasse
  - theme/memoire-non-mise-a-jour
  - theme/signature-api-de-memoire
  - theme/promesse-non-tenue
  - alerte/a-corriger
---

# 2026-09-26_lecon-appli-ia_10_securite-donnees

Document source : [[2026-09-26_lecon-appli-ia_10_securite-donnees.docx]]

## Résumé

**Le fait central n'est pas dans la leçon, il est dans son exécution : le job a dépassé son plafond, a été tué, et a publié quand même.** Tentative 1, lancée manuellement à 17:40 : **3,0689 $ pour un plafond de 3,00 $ — 102 %**, `subtype=error_max_budget_usd`, `stop_reason=tool_use`, **64 tours, 14 min 04 s**, 5 047 161 tokens de cache lu. Le processus a été coupé en plein travail. Quatre-vingt-dix secondes plus tard, `run_job.sh` a relancé : **tentative 2, 3 tours, 9,9 secondes, 0,2141 $** — et `subtype=success`, `stop_reason=end_turn`. Le runner a écrit **« ✅ Succès à la tentative 2 »**, l'audit du vault a dit « conforme », et le push est passé. **Une exécution de dix secondes qui n'a rien pu produire a validé le travail partiel de celle qui l'avait précédée** : la tentative 2 s'est très probablement arrêtée sur la vérification de doublon, la leçon du jour étant déjà sur le disque. Le plafond est appliqué **par tentative**, pas au cumul : le coût réel de ce livrable est **3,2830 $**. C'était la question ouverte depuis hier soir — *« la prochaine exécution dira si la marge existe encore »* — et la réponse est non : le prompt est passé de 74 610 à **107 602 octets** (+44 %) entre la n°09 et la n°10, et la n°09 coûtait déjà 2,7036 $, soit 90 % du plafond.

**Et la casualty de la coupure est exactement celle qui compte : `PROJET.md` n'a pas été touché.** Même taille, même empreinte `79e4d887b1560ee9ede9ecd394aa2f55` avant et après — vérifié sur un état capturé avant le lancement. L'étape 6 du prompt appelle ce fichier *« la seule mémoire du parcours »*, et la règle 4 impose à chaque leçon de s'enchaîner sur l'état qu'il décrit. **La leçon 11 lira donc un `PROJET.md` qui ignore tout de la 10** : ni `normaliserSlug`, ni la colonne `slug_normalise`, ni les en-têtes de sécurité, ni `audit-securite.js`, ni le passage de `package.json` en 0.9.0. Le commit `8322368` a pourtant tout poussé — `.env.example`, `audit-securite.js` (146 lignes), et les modifications d'`indexer.js`, `serveur.js`, `utils.js`. C'est le scénario que l'étape 5 bis du prompt décrit depuis le 21/08 pour un autre cas : *« un document invalide est PIRE qu'une absence de leçon : run_job.sh l'auto-commit et le pousse sur le dépôt public comme un succès »*. Ici le document est valide ; c'est la mémoire qui manque, et rien ne la vérifie.

**Sur le contenu, en revanche, cette leçon est la mieux mesurée du parcours, et je l'ai rejouée intégralement.** **Les quatre décomptes de lignes sont exacts au chiffre près** — `utils.js` 121, `indexer.js` 162, `serveur.js` 303, `audit-securite.js` 146 : la règle 22, écrite hier après le « environ 90 lignes » de la n°06, a tenu dès sa première exécution. **Les quatre sorties mesurées sont exactes au caractère près** : `node scripts/audit-securite.js` rend bien les cinq contrôles et le « Bilan : 5 contrôle(s) OK · 0 problème(s) » ; la validation du PORT rend `PORT invalide : "abc" — doit être un entier entre 1 et 65535` et un **code de sortie 1** pour les deux variantes ; `curl -s -I` rend les **quatre en-têtes**, CSP complète comprise (`default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'`) ; et la démonstration SQL tient — `slug LIKE '%leçon%'` rend **0 résultat**, `slug_normalise LIKE '%lecon%'` en rend 308 le 26/09 et **310 à ma relecture**, l'écart étant les deux fichiers que le job a lui-même ajoutés après sa mesure, ce que la leçon anticipe en toutes lettres. `npm test` rend **33 tests, 0 fail**, l'indexeur ses six catégories, les **quatre URL répondent 200**, et la continuité avec la n°09 est exacte (33 tests, 17 + 16, et la recherche qui « utilisait LIKE sur le champ slug brut »). L'étape 5 bis passe ses **quinze motifs**, dont les six écrits hier et avant-hier.

**Le défaut de contenu est une signature d'API écrite de mémoire — sur la page que la leçon cite elle-même.** `scripts/audit-securite.js` lit `meta.totalDependencies` pour annoncer le nombre de dépendances analysées. **Ce champ n'existe pas dans npm audit v10.** Mesuré : `npm audit --json` rend `metadata.dependencies` = `{prod: 3, dev: 23, optional: 20, peer: 0, peerOptional: 0, total: 25}` — le champ est `metadata.dependencies.total`, et il vaut **25**. `totalDependencies` appartient au format de npm 6. Le repli `|| '?'` se déclenche donc **à chaque exécution**, et le script imprime `✓ 0 vulnérabilité trouvée (? dépendances analysées)`. La leçon reproduit cette ligne telle quelle dans sa sortie mesurée — **elle est donc parfaitement honnête, et elle publie un point d'interrogation comme un résultat normal**. C'est le garde-fou nominal du parcours qui saute (*« ne jamais écrire de mémoire une signature d'API »*), dans une leçon dont une ressource est `docs.npmjs.com/cli/v10/commands/npm-audit/`. S'y ajoute une **promesse non tenue** : la n°09 annonçait que *« la règle de base sur la branche path traversal du serveur sera revue et blindée »* — « traversal » compte **zéro occurrence** dans la n°10, qui a traité les secrets, `npm audit`, les en-têtes et le RGPD, mais pas celle-là.

**Deux bloquants de `controle_attributions` sont des faux positifs, et le hook ne les a pas vus non plus.** La passe B refuse deux « citations anglaises » : `SELECT COUNT(*) as n FROM livrables WHERE slug LIKE @m` et sa jumelle sur `slug_normalise`. Ce sont des requêtes SQL écrites **entre guillemets droits à l'intérieur d'un bloc de code** — `db.prepare("…")` — et le filtre anti-code de la passe (`[<>{}=]`, `//`, `\w\(\)`) ne les attrape pas : `COUNT(*)` n'est pas `COUNT()`. Même famille que le piège ⑮ du 12/09, le guillemet droit collé à un chiffre pris pour une citation. **Le document est juste, c'est le contrôle qui se trompe** — et il faudra le corriger dans `controle_attributions.py`, donc avec un `--complet` sur 247 documents. Ce qui mérite d'être relevé pour soi-même : le hook a **autorisé le push** parce qu'il ne lance que `--docs`, c'est-à-dire les passes A/A2/A3/A4, sans réseau. Les deux bloquants vivent dans les passes réseau. **Les deux faits de la journée se rejoignent ici** : ce que le hook vérifie n'est pas ce qui bloque, et ce que le runner appelle un succès n'est pas ce qui a été fait.

## Notes liées

- **⬅️ Précédente** · [[2026-09-25_lecon-appli-ia_09_qualite-tests-debogage]]
  **elle annonçait quatre thèmes, la 10 en traite trois** : secrets, `npm audit` et RGPD sont là, le **path traversal « revu et blindé » n'y est pas** (zéro occurrence). Et c'est elle qui coûtait 2,7036 $ — 90 % du plafond — avec un prompt 44 % plus court : la 10 l'a fait exploser
- **🔗 Pont** · [[2026-09-04_lecon-appli-ia_06_recherche-filtres]]
  **la règle 22 est née de son « environ 90 lignes » hier, et elle a tenu aujourd'hui** : les quatre décomptes de la 10 sont exacts au chiffre près. Un durcissement qui produit son effet dès l'exécution suivante, c'est assez rare ici pour être noté
- **🔗 Pont** · [[2026-09-25_lecon-appli-ia_09_qualite-tests-debogage]]
  **`--experimental-strip-types` hier, `meta.totalDependencies` aujourd'hui** : deux fois la même faute, une signature d'API écrite de mémoire, et deux fois sur une page que la leçon cite en ressources. La règle 2 du parcours interdit exactement cela depuis le premier jour
- **🔗 Pont** · [[2026-09-26_lecon-placement-financier_16_transmission-succession-demembrement]]
  **le même jour, sur un autre parcours, l'autre moitié du même problème** : là-bas une leçon qui se contredit d'une section à l'autre, ici un runner qui se contredit d'une tentative à l'autre. Dans les deux cas le document contenait de quoi se corriger lui-même, et rien ne l'a lu
- **🗂️ Dossier** · `livrables/projets/appli-ia/PROJET.md` (hors vault Obsidian)
  **non mis à jour par cette exécution** — empreinte identique avant et après. C'est la mémoire que la leçon 11 lira, et elle ignore tout de la 10
