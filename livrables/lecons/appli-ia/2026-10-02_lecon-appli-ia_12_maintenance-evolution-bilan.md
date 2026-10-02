---
type: fiche-document
source: 2026-10-02_lecon-appli-ia_12_maintenance-evolution-bilan.docx
date_creation: 2026-10-02
date_lecon: 2026-10-02
parcours: appli-ia
numero: 12
statut: parcours-clos
tags:
  - parcours/appli-ia
  - registre/perso
  - module/maintenance
  - outil/npm
  - outil/node
  - outil/vite
  - outil/react
  - concept/semver
  - concept/dette-technique
  - concept/spawnsync-vs-execsync
  - concept/wanted-vs-latest
  - concept/bilan-de-sante
  - source/docs-npmjs
  - source/semver-org
  - source/nodejs-releases
  - theme/sortie-reproduite-a-l-identique
  - theme/commande-qui-n-existe-pas
  - theme/motif-inerte
  - alerte/a-corriger
  - jalon/fin-de-parcours
---

# 2026-10-02_lecon-appli-ia_12_maintenance-evolution-bilan

Document source : [[2026-10-02_lecon-appli-ia_12_maintenance-evolution-bilan.docx]]

## Résumé

**Tout ce que cette leçon annonce, je l'ai exécuté, et tout tient — c'est la leçon la mieux mesurée que j'aie relue cette semaine, tous parcours confondus.** Les **six numéros de version** sont justes, vérifiés un par un contre le registre npm le 02/10/2026 : `@types/node` **26.6.4**, `react` et `react-dom` **19.3.0**, `@types/react` et `@types/react-dom` **19.3.0**, `vite` **8.3.2** — et ce sont exactement les versions **installées** dans `node_modules` et `frontend/node_modules`. `scripts/maintenance.js` fait **144 lignes**, les 144 annoncées (« compté le 02/10/2026 »). Et surtout : **`npm run maintenance` reproduit mot pour mot le bloc de sortie attendue publié dans la leçon** — « ✓ 33 tests · 0 échec(s) », « ✓ 5/5 contrôles passés », « ✓ Toutes les dépendances sont à jour », « ✓ Sauvegarde du jour », « Bilan : 4 OK · 0 point(s) à traiter », « Le portail est en bonne santé. », exit 0. `cd frontend && npm run typecheck` rend **exit 0 sans un message**, comme annoncé. Et le bloc d'erreur de l'exercice 4 **se reproduit à l'identique** : dans un répertoire de test neuf avec `"@types/node": "^999.0.0"`, npm 11.16.0 imprime bien `npm error code ETARGET` puis `npm error notarget No matching version found for @types/node@^999.0.0.` — seul le retour à la ligne de la dernière phrase diffère. Les trois pages de `docs.npmjs.com` confirment ce que la leçon leur fait dire : les colonnes **Current / Wanted / Latest** de `npm outdated` et la sémantique des couleurs — *« Yellow indicates that there's a newer version above your semver requirements (usually new major…) so proceed with caution »* —, que la leçon rend correctement par « si latest dépasse wanted (colonne jaune), tu as une MAJOR disponible ». **Et un geste que peu de leçons font : distinguer le manifeste du verrou.** L'exercice 2 écrit *« Le fichier package.json du frontend n'a pas été modifié depuis la leçon 11 : vite est à 8.2.2, react à 19.2.8 »* — c'est exact, `frontend/package.json` déclare toujours `^19.2.8` et `^8.2.2`, parce que 19.3.0 et 8.3.2 tombent **dans** ces plages et que `npm update` n'a donc aucune raison de les réécrire. Une leçon sur les dépendances qui ne confond pas ce qui est installé avec ce qui est déclaré.

