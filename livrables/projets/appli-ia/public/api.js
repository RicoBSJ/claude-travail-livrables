// api.js — Accès aux données du serveur
//
// Ce module ne connaît RIEN de l'affichage : il ne touche jamais au DOM.
// Sa seule responsabilité est d'aller chercher les données et de signaler
// les erreurs. On pourrait le réutiliser tel quel dans une autre page.

/**
 * Récupère l'inventaire complet auprès du serveur local.
 * Renvoie une promesse résolue avec l'objet { lecons: {...}, quiz: {...}, ... }
 * ou rejetée si le serveur répond autre chose qu'un succès.
 */
export function chargerInventaire() {
  return fetch("/api/inventaire").then(function (reponse) {
    // Sans ce test, une réponse 404 ou 500 passerait pour un succès et
    // ferait échouer .json() plus loin, avec un message incompréhensible.
    if (!reponse.ok) {
      throw new Error("Réponse serveur : " + reponse.status);
    }
    return reponse.json();
  });
}
