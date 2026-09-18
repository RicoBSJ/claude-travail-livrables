// frontend/src/types.ts — le CONTRAT DE L'API, vu du navigateur
// Ajouté le 28/08/2026, en typant le frontend. Miroir de ../../src/types.ts depuis le 18/09/2026.
//
// Historique : jusqu'à la leçon 08, ../../src/types.ts déclarait `Categorie` avec `recents` ET
// `livrables` obligatoires — une forme qu'aucune route ne renvoyait. Ce fichier a été écrit pour
// décrire ce qui circule réellement sur le fil :
//
//   • /api/inventaire        renvoie { nombre, taille_ko, recents } — SANS `livrables`
//   • /api/livrables?cat=X   renvoie { categorie, nombre, livrables } — une enveloppe
//
// Depuis la leçon 08 (18/09/2026), le serveur déclare les mêmes noms et les mêmes formes
// (CategorieResumee, Inventaire, ReponseLivrables). Les deux fichiers sont tenus en synchronisation
// par CHOIX, pas par contrainte : testé le 18/09/2026, un `import type` de ../../src/types passe
// tsc et vite build ; seul le serveur de développement refuse de servir hors de server.fs.allow.
// Règle inchangée : le frontend type ce qu'il REÇOIT, et le vérifie contre une réponse réelle.

/** Un livrable, tel que renvoyé par les deux routes. Forme identique de part et d'autre. */
export interface Livrable {
  /** Nom du fichier, extension incluse. */
  nom: string
  /** Date `YYYY-MM-DD` extraite du NOM, ou `null` hors convention de nommage. */
  date: string | null
  /** Slug descriptif extrait du nom, après la date. */
  slug: string
  /** Taille en octets. */
  taille: number
  /** Extension en minuscules, point inclus : `.docx`, `.pptx`, `.md`… */
  extension: string
}

/** Une entrée de `/api/inventaire` : les compteurs et un aperçu. */
export interface CategorieResumee {
  nombre: number
  taille_ko: number
  /** Les 5 plus récents seulement — l'aperçu, pas la liste. */
  recents: Livrable[]
}

/** Réponse complète de `/api/inventaire` : une entrée par dossier suivi. */
export type Inventaire = Record<string, CategorieResumee>

/** Réponse de `/api/livrables?categorie=X` : l'enveloppe et la liste entière. */
export interface ReponseLivrables {
  categorie: string
  nombre: number
  livrables: Livrable[]
}
