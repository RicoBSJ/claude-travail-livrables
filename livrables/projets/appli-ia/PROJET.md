# Projet fil rouge — « Portail Livrables »

> Mémoire du parcours **Développement d'applications avec l'IA** (12 leçons, vendredi 8h03).
> Le job `appli-ia-lecon` lit ce fichier au début de chaque leçon et le met à jour à la fin.
> **Ne pas supprimer** : sans lui, la continuité du fil rouge est perdue.

---

## État de l'application

**Non démarrée.** Le parcours commence à la leçon 01 (cadrage et spécification).

## Objectif du projet

Une application web **locale** qui liste, recherche et filtre les livrables produits par les
jobs automatisés du projet Claude_Travail : leçons (`livrables/lecons/`), veilles
(`sources/veille/`), quiz et infographies.

Pourquoi ce sujet :
- les données existent déjà sur le disque, aucune saisie à créer ;
- l'outil sert vraiment au quotidien (plus de 100 livrables accumulés) ;
- aucune donnée de personne accompagnée n'y entre jamais — uniquement mes propres documents
  de travail.

## Choix techniques arrêtés

| Élément | Choix | Décidé en leçon |
|---|---|---|
| Langage | JavaScript / TypeScript | avant le parcours |
| Runtime | Node.js | avant le parcours |
| Framework | *à décider* | leçon 01 ou 05 |
| Base de données | *à décider* | leçon 07 |

Aucune version de bibliothèque n'est encore figée : elles seront relevées à la documentation
officielle au fil des leçons, jamais de mémoire.

## Fichiers du projet

Aucun pour l'instant.

## Livré à la leçon NN

Rien encore.

## Reste à faire

L'intégralité de la feuille de route (12 leçons) :

1. Cadrage, spécification, environnement
2. Socle web, premier écran
3. TypeScript et structure de projet
4. Lecture des données réelles (Node.js)
5. Interface (React / Next.js)
6. Recherche et filtres
7. Persistance (base de données)
8. API et architecture
9. Qualité, tests, débogage
10. Sécurité et données (RGPD)
11. Mise en production
12. Maintenance et évolution

## Points en suspens

- Le périmètre exact du portail (livrables seuls, ou aussi les sources ?) est à trancher en
  leçon 01.
- Le choix du framework d'interface dépendra du niveau de complexité constaté aux leçons 2-4.
