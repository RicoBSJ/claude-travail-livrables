---
type: fiche-document
source: 2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran.docx
date_creation: 2026-08-14
date_lecon: 2026-08-07
parcours: appli-ia
numero: 2
statut: parcours-actif
tags:
  - parcours/appli-ia
  - registre/mixte
  - module/fondamental
  - techno/html-css-js
  - techno/node-http
  - notion/requete-reponse
  - notion/path-traversal
---

# 2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran

Document source : [[2026-08-07_lecon-appli-ia_02_socle-web-premier-ecran.docx]]

## Résumé

Le socle web : rôles respectifs de HTML, CSS et JavaScript, boucle requête-réponse, et lecture d'un serveur HTTP Node.js **sans aucune bibliothèque externe** — choix délibéré, Express n'arrivant qu'en leçon 08 pour qu'on comprenne d'abord la couche native.

La pédagogie repose sur quatre gestes appliqués à du code déjà déposé sur le disque : **lire, prédire, modifier, casser**. On ne recopie rien.

La section sur les pièges de l'IA vaut d'être retenue au-delà du parcours : oubli du garde-fou contre le *path traversal*, chemins construits par concaténation, et lecture bloquante (`readFileSync`) dans un gestionnaire de requête — qui fige le serveur pour tous.

Cette leçon a été relue trois fois et porte un **journal des corrections en fin de document**, dont une erreur de fond : elle affirmait à tort qu'un chemin avec barre oblique casse sous Windows.

## Notes liées

- **⬅️ Précédente** · [[2026-08-02_lecon-appli-ia_01_cadrage-specification]]
  dont la spécification est ici mise à l'épreuve du code
- **➡️ Suivante** · [[2026-08-14_lecon-appli-ia_03_typescript-structure-projet]]
  qui type le code écrit ici, et résout l'écart n°4 laissé ouvert
- **🔗 Pont** · [[2026-04-10_lecon01_fondamentaux]]
  même famille d'outils vue deux ans plus tôt sous l'angle de l'usage ; ici sous celui de la production de code
