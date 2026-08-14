// src/types.ts — Interfaces du Portail Livrables
// Leçon 03 — TypeScript et structure de projet (14/08/2026)
//
// Ce fichier est la "carte d'identité" des données manipulées par l'application.
// Il ne contient aucune logique : uniquement des descriptions de formes.

/**
 * Un livrable est un fichier produit par les jobs automatisés.
 * Cette interface décrit exactement ce que la route /api/inventaire retourne
 * pour chaque entrée du tableau `recents`.
 */
export interface Livrable {
  /** Nom du fichier, extension incluse. Ex : "2026-08-14_lecon-appli-ia_03_typescript.docx" */
  nom: string;
  /** Taille en octets, telle que retournée par fs.statSync().size */
  taille: number;
  /** Date de dernière modification, format ISO 8601 tronqué : "YYYY-MM-DD" */
  modifie: string;
}

/**
 * Une catégorie regroupe tous les livrables d'un même dossier source.
 * C'est ce que contient chaque valeur de l'objet Inventaire.
 */
export interface Categorie {
  /** Nombre total de livrables dans ce dossier et ses sous-dossiers */
  nombre: number;
  /** Poids total arrondi en kilooctets */
  taille_ko: number;
  /** Les 5 livrables les plus récents, triés par date décroissante */
  recents: Livrable[];
}

/**
 * L'inventaire complet, clé = identifiant du dossier (lecons, quiz, etc.)
 * C'est ce que retourne la route /api/inventaire — et ce que lit l'interface web.
 */
export type Inventaire = Record<string, Categorie>;

/**
 * Configuration d'un dossier source : son identifiant court et son chemin absolu sur le disque.
 */
export interface DossierConfig {
  cle: string;
  chemin: string;
}