**Le Challenge envoie le lecteur vers une commande qui n'existe pas.** Il demande d'ajouter un cinquième contrôle à `maintenance.js` et précise : *« Utilise `lancer()` pour appeler `npm build` — le script build est défini dans package.json. »* Or `npm build` **n'est pas une commande npm** : npm 11.16.0 répond `Unknown command: "build"` et suggère de lui-même `npm run build # run the "build" package script`. La seconde moitié de la phrase est juste — le script `build` existe bien, il appelle `tsc`, et `npm run build` rend exit 0 — mais un lecteur qui suit la consigne à la lettre écrit `lancer('npm', ['build'])` et obtient un contrôle n°5 **qui échoue toujours**, dans un script dont le rôle est précisément de dire si le projet va bien. **Et aucun des treize motifs de l'étape 5 bis ne pouvait le voir** : le motif (o), écrit le 26/09 pour vérifier qu'« un outil nommé comme remède est installé », trouve `npm` installé et s'arrête là ; rien ne vérifie qu'une **forme de commande** existe. C'est un angle mort d'un genre nouveau pour ce parcours — jusqu'ici les défauts portaient sur des versions, des sorties ou des extraits de fichiers, jamais sur l'existence d'un verbe.

**Un écart d'un seul caractère entre la sortie annoncée et la sortie réelle — et c'est la règle 1 du parcours qu'il touche.** Le bloc « Sortie attendue de `npm run maintenance` après la mise à jour (mesurée le 02/10/2026) » écrit « ✓ **33 test(s)** · 0 échec(s) ». Le script, lui, imprime « ✓ **33 tests** · 0 échec(s) » — son gabarit est `${passeTotal} tests · ${echecTotal} échec(s)`, sans parenthèses. Tout le reste du bloc est exact au caractère, y compris la barre de séparation et les deux lignes de bilan. Le défaut est minuscule et il est symptomatique : dans un parcours dont la première règle est **« une sortie se reproduit »**, et dans la seule leçon du parcours consacrée à vérifier que tout va bien, le bloc de sortie a été **recopié à la main plutôt que collé**. Deux écarts mineurs du même ordre : la dernière phrase du message ETARGET est coupée en deux lignes dans la leçon et en une seule dans la réalité ; et le récapitulatif du **journal du job** annonce « frontend/ — react/react-dom 19.2.8 → 19.3.0, vite 8.2.2 → 8.3.2 » sans dire qu'il parle du verrou et non du manifeste — le document, lui, le dit. Le journal n'est pas le livrable, mais c'est lui qu'on relit en premier.

