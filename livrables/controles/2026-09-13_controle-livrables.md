---
type: fiche-document
source: 2026-09-13_controle-livrables.docx
date_creation: 2026-09-13
date_controle: 2026-09-13
job: controle-livrables
statut: controle-hebdomadaire
tags:
  - controle/livrables
  - theme/controles-communs
  - theme/harnais-non-regression
  - theme/exit-3
  - theme/faux-positif
  - theme/perimetre-tacite
  - theme/valeur-decimale
  - alerte/a-corriger
---

# 2026-09-13_controle-livrables

Document source : [[2026-09-13_controle-livrables.docx]]

## Résumé

**Première note produite avec l'étape 4bis, relancée à la main à 16h17 après archivage de celle de 11h03 — et ce qu'elle recopie des contrôles communs est exact.** Quinze documents (onze leçons, quatre veilles), **113 URL déclarées, 113 testées** : j'ai refait la somme des sections URLS d'`extract_docx.py` sur les quinze, c'est 113 (la note de 11h03 disait 128 « avec doublons »). Les quatre décomptes de veille sont bien COHÉRENT — rejoués un par un. La section 🧪 Harnais reproduit mot pour mot ce que `non_regression.sh --complet` a écrit dans `en_cours/nr_complet.txt` à 16h19 : 223 documents · 0 bloquant, référence du 13/09 14:34, aucun verdict changé, 14/14, trois témoins à 0, le témoin d'avant correction à 1 avec « MAL ATTRIBUEE : All signs point to… », et la dernière ligne « ▶ Terminé — exit 0 » — le job a attendu la fin, comme le prompt l'exige, et a supprimé le fichier. Les calculs refaits sont justes : (1,028)⁸ = 1,2472 → 37 417 € ; 5,32 et 10,17 sur 97 € avec 0,93 ; seuil OVH Perso à 5 ventes au renouvellement. Mailchimp lu à 38 230 caractères, « correction déclarée » — la note ne répète pas le « rendu JavaScript » de ce matin. 🔴 : aucun, et c'est vrai — les deux défauts de ce matin (Mailchimp, Gurman) ont été corrigés à 12h et à 15h. Coût **1,63 $** (41 % du plafond), 48 tours, **16 min 34 s** ; le log de 11h03 affichait 1,56 $ : l'étape 4bis, harnais compris, coûte quelques centimes de plus et un quart d'heure de temps machine.

**Le défaut central : la note se contredit sur les « exit 3 », et se trompe dans les deux sens.** Le tableau écrit « exit 3 : psychologytoday » (ennéagramme 15), « exit 3 : 3 pages (403) » (dzogchen 15), « exit 3 : economie.gouv.fr » (revenus-passifs 07), « exit 3 : consilium » (ai-act 11/09), « exit 3 : apple.com » (imac 06/09 et 13/09) — six lignes — et le bilan chiffré écrit « Contrôle attributions (exit 0 / exit 3) : **15 / 0** ». J'ai rejoué le contrôle sur les cinq documents : **tous en exit 0**, zéro NON VERIFIABLE. Le job a lu la ligne « PAGES NON LUES (0 octet) » et l'a transcrite en « exit 3 » — or un 3 ne sort que si une *vérification* a été impossible (citation ou version sur une page non lue), pas quand une page listée est muette sans que rien n'en dépende. Conséquence : par la règle du prompt — *« un 🟢 n'est possible que si le contrôle des attributions est sorti en 0, pas en 3 »* — six 🟢 du tableau sont interdits par ce que le tableau lui-même affirme. Ils sont justes par chance, parce que le code réel était 0. La note ne peut pas être relue sans relancer le contrôle : c'est le contraire de ce qu'une note de contrôle doit permettre.

**Le point de vigilance ① est un faux positif du contrôle commun, et la note ne l'a pas attrapé alors que le prompt le lui demandait.** *« Prix Fnac (1 689 €) absent de la page consomac.fr aspirée … Non vérifiable mécaniquement »* — la page `consomac.fr/comparateur/mac/imac-m4`, ouverte ce soir avec le même agent, porte **« 1 689,00 € −6 % »** noir sur blanc. La passe D de `controle_attributions.py` cherche « 1 689 » avec une borne `(?![\d.,])` : la virgule de « 1 689,00 » fait échouer la recherche — toute valeur écrite en décimales françaises sur la page est déclarée absente (et le traitement des espaces insécables est du code mort : `re.escape` n'échappe plus l'espace depuis Python 3.7). Défaut ㉕, à corriger dans le contrôle. Mais le prompt était explicite : *« la passe D “A VERIFIER” — c'est TON contrôle B qui tranche, à la source primaire »*. Le job n'a pas ouvert la page ; il a écrit « comparateur temps réel, prix peuvent avoir évolué » — une hypothèse plausible, non testée, présentée comme un constat. Même famille que le « rendu JavaScript » de 11h03 : un « non vérifiable » écrit sans avoir vérifié.

