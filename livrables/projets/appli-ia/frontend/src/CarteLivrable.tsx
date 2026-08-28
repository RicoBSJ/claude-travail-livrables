import type { Livrable } from './types'

// CarteLivrable affiche une carte pour un fichier.
// La forme des props est décrite par une interface : le compilateur vérifie
// désormais que chaque appelant passe bien un Livrable complet.
interface Props {
  fichier: Livrable
}

function CarteLivrable({ fichier }: Props) {
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