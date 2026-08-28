import { useState, useEffect } from 'react'
import CarteLivrable from './CarteLivrable'
import type { CategorieResumee, Livrable, ReponseLivrables } from './types'

// Nombre de cartes affichées avant dépliage. Une catégorie peut contenir
// plusieurs centaines de fichiers (232 leçons au 28/08/2026) : tout afficher
// d'emblée rendrait la page illisible et lente à peindre.
const APERCU = 12

// GrilleCategorie reçoit ses données d'en-tête via props :
//   nomCle   : clé API ("lecons", "quiz", …)
//   label    : label lisible ("Leçons", "Quiz", …)
//   categorie: { nombre, taille_ko } — les compteurs, issus de /api/inventaire
//
// MAIS il charge lui-même la LISTE COMPLÈTE via /api/livrables?categorie=X.
// C'est la route construite en leçon 04, restée inutilisée jusqu'ici : le
// composant affichait `categorie.recents`, soit les 5 plus récents seulement.
//
// Pourquoi chaque catégorie charge ses propres données plutôt qu'un fetch
// global dans App : un composant qui possède son état est réutilisable et
// testable seul. C'est aussi ce qui permet à une catégorie d'échouer sans
// emporter les cinq autres.
interface Props {
  nomCle: string
  label: string
  /** Compteurs issus de /api/inventaire — la liste, elle, est chargée ici. */
  categorie: CategorieResumee
}

function GrilleCategorie({ nomCle, label, categorie }: Props) {
  // useState<T | null> : le type doit inclure la valeur initiale, sinon TypeScript
  // infère `null` seul et refuse ensuite le tableau.
  const [livrables, setLivrables] = useState<Livrable[] | null>(null)
  const [chargement, setChargement] = useState(true)
  const [erreur, setErreur] = useState<string | null>(null)
  const [deplie, setDeplie] = useState(false)

  // Dépendance [nomCle] : l'effet est rejoué si la catégorie change.
  // Un tableau vide serait faux ici — le composant est monté une fois par
  // catégorie, mais rien ne garantit que React ne le réutilise pas.
  useEffect(() => {
    let annule = false   // évite un setState après démontage du composant

    fetch('/api/livrables?categorie=' + encodeURIComponent(nomCle))
      .then(reponse => {
        if (!reponse.ok) {
          throw new Error('réponse ' + reponse.status)
        }
        return reponse.json()
      })
      .then((donnees: ReponseLivrables) => {
        if (annule) return
        setLivrables(donnees.livrables)
        setChargement(false)
      })
      .catch((err: unknown) => {
        if (annule) return
        // `catch` reçoit un unknown : on ne suppose pas que c'est une Error.
        setErreur(err instanceof Error ? err.message : String(err))
        setChargement(false)
      })

    return () => { annule = true }   // fonction de nettoyage
  }, [nomCle])

  // Note de typage (28/08/2026) : les conditions d'affichage testent `livrables !== null`
  // et non `!chargement && !erreur`. Le compilateur ne peut pas déduire du second que le
  // tableau est chargé — c'est un invariant que nous savions vrai, et que rien dans le
  // code ne garantissait. Tester la donnée elle-même est à la fois plus sûr et plus clair.
  //
  // État dérivé : calculé à chaque rendu à partir de l'état existant.
  // On ne le stocke PAS dans un useState — ce serait une donnée en double,
  // qu'il faudrait penser à resynchroniser à chaque changement.
  const visibles = livrables === null
    ? []
    : (deplie ? livrables : livrables.slice(0, APERCU))
  const reste = livrables === null ? 0 : livrables.length - APERCU

  return (
    <section className={'categorie categorie--' + nomCle}>
      <div className="categorie-en-tete">
        <h2>{label}</h2>
        <span className="badge">{categorie.nombre} fichier(s)</span>
        <span className="taille">{categorie.taille_ko} Ko au total</span>
      </div>

      {chargement && <p className="statut-categorie">Chargement…</p>}

      {erreur && (
        <p className="statut-categorie erreur">
          ⚠️ Liste indisponible ({erreur}).
        </p>
      )}

      {livrables !== null && livrables.length === 0 && (
        <p className="vide">Aucun fichier dans cette catégorie.</p>
      )}

      {livrables !== null && livrables.length > 0 && (
        <>
          <div className="grille-cartes">
            {visibles.map(fichier => (
              <CarteLivrable key={fichier.nom} fichier={fichier} />
            ))}
          </div>

          {reste > 0 && (
            <button
              type="button"
              className="bouton-deplier"
              onClick={() => setDeplie(!deplie)}
            >
              {deplie
                ? 'Replier — n’afficher que ' + APERCU + ' fichiers'
                : 'Afficher les ' + reste + ' autres fichiers'}
            </button>
          )}
        </>
      )}
    </section>
  )
}

export default GrilleCategorie
