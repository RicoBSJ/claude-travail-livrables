---
type: fiche-document
source: 2026-10-17_veille_ai-act.docx
date_creation: 2026-10-17
date_veille: 2026-10-17
veille: ai-act
statut: veille-active
tags:
  - veille/ai-act
  - registre/pro
  - theme/semaine-creuse
  - theme/echeance-2-decembre-2026
  - theme/ddadue
  - source/commission
  - source/eur-lex
  - source/cnil
  - source/iapp
  - declenchement/manuel
  - audit/standard
---

# 2026-10-17_veille_ai-act

Document source : [[2026-10-17_veille_ai-act.docx]]

## Résumé

**Édition hors créneau, lancée à la main pour éprouver quatre correctifs avant le créneau du vendredi — et c'est le générateur qui a failli publier une note vide.** Le job tourne normalement le vendredi 9h03 ; celui-ci a été déclenché le samedi 17/10, un jour après l'édition du 16/10, précisément pour voir à l'œuvre les bornes de bloc de l'étape 5 bis, l'exemption ⑩, ㊲ et ㊴. Résultat du fond : **🟢 compte-rendu allégé, 0 fait marquant**, ce qui était l'issue attendue — une fenêtre de sept jours qui recouvre six jours déjà couverts ne peut presque rien apporter, et la note le dit en propres termes plutôt que de meubler.

🔴 **LE DÉFAUT LE PLUS INSTRUCTIF EST QUE LE CONTRÔLE D'INTÉGRITÉ DU PROMPT A DIT « OK » SUR UNE NOTE DONT 85 % DU TEXTE MANQUAIT.** Le prompt du job prescrit de construire chaque paragraphe avec `run: new TextRun({...})`. Avec la version de `docx` installée dans `en_cours/`, **cette propriété est silencieusement ignorée** : la première génération a produit un `.docx` de 11,4 Ko, **XML valide**, portant ses **10 hyperliens** — et ne contenant que **2 088 caractères de texte**, c'est-à-dire les seules lignes de liens. Titre, niveau d'alerte, fenêtre, rectifications, échéances, corps entier : disparus. ⚠️ **Le contrôle obligatoire que le prompt impose a répondu `OK — XML conforme, 10 lien(s)`** : il vérifie la conformité XML, les balises mal formées et le nombre de liens, **jamais le volume de texte**. C'est mot pour mot le « cas réel du mois d'août » que le prompt cite en exemple — une leçon dont trois tableaux avaient disparu —, et son propre garde-fou ne l'attrape pas. Corrigé en `children: [...]` : 2 088 → **7 438 caractères**.

**L'étape 5 bis m'a refusé deux fois, et elle avait raison les deux fois.** ① J'avais écrit en prose l'ancienne adresse EUR-Lex en forme `legal-content / CELEX`, pour dire que l'édition du 16/10 l'avait déclarée non lue : le contrôle commun l'a lue comme **une page citée dans le corps et absente des Ressources** — un bloquant. C'est la règle ③ du 12/10/2026, *un correcteur écrit dans la même langue que les motifs*, et l'adresse n'est désormais plus reproduite. ② Trois dates du règlement modificatif étaient **entre guillemets** alors que les pages EUR-Lex qui les portent **n'avaient pas été lues par le contrôle** : il a refusé trois « citations courtes absentes des pages de la note » en nommant les pages non lues. Reformulées en style indirect — c'est la règle du dépôt sur les pages intermittentes. ③ Et le motif (8) a attrapé une formulation négligente : ma phrase « reste non vérifiée » voisinait l'identifiant 2026/1744, que la page de la Commission porte bel et bien ; la réserve a été rattachée à la **date de publication**, qui est ce qui n'est pas confirmé.

🟢 **ET UNE TROUVAILLE UTILE À TOUTE LA SÉRIE : LA FORME ELI D'EUR-LEX EST LISIBLE.** L'édition du 16/10 listait le règlement sous la forme `legal-content / CELEX` et l'a déclarée non lue — **0 octet, HTTP 202**, ce qui était exact pour cette adresse. La forme **ELI** rend **609 895 octets bruts et 154 851 caractères utiles**, mesurés sur **quatre lectures consécutives** pendant cette exécution. Le garde-fou 11, qui exige que chaque édition porte le lien de ses références héritées, peut donc enfin être tenu sur une source primaire **réellement lue**. ⚠️ **Avec sa réserve, et elle est importante** : le contrôle d'attributions, qui récupère en rafale toutes les adresses de la note, a reçu **HTTP 202 et 0 octet** sur ces deux mêmes adresses quelques minutes plus tard. EUR-Lex **freine les rafales** ; ses pages ne sont pas mortes, mais un outil qui enchaîne les requêtes ne peut pas les relire. **Les dates sont donc vérifiées par lecture directe, pas par le contrôle automatique**, et la note l'écrit.

**Trois dates sur quatre sont confirmées à la source primaire, et la quatrième ne l'est pas.** Dans le texte du règlement (UE) 2026/1744 lu directement : la date de l'acte, **8 juillet 2026**, et celle de l'entrée en vigueur, **27 juillet 2026**, y figurent ; l'échéance du **2 décembre 2026** aussi. ⚠️ **La date du 24 juillet 2026 — celle que la série donne pour la publication au Journal officiel depuis le 29/08/2026 — n'a pas été retrouvée dans cette page.** Et la Q/R de la CNIL la présente comme la date d'**adoption**, ce qui confond publication et acte : c'est exactement l'écart que le garde-fou 11 demande de signaler et que l'édition du 11/09 avait laissé passer. La note tranche : le 8 juillet pour l'acte, le 27 juillet pour l'entrée en vigueur, **la publication au JOUE non confirmée sur cette page**.

