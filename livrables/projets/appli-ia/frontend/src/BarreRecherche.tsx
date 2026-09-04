// BarreRecherche.tsx — leçon 06 (04/09/2026)
//
// Ce composant est dit « contrôlé » : il ne possède PAS son propre état.
// Les valeurs affichées (valeurRecherche, categorieActive, extensionActive) lui
// arrivent par props, et les changements remontent vers App via les callbacks
// onRecherche, onCategorie, onExtension.
//
// Pourquoi ce choix ?
//   App possède les données. Les filtres sont une clé de lecture de ces données.
//   Placer l'état des filtres dans App garantit que le composant qui filtre
//   (App → GrilleCategorie) et celui qui expose les commandes (BarreRecherche)
//   voient toujours la même vérité.

interface Props {
  /** Valeur courante du champ de texte */
  valeurRecherche: string
  /** Clé de catégorie active, "" = toutes */
  categorieActive: string
  /** Extension active (".docx", ".pptx"…), "" = toutes */
  extensionActive: string
  /** Liste des clés de catégorie disponibles (pour les options du <select>) */
  categories: string[]
  /** Labels lisibles, indexés par clé */
  labels: Record<string, string>
  /** Toutes les extensions présentes dans le portail */
  extensions: string[]
  /** Appelé à chaque frappe dans le champ de recherche */
  onRecherche: (valeur: string) => void
  /** Appelé quand on change de catégorie */
  onCategorie: (cle: string) => void
  /** Appelé quand on change d'extension */
  onExtension: (ext: string) => void
  /** Nombre de résultats actuellement visibles (pour le retour utilisateur) */
  nombreResultats: number
}

function BarreRecherche({
  valeurRecherche,
  categorieActive,
  extensionActive,
  categories,
  labels,
  extensions,
  onRecherche,
  onCategorie,
  onExtension,
  nombreResultats,
}: Props) {
  const aFiltres =
    valeurRecherche !== '' ||
    categorieActive !== '' ||
    extensionActive !== ''

  return (
    <div className="barre-recherche">
      {/* Champ de texte libre */}
      <label className="barre-label" htmlFor="champ-recherche">
        Rechercher
      </label>
      <input
        id="champ-recherche"
        type="search"
        className="barre-input"
        placeholder="Nom ou slug…"
        value={valeurRecherche}
        onChange={e => onRecherche(e.target.value)}
        autoComplete="off"
      />

      {/* Filtre par catégorie */}
      <label className="barre-label" htmlFor="filtre-categorie">
        Catégorie
      </label>
      <select
        id="filtre-categorie"
        className="barre-select"
        value={categorieActive}
        onChange={e => onCategorie(e.target.value)}
      >
        <option value="">Toutes</option>
        {categories.map(cle => (
          <option key={cle} value={cle}>
            {labels[cle] !== undefined ? labels[cle] : cle}
          </option>
        ))}
      </select>

      {/* Filtre par extension */}
      <label className="barre-label" htmlFor="filtre-extension">
        Format
      </label>
      <select
        id="filtre-extension"
        className="barre-select"
        value={extensionActive}
        onChange={e => onExtension(e.target.value)}
      >
        <option value="">Tous</option>
        {extensions.map(ext => (
          <option key={ext} value={ext}>
            {ext}
          </option>
        ))}
      </select>

      {/* Retour utilisateur : nombre de résultats + bouton de remise à zéro */}
      <span className="barre-resultats">
        {nombreResultats} résultat{nombreResultats !== 1 ? 's' : ''}
      </span>

      {aFiltres && (
        <button
          type="button"
          className="barre-reset"
          onClick={() => {
            onRecherche('')
            onCategorie('')
            onExtension('')
          }}
        >
          ✕ Effacer les filtres
        </button>
      )}
    </div>
  )
}

export default BarreRecherche
