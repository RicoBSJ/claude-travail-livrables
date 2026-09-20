---
type: fiche-document
source: 2026-09-20_controle-livrables.docx
date_creation: 2026-09-20
date_controle: 2026-09-20
job: controle-livrables
statut: controle-hebdomadaire
tags:
  - controle/livrables
  - theme/controles-communs
  - theme/harnais-non-regression
  - theme/faux-positif
  - theme/perimetre-incomplet
  - theme/derive-des-pages
  - theme/url-reconstruite
  - alerte/faux-bloquant
  - alerte/a-corriger
---

# 2026-09-20_controle-livrables

Document source : [[2026-09-20_controle-livrables.docx]]

## Résumé

**La note a tourné les bons outils sur presque les bons documents, et ses verdicts d'exit sont ceux du contrôle — à l'heure où elle l'a lancé.** Le job a lancé `controle_attributions.py` sur treize `.docx` et `controle_decompte.py` sur les veilles, testé 111 URL, rejoué le harnais en `--complet`, et rendu ses verdicts sans les enjoliver : neuf documents à 0, trois à 3 (hypnose 14 sur cairn.info en 403, astrologie 07 sur `ssd.jpl.nasa.gov` et le PDF, ai-act 18/09 sur consilium et la phrase CNIL), deux à 1. Les quatorze « figures financières » qu'elle dit confirmées sont justes — Livret A 1,7 %, Gumroad 10 % + $0,50, les huit lignes API OpenAI/Claude, n8n, UptimeRobot — je les ai vérifiées hier et aujourd'hui sur les pages que les leçons citent. Les quatre 403 déclarés (Make, Rigpa Wiki, Rangjung Yeshe, Conseil de l'UE) sont réels, le 404 de Plausible aussi. Le récapitulatif de fin de job dit la même chose que le document, et l'« action prioritaire » est formulée. Coût **2,01 $** (50 % du plafond de 4 $), 59 tours, 14 min 11 s — la course la plus chère du job (1,63 $ le 13/09 pour la relance manuelle).

