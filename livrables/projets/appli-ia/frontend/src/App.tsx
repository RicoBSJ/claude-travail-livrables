// App.tsx — mis à jour leçon 06 (04/09/2026)
// Ajout : état des filtres, useMemo pour les listes dérivées, BarreRecherche.

import { useState, useEffect, useMemo } from 'react'
import GrilleCategorie from './GrilleCategorie'
import BarreRecherche from './BarreRecherche'
import type { Inventaire, Livrable } from './types'
import './index.css'

// Labels lisibles pour chaque clé de catégorie retournée par l'API.
const LABELS: Record<string, string> = {
  lecons: 'Leçons',
  quiz: 'Quiz',
  infographies: 'Infographies',
  veilles: 'Veilles',
  documents: 'Documents',
  controles: 'Contrôles',
}

// Extensions reconnues dans le portail — sert à peupler le <select> Format.
// L'ordre reflète la fréquence d'apparition plutôt que l'ordre alphabétique.
const EXTENSIONS_CONNUES = ['.docx', '.pptx', '.pdf', '.md']

// Normalise une chaîne pour la recherche : minuscules, sans accents.
// Cela permet de taper "lecon" et de trouver "leçon", ou "education" pour "éducation".
function normaliser(s: string): string {
  return s
    .toLowerCase()
    .normalize('NFD')           // décompose les caractères accentués
    .replace(/[\u0300-\u036f]/g, '') // supprime les diacritiques
}

// Teste si un livrable correspond aux trois filtres actifs.
// Exportée ici pour être réutilisable et testable unitairement en leçon 09.
export function matcheFiltres(
  livrable: Livrable,
  recherche: string,
  extension: string
): boolean {
  // Filtre par extension (exact)
  if (extension !== '' && livrable.extension !== extension) return false

  // Filtre par texte : on cherche dans le nom ET dans le slug normalisés.
  if (recherche !== '') {
    const cible = normaliser(livrable.nom + ' ' + livrable.slug)
    if (!cible.includes(normaliser(recherche))) return false
  }

  return true
}

function App() {
  // ── État des données ────────────────────────────────────────────────────
  const [inventaire, setInventaire]  = useState<Inventaire | null>(null)
  const [chargement, setChargement]  = useState(true)
  const [erreur, setErreur]          = useState<string | null>(null)

  // ── État des filtres ────────────────────────────────────────────────────
  // Trois variables d'état distinctes plutôt qu'un objet unique : chaque
  // setState ne re-rend que les composants qui lisent cette valeur.
  const [recherche, setRecherche]           = useState('')
  const [categorieActive, setCategorieActive] = useState('')
  const [extensionActive, setExtensionActive] = useState('')

  // useEffect avec [] : s'exécute UNE SEULE FOIS, au montage du composant.
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

  // ── Données dérivées avec useMemo ───────────────────────────────────────
  // La liste des catégories à afficher dépend du filtre catégorieActive.
  // useMemo recalcule seulement si inventaire ou categorieActive changent —
  // pas à chaque frappe dans le champ texte, par exemple.
  const categoriesVisibles = useMemo(() => {
    if (inventaire === null) return []
    if (categorieActive === '') return Object.keys(inventaire)
    return Object.keys(inventaire).filter(cle => cle === categorieActive)
  }, [inventaire, categorieActive])

  // Compteur global de résultats : somme des fichiers correspondant aux filtres
  // dans toutes les catégories visibles. Cette valeur n'est disponible qu'ici
  // car GrilleCategorie charge ses propres données.
  // On s'appuie sur les compteurs de l'inventaire (pas sur les listes chargées
  // par GrilleCategorie) — approximation acceptable : l'inventaire agrège tout.
  // La valeur exacte par catégorie est affichée dans chaque GrilleCategorie.
  const totalFichiers = useMemo(() => {
    if (inventaire === null) return 0
    return categoriesVisibles.reduce(
      (acc, cle) => acc + inventaire[cle].nombre,
      0
    )
  }, [inventaire, categoriesVisibles])

  // ── Rendu conditionnel ─────────────────────────────────────────────────
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

  if (inventaire === null) {
    return <p className="statut">Aucune donnée reçue.</p>
  }

  return (
    <div className="portail">
      <header className="en-tete">
        <h1>Portail Livrables</h1>
        <p className="sous-titre">
          {Object.keys(inventaire).length} catégorie(s) ·{' '}
          {Object.values(inventaire).reduce((a, c) => a + c.nombre, 0)} fichier(s)
        </p>
      </header>

      {/* Barre de recherche — composant contrôlé, état dans App */}
      <BarreRecherche
        valeurRecherche={recherche}
        categorieActive={categorieActive}
        extensionActive={extensionActive}
        categories={Object.keys(inventaire)}
        labels={LABELS}
        extensions={EXTENSIONS_CONNUES}
        onRecherche={setRecherche}
        onCategorie={setCategorieActive}
        onExtension={setExtensionActive}
        nombreResultats={totalFichiers}
      />

      <main className="contenu">
        {categoriesVisibles.map(cle => (
          <GrilleCategorie
            key={cle}
            nomCle={cle}
            label={LABELS[cle] !== undefined ? LABELS[cle] : cle}
            categorie={inventaire[cle]}
            // On passe une fonction de filtre, pas les valeurs brutes.
            // GrilleCategorie peut ainsi filtrer sa propre liste sans
            // connaître la logique métier — c'est la responsabilité d'App.
            filtreLivrable={(liv: Livrable) =>
              matcheFiltres(liv, recherche, extensionActive)
            }
          />
        ))}

        {categoriesVisibles.length === 0 && (
          <p className="statut">
            Aucune catégorie ne correspond aux filtres actifs.
          </p>
        )}
      </main>

      <footer className="pied-de-page">
        <p>Portail Livrables — données locales, aucune donnée personnelle</p>
      </footer>
    </div>
  )
}

export default App
