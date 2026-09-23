// src/types.ts — Contrat de l'API du Portail Livrables (côté serveur)
// Mis à jour leçon 04 (21/08/2026) : Livrable enrichi avec date, slug, extension
// Mis à jour leçon 08 (18/09/2026) : Categorie scindée en CategorieResumee + ReponseLivrables
//   — alignement avec ce que les routes renvoient réellement
//   — alignement avec frontend/src/types.ts (même noms, mêmes formes)
//
// Ce fichier décrit les FORMES DES DONNÉES telles que le serveur les expose.
// Il ne contient aucune logique : uniquement des descriptions.
//
// frontend/src/types.ts est le miroir de ce fichier vu du navigateur.
// Les deux ne peuvent pas être le même fichier (systèmes de modules différents :
// CommonJS côté serveur, modules ES côté Vite). Tenir les deux en sync.

/**
 * Un livrable est un fichier produit par les jobs automatisés.
 * Leçon 04 : date et slug sont extraits du NOM du fichier.
 * Leçon 08 : extraireDate() gère aussi la date en fin de nom (quiz, infographies).
 */
export interface Livrable {
  /** Nom du fichier, extension incluse. Ex : "2026-08-21_lecon-appli-ia_04_donnees.docx" */
  nom: string;
  /** Date au format YYYY-MM-DD extraite du nom. null si le fichier n'a pas de date. */
  date: string | null;
  /** Slug descriptif extrait du nom. Ex : "lecon-appli-ia_04_donnees" */
  slug: string;
  /** Taille en octets, telle que retournée par fs.stat().size */
  taille: number;
  /** Extension en minuscules avec le point : ".docx", ".pptx", ".md"… */
  extension: string;
}

/**
 * Une entrée de /api/inventaire : compteurs et aperçu des 5 plus récents.
 * Cette route ne renvoie PAS la liste complète (voir ReponseLivrables).
 * Avant leçon 08, ce type s'appelait Categorie et déclarait livrables obligatoire —
 * aucune route ne renvoyait cette forme.
 */
export interface CategorieResumee {
  /** Nombre total de livrables dans ce dossier et ses sous-dossiers */
  nombre: number;
  /** Poids total arrondi en kilooctets */
  taille_ko: number;
  /** Les 5 livrables les plus récents, triés par date du NOM décroissante */
  recents: Livrable[];
}

/**
 * Réponse complète de /api/inventaire : une entrée par dossier suivi.
 * Avant leçon 08, ce type s'appelait Inventaire avec Record<string, Categorie>.
 */
export type Inventaire = Record<string, CategorieResumee>;

/**
 * Réponse de /api/livrables?categorie=X : liste complète d'une catégorie.
 * Avant leçon 08, cette forme n'était déclarée nulle part côté serveur.
 */
export interface ReponseLivrables {
  categorie: string;
  nombre: number;
  livrables: Livrable[];
}

/**
 * Configuration d'un dossier source (usage interne serveur).
 */
export interface DossierConfig {
  chemin: string;
  extensions: string[];
  /** true si les sous-dossiers de `chemin` comptent (lecons/, veille/ sont rangés par série). */
  recursif: boolean;
}