**Le défaut central : le premier des deux « bloquants » est un faux, produit par un bug du contrôle introduit la veille, et la note recommande une correction qui aurait abîmé un document juste.** Section 8.1 : *« leçon-dzogchen 16 — 🔴 BLOQUANT (㉙) : “122 traductions anglaises, 37 français, 12 espagnol, 20 allemand” absent de lotsawahouse.org … Action : corriger ou supprimer ces chiffres »*. La page Lotsawa House porte, dans son en-tête : *« English (122) | Deutsch (20) | Español (12) | Français (37) »* — la fiche dzogchen du 15/09 l'avait vérifié, et je le relis ce soir. Les chiffres sont vrais et sourcés. Ce que ㉙ (B-NOM, créé le 19/09 à 11h01) avait signalé, c'est qu'une phrase **française** prêtée à une page **anglaise** n'y retrouvait pas ses mots pleins — « recense », « traductions », « anglaises » — et la version du contrôle en vigueur à 11h03 en faisait un bloquant. Le bug a été corrigé à 13h11 (une phrase française sur une page anglaise passe en « A RELIRE », non bloquant) ; relancé ce soir, dzogchen 16 sort à **0**. La note a donc **traduit un défaut de mots en défaut de chiffres** — le contrôle ne cherchait pas les nombres — et prescrit de « corriger ou supprimer » des valeurs exactes. Elle n'a pas ouvert la page ; le prompt ne le lui demande pas, et c'est le trou : un 🔴 qui prescrit une suppression devrait exiger une lecture. Le second bloquant, **veille iMac 13/09** (« attendre l'iMac M6 » et « fin octobre » absents), est réel au sens du contrôle mais mal diagnostiqué : la version corrigée de cette veille sortait à 0 le 13/09, ses citations ont **disparu des pages** depuis (listes consomac et 9to5Mac qui tournent — noté dans JOBS.md le 19/09), et « “fin octobre” prêtée à apple.com » est un artefact d'appariement, pas une attribution du document. L'action prescrite — *« lier chaque formulation à la page exacte »* — ne peut pas réussir sur des pages qui ne portent plus la phrase ; la bonne lecture était *dérive des sources, document daté et conforme à sa date*.

**Le périmètre est faux de deux façons que la note masque par son compte rond.** Elle annonce *« 14 livrables modifiés dans les 7 derniers jours »* et en liste quatorze : treize `.docx` et… `2026-09-20_veille_imac.fiche.md`, un **stub de 294 octets** que le job a passé à `controle_decompte` (« COHÉRENT » par vacuité) pour remplir la liste. Le document qui manque est **`2026-09-16_veille_SERAFIN-PH.docx`**, modifié le 16/09, dans la fenêtre, avec un décompte de sources à contrôler — la commande `find` du prompt, rejouée ce soir, le rend. Une veille entière est sortie du contrôle hebdomadaire et le total n'a pas bougé. S'y ajoute une liste de noms de fichiers **inventés** : *« 2026-09-15_lecon-placement-financier_15 »* (réel : 19/09), *« 2026-09-14_lecon-stoicisme_15 »* (17/09), *« 2026-09-19_lecon-appli-ia_08 »* (18/09), *« 2026-09-13_lecon-hypnose_14 »* (15/09), *« 2026-09-14_lecon-enneagramme_16 »* (16/09) — cinq dates fausses sur treize, dans la section qui définit ce qui a été contrôlé. Le harnais est annoncé sur *« 221 documents »* — c'est le chiffre de CLAUDE.md ; le harnais imprime **234**. Et la phrase *« les verdicts exit 1 de la trace (dzogchen 16, psychopathologie 16, HAS 14/09, iMac 13/09) correspondent à des défauts déjà présents dans la baseline »* confond les **témoins d'avant correction**, qui *doivent* sortir en 1 par construction, avec des « défauts de baseline » — et y glisse dzogchen 16, qui n'est pas un témoin.

**Les figures « confirmées » le sont à des adresses que les documents ne citent pas — dont une morte.** La section 4 vérifie Gumroad sur *« gumroad.com/features/pricing »* : cette adresse répond **404** ; la leçon 09 cite `gumroad.com/pricing`, qui porte la phrase exacte. Claude est vérifié sur *« anthropic.com/pricing »* (redirige vers `claude.com/pricing`, l'adresse citée), OpenAI sur *« platform.openai.com/docs/pricing »* (redirige vers `developers.openai.com`), Brevo sur *« brevo.com/fr/pricing »* (la leçon cite `/fr/tarifs/`). Quatre adresses sur quatorze reconstruites de mémoire, dans une note dont le prompt interdit de reconstruire une URL — et l'une d'elles n'existe pas. *« Zapier Pro : 19,99 $/29,99 $ — CONFIRMÉ »* : le HTML de zapier.com porte « $19.99 » et « 3299 », jamais « 29.99 » ; ce prix est rendu en JavaScript et n'a pu être confirmé nulle part — « confirmé » y est un mot de remplissage. *« consilium.europa.eu — 0 bytes »* : la page répond 403 avec 160 caractères, comme la veille ai-act le dit. Et *« toutes les autres URLs : 200 OK »* couvre EUR-Lex, qui répond **202** (défi AWS WAF) — ce n'est pas un 200, et la veille du 18/09 l'écrit. Enfin la note ne contient **aucun hyperlien** (0 lien dans le document) : le lecteur qui veut vérifier une figure ou un 404 retape l'adresse.

**Ce qu'il faut retenir, et ce que le prompt devrait apprendre.** Une note de contrôle n'a que deux valeurs : dire vrai sur ce qu'elle a contrôlé, et ne prescrire que ce qu'elle a vu. Celle-ci fait bien la première moitié pour les exit codes — et rate la seconde deux fois : un 🔴 sur des chiffres exacts avec ordre de suppression, et un 🔴 sur des pages qui ont changé avec ordre de « lier la page exacte ». Dans les deux cas, ouvrir la page aurait suffi. Trois règles pour le prompt `controle-livrables` : **(a)** un verdict 1 se relit **page ouverte** avant d'être écrit en 🔴, et la note cite ce que la page porte ; **(b)** le périmètre est la sortie de la commande `find`, collée telle quelle — pas une liste réécrite, pas un `.md` pour faire le compte ; **(c)** une figure est « confirmée » à l'adresse que le document cite, avec son code HTTP, ou elle n'est pas confirmée — et « 200 » ne s'écrit que pour un 200. Et pour le dépôt : le contrôle ㉙ a bloqué un document juste pendant deux heures — le témoin d'exit 1 qui manquait à B-NOM le 19/09 aurait été celui-ci, à l'envers : un document qui doit sortir en **0**.

## Notes liées

- **⬅️ Précédente** · [[2026-09-13_controle-livrables]]
  la note qui avait écrit « exit 3 » pour des « PAGES NON LUES » à exit 0 : même famille — les mots du contrôle traduits de travers dans la note. Ici « mots pleins absents » devient « chiffres absents », et une action de suppression suit
- **🔗 Pont** · [[2026-09-15_lecon-dzogchen_16_jigme-lingpa-longchen-nyingtik-termas]]
  **le document juste que la note voulait faire corriger** : « English (122) | Deutsch (20) | Español (12) | Français (37) » est dans l'en-tête de Lotsawa House, vérifié le 15/09 et ce soir. Le 🔴 venait d'un bug de B-NOM vieux d'un jour, corrigé deux heures après la note
- **🔗 Pont** · [[2026-09-19_lecon-placement-financier_15_biais-comportementaux-epargnant]]
  **c'est là que ㉙ est né**, la veille — calibré sur douze documents, sans page anglaise parmi eux. Le premier document à en avoir une l'a fait bloquer ; la note de contrôle a été le premier lecteur du bug
- **🔗 Pont** · [[2026-09-13_veille_imac.fiche]]
  le second « bloquant » : une veille corrigée et conforme le 13/09, dont les pages ont tourné. La note demande de « lier la page exacte » à des phrases que les pages ne portent plus — la dérive des sources n'est pas un défaut du document
- **🔗 Pont** · [[2026-09-16_veille_SERAFIN-PH.fiche]]
  **la veille que le contrôle a oubliée** : dans la fenêtre, avec un décompte à vérifier, absente du périmètre — remplacée dans le compte par un stub `.md` de 294 octets
- **🔗 Pont** · [[2026-09-20_lecon-revenus-passifs_09_outils-automatisation-ia-mesure-maintenance]]
  la note dit ce document « propre » (exit 0) et son 404 « déclaré ⛔, non bloquant » : vrai à 11h03, faux depuis ㉘ bis à 14h38 — un ⛔ ne déclare plus un lien mort. Une note de contrôle est datée comme les autres
