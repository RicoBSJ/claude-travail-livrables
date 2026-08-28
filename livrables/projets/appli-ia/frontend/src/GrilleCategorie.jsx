import CarteLivrable from './CarteLivrable.jsx'

// GrilleCategorie reçoit ses données via props (paramètre de la fonction) :
//   nomCle   : clé API ("lecons", "quiz", …)
//   label    : label lisible ("Leçons", "Quiz", …)
//   categorie: { nombre, taille_ko, recents: [{nom, date, slug, taille, extension}] }
//
// Le composant ne modifie pas les données — il les affiche.
function GrilleCategorie({ nomCle, label, categorie }) {
  return (
    <section className={'categorie categorie--' + nomCle}>
      <div className="categorie-en-tete">
        <h2>{label}</h2>
        <span className="badge">{categorie.nombre} fichier(s)</span>
        <span className="taille">{categorie.taille_ko} Ko au total</span>
      </div>

      {categorie.recents.length === 0 ? (
        <p className="vide">Aucun fichier dans cette catégorie.</p>
      ) : (
        <div className="grille-cartes">
          {categorie.recents.map(fichier => (
            <CarteLivrable key={fichier.nom} fichier={fichier} />
          ))}
        </div>
      )}
    </section>
  )
}

export default GrilleCategorie