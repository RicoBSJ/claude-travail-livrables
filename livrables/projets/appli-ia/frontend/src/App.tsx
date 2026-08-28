import { useState, useEffect } from 'react'
import GrilleCategorie from './GrilleCategorie'
import type { Inventaire } from './types'
import './index.css'

// Labels lisibles pour chaque clé de catégorie retournée par l'API.
// L'API retourne { lecons: {...}, quiz: {...}, ... } — on traduit ici.
const LABELS: Record<string, string> = {
  lecons: 'Leçons',
  quiz: 'Quiz',
  infographies: 'Infographies',
  veilles: 'Veilles',
  documents: 'Documents',
  controles: 'Contrôles',
}

function App() {
  // Trois variables d'état :
  //   inventaire  → les données reçues de l'API (null tant que non chargées)
  //   chargement  → true pendant la requête, false ensuite
  //   erreur      → message d'erreur ou null si tout va bien
  const [inventaire, setInventaire]  = useState<Inventaire | null>(null)
  const [chargement, setChargement]  = useState(true)
  const [erreur, setErreur]          = useState<string | null>(null)

  // useEffect avec [] : s'exécute UNE SEULE FOIS, au montage du composant.
  // Sans [], il s'exécuterait après CHAQUE re-render → boucle infinie.
  useEffect(() => {
    fetch('/api/inventaire')
      .then(reponse => {
        if (!reponse.ok) {
          throw new Error(
            'Le serveur a répondu ' + reponse.status +
            '. Vérifiez que scripts/serveur.js tourne sur le port 3000.'
          )
        }
        return reponse.json()
      })
      .then((donnees: Inventaire) => {
        setInventaire(donnees)
        setChargement(false)
      })
      .catch((err: unknown) => {
        setErreur(err instanceof Error ? err.message : String(err))
        setChargement(false)
      })
  }, [])

  // Rendu conditionnel selon l'état courant.
  // React affiche ce que la fonction retourne — rien d'autre.
  if (chargement) {
    return <p className="statut">Chargement de l'inventaire…</p>
  }

  if (erreur) {
    return (
      <div className="statut erreur">
        <p>⚠️ {erreur}</p>
        <p>
          Astuce : ouvrez un terminal à la racine du projet et lancez{' '}
          <code>node scripts/serveur.js</code>
        </p>
      </div>
    )
  }

  // À ce stade, chargement et erreur sont faux — mais TypeScript ne le déduit pas
  // des deux `return` précédents. Ce garde explicite le lui apprend, et protège
  // d'un vrai cas : une réponse 200 dont le corps serait `null`.
  if (inventaire === null) {
    return <p className="statut">Aucune donnée reçue.</p>
  }

  const totalFichiers = Object.values(inventaire)
    .reduce((acc, cat) => acc + cat.nombre, 0)

  return (
    <div className="portail">
      <header className="en-tete">
        <h1>Portail Livrables</h1>
        <p className="sous-titre">
          {Object.keys(inventaire).length} catégorie(s) · {totalFichiers} fichier(s)
        </p>
      </header>

      <main className="contenu">
        {Object.entries(inventaire).map(([cle, categorie]) => (
          <GrilleCategorie
            key={cle}
            nomCle={cle}
            label={LABELS[cle] !== undefined ? LABELS[cle] : cle}
            categorie={categorie}
          />
        ))}
      </main>

      <footer className="pied-de-page">
        <p>Portail Livrables — données locales, aucune donnée personnelle</p>
      </footer>
    </div>
  )
}

export default App