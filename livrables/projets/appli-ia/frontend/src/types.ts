// frontend/src/types.ts — le CONTRAT DE L'API, vu du navigateur
// Ajouté le 28/08/2026, en typant le frontend.
//
// ⚠️ Ce fichier n'est pas un doublon de ../../src/types.ts. Celui-là décrit les
// données telles que le SERVEUR les manipule ; celui-ci décrit ce qui circule
// réellement sur le fil, et les deux ne coïncident pas :
//
//   • /api/inventaire        renvoie { nombre, taille_ko, recents } — SANS `livrables`
//   • /api/livrables?cat=X   renvoie { categorie, nombre, livrables } — une enveloppe,
//                            pas une Categorie
//
// Or `Categorie` dans ../../src/types.ts déclare `recents` ET `livrables` comme
// obligatoires : aucune des deux routes ne renvoie cette forme. C'est le piège que
// la leçon 03 signalait — TypeScript fait confiance aux déclarations, jamais aux
// données à l'exécution. Une interface qui décrit ce qu'on aimerait recevoir ne
// protège de rien.
//
// Règle retenue : le frontend type ce qu'il REÇOIT. À réconcilier côté serveur en
// leçon 08 (API et architecture), où le contrat devrait devenir la source unique.

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
