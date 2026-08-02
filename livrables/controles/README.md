# Notes de contrôle qualité

Produites chaque **dimanche à 11h03** par le job `controle-livrables`, après tous les autres
jobs de la semaine.

## Ce que le contrôle vérifie

| Contrôle | Détail |
|---|---|
| **Liens** | chaque URL testée (200 / 403 anti-robot / 404 = lien mort) |
| **Chiffres officiels** | tout taux, seuil, plafond ou barème remonté à la **source primaire** et comparé à la valeur en vigueur **ce jour** |
| **Citations** | toute phrase entre guillemets attribuée à un auteur ou une autorité |
| **Fenêtre temporelle** | pour les veilles : chaque actualité est-elle bien dans la fenêtre annoncée ? |
| **Décompte des sources** | le « X/Y sources » correspond-il à la liste réelle ? |
| **Cohérence interne** | calculs refaits, corrigés d'exercices confrontés à la théorie de leur propre document |

## Ce qu'il ne fait pas

- **Il ne corrige jamais rien.** Il constate et signale ; toute correction reste une décision humaine.
- **Il n'évalue pas la qualité éditoriale** (style, intérêt pédagogique, pertinence). Le contrôleur
  est le même type de modèle que le producteur : son jugement de goût partagerait les mêmes angles
  morts. Sa valeur est dans la vérification **mécanique et externe**.

## Lire une note

Trois niveaux de gravité :

- 🔴 **Erreur factuelle** — valeur fausse ou périmée, **confirmée à la source primaire**. À corriger.
- 🟠 **Imprécision** — valeur juste mais mal sourcée, floutée, ou hors fenêtre.
- 🟢 **Rien à signaler.**

Une section « 🔍 Non vérifiable » liste ce qui n'a pas pu être contrôlé et pourquoi : c'est une
information, pas un blanc-seing.

## Déclenchement manuel

```bash
bash outils/scripts/run_job.sh controle-livrables
```