**Le constat de fond, source par source, et il est honnête.** Fenêtre du 10 au 17 octobre. La liste « Latest News » de la Commission, relue **dans l'ordre**, donne 14/10 (compétences numériques) et 13/10 (cybersécurité UE-Ukraine) — **hors périmètre AI Act** —, puis 05/10 (panel scientifique), hors fenêtre et déjà couvert le 16/10. L'IAPP rend **vingt titres datés** : ses items du 14 et du 15/10 étaient déjà repris le 16/10, et ses deux entrées du 16/10 portent sur le Canada et sur des audits de conformité américains. `artificialintelligenceact.eu`, lue avec un agent de navigateur à **16 210 caractères** — la mesure même que le prompt documente —, n'a rien dans la fenêtre : son billet le plus récent est du 14 mai 2026. La CNIL s'arrête au 26 août 2026. Le Conseil de l'UE répond **403** après trois essais, et un repli par recherche sur son domaine **ne trouve aucun communiqué relatif au règlement sur l'IA en octobre 2026** — ce qui confirme indépendamment ce qu'écrivait l'édition du 16/10.

**Les quatre correctifs de la veille se sont exercés, et trois ont mordu.** L'**exemption ⑩** a signalé `iapp.org/news/` comme page d'index dont la taille n'est pas une propriété du document — deuxième validation en production, sur une édition fraîche. **㊲** a écarté une valeur d'instrumentation de la passe D en la nommant. **㊴** n'a laissé passer aucune URL fantôme là où la note cite neuf adresses en prose. Le **plafond relevé à 5 $** n'a pas été sollicité : un lancement manuel ne passe pas par `run_job.sh`. ⚠️ **Et ㊳ est resté muet pour la bonne raison technique mais pas pour la bonne raison de fond** : il relie un document au log de son run par la date et l'identifiant du job ; **un lancement manuel ne produit aucun log**, donc il n'a rien à examiner. Un livrable produit à la main lui est invisible.

### Requêtes passées pour cet audit

| requête | degré obtenu | source |
|---|---|---|
| `8 July 2026` · `27 July 2026` · `2 December 2026` | **① littéral** | EUR-Lex ELI, règlement 2026/1744 |
| `24 July 2026` | **④ absent** de la page du règlement | idem |
| `2026/1744` · `2024/1689` | **① littéral** | idem |
| `L_202601744` (forme JOUE) | ④ absent | idem |
| 8 adresses citées | 7 en **HTTP 200**, Consilium en **403** | vérification `curl` avant publication |
| EUR-Lex ELI, 4 lectures consécutives | **200 · 609 895 octets** chaque fois | mesure d'intermittence |

**Non interrogé** : le corps des articles IAPP marqués MEMBER, non lisibles par construction ; le dossier législatif du DDADUE, `legifrance.gouv.fr` requérant JavaScript — la note l'écrit « non vérifié à une source primaire pendant cette exécution », ce qu'exige le motif (5).

## Notes liées

- **⬅️ Précédente** · [[2026-10-16_veille_ai-act.fiche]]

- **➡️ Suivante** · vendredi **23/10/2026** à 9h03, créneau normal, **plafond désormais à 5,00 $** après le dépassement du 16/10 (3,2339 $ pour 3,00 $). ⚠️ **Cette édition-ci devient son « édition précédente »** pour `controle_edition_precedente.py` : une édition hors créneau décale la chaîne de relecture, et la série compte deux éditions pour la semaine du 13 au 19 octobre. 📌 **Et le générateur du vendredi reproduira le défaut `run:`** si le prompt n'est pas corrigé : c'est le point à traiter avant le créneau

- **🔗 Pont** · [[2026-10-16_veille_ai-act.fiche]] — l'édition qu'on vient d'éprouver : job mort sur son plafond, zéro contrôle lancé, quatre refus dont **trois artefacts** de délimitation de bloc. Les deux correctifs posés alors sont ici validés sur une édition neuve

- **🔗 Pont** · [[2026-10-17_lecon-placement-financier_19_allocation-coherente-tenir-duree]] — produite le même jour, et le contraste de méthode est net : là un run automatique à 45 % de son plafond sans une réserve, ici un run manuel dont le générateur a failli publier une coquille vide que le contrôle d'intégrité validait

- **🗂️ Dossier** · série **ai-act**, édition **hors créneau** du 17/10/2026. 🟢 **Semaine creuse assumée** : 0 fait marquant, compte-rendu allégé, et c'est l'issue correcte pour une fenêtre recouvrant à six jours près celle de la veille. 📌 **DEUX PISTES, et la première est urgente avant vendredi** : ① **corriger le prompt du job**, qui prescrit `run: new TextRun({...})` — propriété ignorée par la version de `docx` installée, qui produit un document valide, lié et **vide** ; et ② **élargir le contrôle d'intégrité** du prompt au **volume de texte**, puisqu'il a validé une note à 2 088 caractères. 📌 Troisième piste, moins pressante : **faire lire la forme ELI à la série** plutôt que la forme `legal-content / CELEX`, qui rend 0 octet. ⚠️ **À ne pas perdre** : la réserve d'intermittence sur EUR-Lex, et le fait que la publication au JOUE du 24 juillet n'est **pas** confirmée par la page du règlement.
