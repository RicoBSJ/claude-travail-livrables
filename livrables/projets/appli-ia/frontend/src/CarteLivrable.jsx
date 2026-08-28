// CarteLivrable affiche une carte pour un fichier.
// Props reçues : fichier = { nom, date, slug, taille, extension }
// date peut être null pour les fichiers hors convention de nommage.
function CarteLivrable({ fichier }) {
  const tailleKo = Math.round(fichier.taille / 1024)

  return (
    <article className="carte">
      <span className="carte-ext">{fichier.extension}</span>
      <p className="carte-slug" title={fichier.nom}>
        {fichier.slug}
      </p>
      {fichier.date !== null ? (
        <p className="carte-date">{fichier.date}</p>
      ) : (
        <p className="carte-date carte-date--null">date inconnue</p>
      )}
      <p className="carte-taille">
        {tailleKo > 0 ? tailleKo + ' Ko' : '< 1 Ko'}
      </p>
    </article>
  )
}

export default CarteLivrable