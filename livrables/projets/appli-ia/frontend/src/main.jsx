import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

// createRoot : API React 18+ pour monter une application dans le DOM.
// document.getElementById('root') cible le <div id="root"> de index.html.
//
// StrictMode active des vérifications supplémentaires EN DÉVELOPPEMENT UNIQUEMENT :
// les effets (useEffect) sont appelés deux fois pour détecter les effets de bord.
// Ce double appel disparaît en production (npm run build).
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)