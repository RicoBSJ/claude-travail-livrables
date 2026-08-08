# Exercices du parcours

Artefacts pédagogiques. **Ne font pas partie de l'application** — ils servent à comprendre,
pas à faire tourner le Portail Livrables.

## Challenge de la leçon 01 — l'effet d'une spécification

La leçon 01 propose de demander deux fois la même chose à une IA : d'abord sans contexte,
puis en lui fournissant `SPEC.md`. Les deux scripts ci-dessous sont le résultat réel de cette
expérience, menée le 08/08/2026.

| Fichier | Demande formulée | Ce qu'il produit |
|---|---|---|
| `01_lister_fichiers_sans_spec.js` | « écris-moi un script Node.js qui liste mes fichiers » | Lister générique : tous dossiers, tous types de fichiers, tri sur le `mtime` |
| `02_lister_livrables_avec_spec.js` | la même demande, `SPEC.md` fournie | Les 6 dossiers déclarés, 4 extensions, exclusions, date lue dans le NOM, filtres par type et par mot-clé |

### Les cinq différences

1. **Périmètre** — v1 : n'importe quel dossier · v2 : six sources précises, `livrables/projets/`
   jamais parcouru (exclusion structurelle, pas un filtre qu'on peut oublier).
2. **Date** — v1 : le `mtime`, donc un fichier corrigé remonte en tête · v2 : la date contenue
   dans le nom, comme l'exige la spec.
3. **Type** — v2 déduit le type du dossier d'origine (Leçon, Quiz, Veille…), information absente
   du fichier lui-même.
4. **Exclusions** — v2 écarte les fichiers de verrouillage Office (`~$…`).
5. **Fonctions** — v2 implémente la recherche et le filtre, présents dans la spec mais absents
   de la demande.

### Ce que l'exercice démontre

Les deux programmes n'ont presque rien en commun. Ce n'est pas une question de qualité de code :
**c'est la spécification qui a fait le travail**. Conforme au résultat de Geruslu, Aliyeva &
Tüzün (arXiv, 26/03/2026) cité en leçon 01 — la spécification de la tâche est un facteur
déterminant de la qualité du code généré, devant le choix du modèle.

### Utilisation

```bash
node exercices/01_lister_fichiers_sans_spec.js [dossier]
node exercices/02_lister_livrables_avec_spec.js [--type=veille] [--recherche=imac]
```

Les deux sont en **lecture seule**.

### Écart trouvé grâce à cet exercice

Le script conforme a révélé que `README.md` était compté comme un livrable dans
`livrables/controles/`. Corrigé dans `SPEC.md` v1.2.