**Inertie mesurée de l'étape 5 bis : cinq motifs sur treize n'avaient rien à examiner.** Script ré-extrait verbatim du prompt et rejoué sous `env -i` depuis la racine du projet : **OK — XML conforme · 4 tableaux · 5 liens · 27 puces, 0 vide**, et les onze verdicts de queue au vert. Mais la matière : **(e)** une seule observation prescrite · **(f)** deux comportements négatifs prêtés à un outil · **(l)** deux énoncés « N lignes » avec leur fichier — et c'est celui-là qui a travaillé pour de bon, puisque `wc -l` confirme les 144 · **(i)** trois blocs de code portant un `require`/`import` · **(n)** 155 blocs de code examinés. **Et zéro matière pour (g)** (messages d'exécution), **(h)** (drapeaux `--experimental`), **(j)** (titres de section prêtés à une page), **(k)** (message d'exécution prêté au compilateur) et **(m)** (lignes « # Attend : »). Les cinq sont inertes sur ce document : ils ont été écrits les 18/09, 25/09 et 26/09 contre des défauts de la leçon n°06, et une leçon sur `npm outdated` ne leur donne rien à mordre. 350 paragraphes sur 350 examinés — le journal de corrections est bien hors champ puisqu'il n'y en a pas. Côté contrôles communs : `controle_attributions` rend **0 bloquant** avec **trois passes inertes** (B, B-NOM, D) et un inventaire C de 14 numéros de version dont il reconnaît lui-même les « mesures locales annoncées » comme légitimes ; `controle_decompte` répond **« LISTE NON RECONNUE »**, comme sur tout ce parcours. **Ce que j'ai trouvé ici, aucun contrôle du dépôt ne pouvait le trouver — il a fallu lancer le script.**

**La leçon la plus chère du dépôt, et la dernière du parcours : 12 sur 12, du 02/08 au 02/10/2026.** **4,3574 $ pour un plafond de 5,00 $ (87 %)**, **102 tours**, 21 min 38 s, 68 729 tokens en sortie, 8 258 340 de cache lu, une seule tentative — avec le prompt le plus lourd des quatorze jobs, **118 352 octets**. À comparer aux 53 tours de l'astrologie et aux 37 du stoïcisme le même jeudi. **Et c'est le contre-exemple à mon propre contre-exemple** : j'ai écrit deux fois cette semaine que « plus de tours ne veut pas dire plus sûr » ; ici le prompt le plus long et le run le plus cher ont produit la leçon la mieux mesurée de la semaine, dont j'ai pu reproduire par exécution **chaque** chiffre et **chaque** bloc de sortie sauf un « s ». Le ratio annoncé 20/80 est mesuré à **23,5 % de théorie** (objectif, théorie, section IA) contre **72,5 % de pratique** (pratique, vérification, challenge) et 3,3 % de ressources — le plus proche de sa cible des cinq parcours de la semaine, et la section « Pratique » pèse à elle seule **49,8 %** du texte. `PROJET.md` est à jour et complet : les douze lignes de « Reste à faire » sont soldées, tous les « Points en suspens » sont fermés, et la contradiction que je relevais le 27/09 sur `/api/db/search` est résolue — la route reste sur `nom LIKE`, c'est écrit, daté et déclaré hors périmètre, ce qui est une fin honnête plutôt qu'un report de plus. La ressource « Git — Tagging » que je signalais listée deux fois et jamais utilisée **ne figure plus** dans le journal de projet. Il reste une dette assumée, nommée dans la leçon elle-même : la **dette invisible**, « les comportements attendus non testés, les messages d'erreur recopiés de mémoire » — et le « s » manquant de ce matin en est le dernier spécimen.

## Notes liées

- **⬅️ Précédente** · [[2026-09-27_lecon-appli-ia_11_mise-en-production-build]]
  elle servait le build React depuis Node.js et soldait trois reports anciens ; **elle annonçait aussi « PROJET.md n'a plus qu'une ligne dans Reste à faire »**, et cette ligne est maintenant barrée. La 11 avait un plafond de mise à jour de `PROJET.md` outrepassé ; la 12 l'a respecté — **+25 / −4 lignes**, très en dessous du seuil de 40
- **➡️ Suivante** · *aucune : parcours fermé de 12 leçons, terminé le 02/10/2026*. Le créneau du vendredi 8h03 reste occupé par `appli-ia-lecon` dans `jobs_config.json` — à décider : suppression du job, ou nouveau parcours sur le même créneau
- **🔗 Pont** · [[2026-09-26_lecon-appli-ia_10_securite-donnees]]
  **la leçon qui a tout mesuré et rien retenu**, et dont sont nés cinq des treize motifs de l'étape 5 bis. Deux semaines plus tard, cinq de ces motifs n'ont plus rien à mordre : ils ont été écrits contre des défauts de la n°06 et de la n°10, et une leçon sur `npm outdated` ne leur donne pas de matière. **Un contrôle efficace finit par devenir inerte — ce n'est pas un échec, c'est son cycle de vie**
- **🔗 Pont** · [[2026-09-24_lecon-astrologie-karmique_08_retrogradations-mouvement-apparent-lecture]]
  **corrigée le même matin, et l'exact opposé** : là-bas onze corrections sur un document dont un pourcentage était lu à l'envers depuis huit jours, trouvées à la main parce qu'aucun motif ne savait les voir. Ici tout est juste, et le seul défaut de fond — une commande qui n'existe pas — est aussi hors de portée des motifs. **Dans les deux cas le contrôle a dit OK ; dans un cas il avait raison**
- **🔗 Pont** · [[2026-10-01_lecon-stoicisme_17_stoicisme-christianisme-emprunts-divergences-posterite]]
  le défaut inverse sur la vérifiabilité : la stoïcisme 17 ne citait **rien**, ce qui la mettait hors de portée des passes qui vérifient les citations. La appli-ia 12 cite tout et **tout est exécutable** — c'est le seul parcours du dépôt où une affirmation peut être réfutée en tapant une commande, et c'est pour cela que sa relecture trouve des défauts que les autres ne peuvent pas produire
- **🗂️ Dossier** · `livrables/projets/appli-ia/` (hors vault Obsidian) — `PROJET.md` 30 410 octets, `scripts/maintenance.js` 144 lignes, `package.json` **v1.1.0**, frontend **v0.6.0**. Parcours **12 / 12**, du 02/08 au 02/10/2026. Les 16 leçons NO-CODE + IA qui précédaient ce parcours restent dans `livrables/lecons/nocode-ia/`
