// src/types.ts — Interfaces du Portail Livrables
// Mis à jour leçon 04 (21/08/2026) : Livrable enrichi avec date, slug, extension
//
// Ce fichier est la "carte d'identité" des données manipulées par l'application.
// Il ne contient aucune logique : uniquement des descriptions de formes.

/**
 * Un livrable est un fichier produit par les jobs automatisés.
 * Leçon 04 : date et slug sont désormais extraits du NOM du fichier
 * (et non du mtime — écart n°3 résolu).
 */
export interface Livrable {
  /** Nom du fichier, extension incluse. Ex : "2026-08-21_lecon-appli-ia_04_donnees.docx" */
  nom: string;
  /** Date au format YYYY-MM-DD extraite du nom. null si le fichier n'a pas de date en préfixe. */
  date: string | null;
  /** Slug descriptif extrait du nom (après la date). Ex : "lecon-appli-ia_04_donnees" */
  slug: string;
  /** Taille en octets, telle que retournée par fs.stat().size */
  taille: number;
  /** Extension en minuscules avec le point : ".docx", ".pptx", ".md"… */
  extension: string;
}

/**
 * Une catégorie regroupe tous les livrables d'un même dossier source.
 */
export interface Categorie {
  /** Nombre total de livrables dans ce dossier et ses sous-dossiers */
  nombre: number;
  /** Poids total arrondi en kilooctets (conservé pour compat frontend) */
  taille_ko: number;
  /** Les 5 livrables les plus récents, triés par date du NOM décroissante */
  recents: Livrable[];
  /** Liste complète (disponible via /api/livrables?categorie=X) */
  livrables: Livrable[];
}

/**
 * L'inventaire complet, clé = identifiant du dossier (lecons, quiz, etc.)
 * C'est ce que retourne la route /api/inventaire.
 */
export type Inventaire = Record<string, Categorie>;

/**
 * Configuration d'un dossier source.
 */
export interface DossierConfig {
  chemin: string;
  extensions: string[];
}