**Un périmètre tacite, et deux imprécisions.** La commande `find … -mtime -7` du prompt renvoie ce soir **97 fichiers** — les 15 de la semaine, plus 82 documents anciens dont la date de modification est dans les sept jours parce qu'ils ont été *corrigés* cette semaine (SERAFIN d'avril à septembre, rgpd, rbpp, les trois leçons n°01…). La note en contrôle 15 et écrit « Livrables couverts : 11 leçons + 4 veilles = 15 » sans un mot sur les 82 autres. Le choix est le bon — le contrôle porte sur ce qui a été *produit* — mais la règle d'exhaustivité impose d'écrire ce qu'on écarte et pourquoi ; la note de 11h03 avait fait le même silence. Ensuite : *« iMac 13/09 — 5 citations Gurman appariées aux bonnes pages »* — le contrôle en a apparié trois (㉓) et simplement trouvé deux, et « M6 MacBook Pro and M6 iMacs Likely Coming in October » est un titre MacRumors, pas une parole de Gurman. Enfin, comme les quatre notes précédentes, celle-ci ne contient **aucune adresse** (0 URL, 0 lien) : le point ① nomme « consomac.fr/comparateur/mac/imac-m4 » en texte, rien n'est cliquable, alors que le style demandé prévoit des liens.

**Ce qui est à corriger, dans l'ordre.** ① Le contrôle : ㉕, la passe D accepte « 1 689,00 » pour « 1 689 » (décimales nulles) et les trois espaces (normale, insécable, fine) — à valider dans les deux sens sur le comparateur consomac et sur un témoin où la valeur est vraiment absente. ② Le prompt : « exit 3 » est le code de sortie de la commande, à lire sur `$?` ou sur la ligne VERDICT (« — et N vérification(s) IMPOSSIBLE(S) »), jamais déduit de « PAGES NON LUES » ; imposer de recopier le code littéral dans la colonne. ③ Le prompt : le périmètre = les documents dont la date *dans le nom* est dans la fenêtre, et la note dit combien `find` en a rendu et combien elle en écarte. ④ Le prompt : une valeur « A VERIFIER » en D se tranche en ouvrant la page avec l'agent de navigateur — écrire « non vérifiable » sans l'avoir ouverte est interdit. La note elle-même ne se corrige pas : c'est la règle absolue du job, et la note suivante (20/09) dira si le prompt tient.

## Notes liées

- **⬅️ Précédente** · [[2026-09-13_controle-livrables_11h03-avant-4bis]]
  la note du matin, archivée : 🟢 sur la veille iMac et sur revenus-passifs 08 alors que l'une portait deux citations mal attribuées et que l'autre avait été refusée au push à 7h03. Celle du soir n'a plus ces deux défauts — parce qu'ils ont été corrigés entre-temps, pas parce qu'elle les aurait vus : la preuve est dans son propre témoin d'avant correction, en exit 1
- **🔗 Pont** · [[2026-09-13_veille_imac.fiche]]
  le document qui a fait naître ㉓ et l'étape 4bis ; la note le déclare « 5 citations appariées » (trois, en réalité) et lui prête un « exit 3 » qui n'existe pas
- **🔗 Pont** · [[2026-09-13_lecon-revenus-passifs_08_outils-creation-hebergement-paiement]]
  Mailchimp « 38 230 car. utiles (correction déclarée) » : la note a lu la ligne d'aspiration au lieu d'affirmer « rendu JavaScript » — c'est le seul endroit où l'on voit l'étape 4bis changer le jugement du contrôleur
- **🔗 Pont** · [[2026-09-11_veille_ai-act.fiche]]
  la règle 10 d'ai-act (un constat fait avec le même outil se répète, il ne se confirme pas) s'applique au contrôleur lui-même : « prix peuvent avoir évolué » et « rendu JavaScript » sont deux façons de ne pas ouvrir la page
