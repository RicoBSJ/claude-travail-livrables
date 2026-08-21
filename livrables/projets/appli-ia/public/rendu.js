// rendu.js — Affichage dans la page
// Mis à jour leçon 04 (21/08/2026) : f.modifie → f.date (résout écart n°3)
//
// Ce module ne connaît RIEN du réseau : il ne fait aucun fetch. Il reçoit des
// données déjà chargées et se contente de les mettre à l'écran. C'est la
// contrepartie exacte d'api.js, qui ne touche jamais au DOM.

/** Écrit un message dans la bande de statut, en haut de la page. */
export function afficherStatut(texte) {
  document.getElementById('statut').textContent = texte;
}

/** Construit le fragment HTML de la liste des fichiers récents d'une catégorie. */
function listeRecents(recents) {
  if (recents.length === 0) {
    return "<p class='meta'>Aucun fichier</p>";
  }
  const items = recents.map(function (f) {
    // f.date est la date extraite du NOM du fichier (leçon 04).
    // Pour les fichiers antérieurs à la convention de nommage, f.date vaut null.
    const dateLabel = f.date ?? '(sans date)';
    return "<li><span class='date'>" + dateLabel + '</span>' + f.nom + '</li>';
  });
  return "<ul class='recents'>" + items.join('') + '</ul>';
}

/** Construit une carte par catégorie et les insère dans la grille. */
export function afficherCartes(data) {
  const grille = document.getElementById('grille');

  for (const cle of Object.keys(data)) {
    const info  = data[cle];
    const carte = document.createElement('div');
    carte.className = 'carte';

    carte.innerHTML =
      '<h2>' + cle + '</h2>' +
      "<p class='meta'>" + info.nombre + ' fichier(s) · ' + info.taille_ko + ' Ko</p>' +
      listeRecents(info.recents);

    grille.appendChild(carte);
  }
}

/** Calcule et affiche les totaux dans le pied de page. */
export function afficherTotaux(data) {
  const categories = Object.values(data);

  const totalLivrables = categories.reduce(
    function (total, cat) { return total + cat.nombre; },
    0
  );

  const poidsMo = categories.reduce(
    function (total, cat) { return total + cat.taille_ko; },
    0
  ) / 1024;

  const heureChargement = new Date().toLocaleTimeString('fr-FR');

  document.getElementById('totaux').textContent =
    totalLivrables + ' livrables · ' +
    poidsMo.toFixed(1).replace('.', ',') + ' Mo' +
    ' — chargé à ' + heureChargement;
}
