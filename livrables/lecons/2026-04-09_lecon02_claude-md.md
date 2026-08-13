---
type: fiche-document
source: 2026-04-09_lecon02_claude-md.docx
date_creation: 2026-08-14
date_lecon: 2026-04-09
parcours: claude-code
numero: 0
statut: parcours-archive
tags:
  - parcours/claude-code
  - registre/mixte
  - outil/claude-md
  - notion/memoire-persistante
  - notion/scopes
---

# 2026-04-09_lecon02_claude-md

Document source : [[2026-04-09_lecon02_claude-md.docx]]

## Résumé

La leçon la plus structurante du trio, et celle dont ce dépôt est l'application directe.

Le problème posé : **Claude Code démarre chaque session avec un contexte vide**. Sans mémoire persistante, il faudrait répéter conventions, commandes et préférences à chaque ouverture.

Deux mécanismes sont distingués, et la distinction reste valable : **CLAUDE.md**, écrit par l'utilisateur, contenant instructions, règles et conventions, avec une portée projet / utilisateur / organisation ; et l'**auto memory**, écrite par Claude, contenant les apprentissages découverts, rattachée au dépôt.

Les quatre emplacements possibles sont détaillés avec leur ordre de priorité — le plus spécifique l'emporte. Les imports, les fichiers liés et les règles ciblées par `.claude/rules/` complètent le dispositif.

**Le `CLAUDE.md` de ce projet, avec ses sous-fichiers thématiques auto-chargés, est né de cette leçon.**

## Notes liées

- **⬅️ Précédente** · [[2026-04-10_lecon01_fondamentaux]]
  dont la contrainte de contexte trouve ici sa réponse
- **➡️ Suivante** · [[2026-04-10_lecon03_mode-plan-reflexion-etendue]]
  troisième et dernière leçon de la série d'avril
