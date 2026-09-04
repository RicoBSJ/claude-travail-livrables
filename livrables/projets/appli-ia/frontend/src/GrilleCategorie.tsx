// GrilleCategorie.tsx — mis à jour leçon 06 (04/09/2026)
// Ajout : prop filtreLivrable (fonction de filtre), useMemo sur la liste filtrée.

import { useState, useEffect, useMemo } from 'react'
import CarteLivrable from './CarteLivrable'
import type { CategorieResumee, Livrable, ReponseLivrables } from './types'

const APERCU = 12

// GrilleCategorie reçoit ses données d'en-tête via props ET une fonction de filtre.
// Elle reste responsable du chargement de sa liste complète.
//
// Pourquoi passer une FONCTION plutôt que les critères bruts (recherche, extension) ?
//   → Inversion de dépendance : GrilleCategorie ne connaît pas la logique métier,
//     elle délègue à App. Si la logique de filtrage évolue, on ne touche pas GrilleCategorie.
//   → Testabilité : on peut passer n'importe quelle fonction de filtre dans les tests
//     unitaires, sans simuler l'état d'App.
interface Props {
  nomCle: string
  label: string
  categorie: CategorieResumee
  /** Fonction appliquée à chaque Livrable pour décider s'il s'affiche. */
  filtreLivrable: (livrable: Livrable) => boolean
}

function GrilleCategorie({ nomCle, label, categorie, filtreLivrable }: Props) {
  const [livrables, setLivrables] = useState<Livrable[] | null>(null)
  const [chargement, setChargement] = useState(true)
  const [erreur, setErreur] = useState<string | null>(null)
  const [deplie, setDeplie] = useState(false)

  useEffect(() => {
    let annule = false

    fetch('/api/livrables?categorie=' + encodeURIComponent(nomCle))
      .then(reponse => {
        if (!reponse.ok) throw new Error('réponse ' + reponse.status)
        return reponse.json()
      })
      .then((donnees: ReponseLivrables) => {
        if (annule) return
        setLivrables(donnees.livrables)
        setChargement(false)
      })
      .catch((err: unknown) => {
        if (annule) return
        setErreur(err instanceof Error ? err.message : String(err))
        setChargement(false)
      })

    return () => { annule = true }
  }, [nomCle])

  // ── Filtrage via useMemo ────────────────────────────────────────────────
  // livablesFiltres est recalculé SEULEMENT si livrables ou filtreLivrable changent.
  // Sans useMemo, il serait recalculé à chaque re-render, y compris ceux déclenchés
  // par d'autres états internes — ce qui sur 232 leçons représente du travail inutile.
  //
  // filtreLivrable est une fonction créée dans App à chaque render d'App.
  // Sa référence change à chaque frappe dans le champ de recherche — c'est voulu :
  // on veut que useMemo recalcule quand les critères changent.
  const livrablesFiltes = useMemo(() => {
    if (livrables === null) return null
    return livrables.filter(filtreLivrable)
  }, [livrables, filtreLivrable])

  // Quand le filtre change, on replie la liste (évite un état incohérent :
  // "5 résultats" mais le bouton indique encore "replier — 12 fichiers").
  // On utilise un effet secondaire sur filtreLivrable pour ce cas précis.
  useEffect(() => {
    setDeplie(false)
  }, [filtreLivrable])

  // État dérivé : les cartes visibles, après filtre et dépliage
  const visibles = livrablesFiltes === null
    ? []
    : (deplie ? livrablesFiltes : livrablesFiltes.slice(0, APERCU))
  const reste = livrablesFiltes === null ? 0 : livrablesFiltes.length - APERCU

  // Si aucun livrable ne correspond au filtre : masquer la section entière.
  // C'est plus propre qu'afficher "0 résultat(s)" pour chaque catégorie vide.
  if (livrablesFiltes !== null && livrablesFiltes.length === 0) {
    return null
  }

  return (
    <section className={'categorie categorie--' + nomCle}>
      <div className="categorie-en-tete">
        <h2>{label}</h2>
        <span className="badge">
          {livrablesFiltes !== null
            ? livrablesFiltes.length + ' résultat(s)'
            : categorie.nombre + ' fichier(s)'}
        </span>
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

      {visibles.length > 0 && (
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
                ? 'Replier — n\'afficher que ' + APERCU + ' fichiers'
                : 'Afficher les ' + reste + ' autres résultat(s)'}
            </button>
          )}
        </>
      )}
    </section>
  )
}

export default GrilleCategorie
