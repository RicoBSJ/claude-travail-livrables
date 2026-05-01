---
name: restaurer-jobs
description: Recrée tous les jobs CronCreate planifiés du projet à partir de jobs_config.json. À utiliser au démarrage de chaque session Claude Code.
---

# Restauration des jobs planifiés

Lis le fichier de configuration : /Users/utilisateur/kDrive/Claude_Travail/jobs_config.json

Affiche d'abord le résumé des jobs à créer sous forme de tableau :
| Nom | Cron | Récurrence | Livrable |

Puis crée chacun des jobs avec CronCreate en utilisant exactement :
- le champ "cron" comme expression cron
- le champ "prompt" comme prompt
- recurring: true
- durable: true

Pour chaque job créé, confirme avec : ✅ [nom] — ID [id] — [récurrence]

Si un job échoue, signale-le clairement et passe au suivant.

À la fin, affiche un récapitulatif :
- Nombre de jobs créés / total
- Rappel : ces jobs sont liés à la session et disparaissent à la fermeture de Claude Code
- Commande pour les recréer : /restaurer-jobs
