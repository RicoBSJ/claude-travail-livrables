import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'

// createRoot : API React 18+ pour monter une application dans le DOM.
// document.getElementById('root') cible le <div id="root"> de index.html.
//
// StrictMode active des vérifications supplémentaires EN DÉVELOPPEMENT UNIQUEMENT :
// les effets (useEffect) sont appelés deux fois pour détecter les effets de bord.
// Ce double appel disparaît en production (npm run build).
// getElementById renvoie HTMLElement | null : TypeScript exige de traiter le null.
// On échoue explicitement plutôt que d'écraser le doute avec un `!` non expliqué.
const racine = document.getElementById('root')
if (racine === null) {
  throw new Error("index.html ne contient pas de <div id=\"root\"> : rien à monter.")
}

createRoot(racine).render(
  <StrictMode>
    <App />
  </StrictMode>
)