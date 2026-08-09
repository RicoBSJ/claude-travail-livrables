// app.js — Portail Livrables
//
// Extrait d'index.html le 09/08/2026 : le JavaScript y représentait 80 % du
// fichier. Séparer structure (HTML), style (CSS) et comportement (JS).
//
// Ce fichier est chargé par <script src="/app.js"></script> placé à la FIN du
// <body>, comme l'était le bloc inline. Cette position garantit que le HTML
// existe déjà quand le script s'exécute : document.getElementById() trouve
// donc bien ses éléments. Déplacer cette balise dans le <head> casserait tout,
// sauf à lui ajouter l'attribut defer.

// Appel à l'API locale : le serveur Node.js renvoie l'inventaire en JSON
fetch("/api/inventaire")
  .then(function(reponse) {
    // Si le serveur renvoie une erreur HTTP, on la propage
    if (!reponse.ok) {
      throw new Error("Réponse serveur : " + reponse.status);
    }
    return reponse.json();
  })
  .then(function(data) {
    // Mise à jour de la bande de statut
    const nbCategories = Object.keys(data).length;
    document.getElementById("statut").textContent =
      "Inventaire chargé — " + nbCategories + " catégories.";

    // Construction des cartes
    const grille = document.getElementById("grille");

    for (const cle of Object.keys(data)) {
      const info  = data[cle];
      const carte = document.createElement("div");
      carte.className = "carte";

      // Liste des fichiers récents
      let recentsHTML;
      if (info.recents.length === 0) {
        recentsHTML = "<p class='meta'>Aucun fichier</p>";
      } else {
        const items = info.recents.map(function(f) {
          return "<li><span class='date'>" + f.modifie + "</span>" + f.nom + "</li>";
        });
        recentsHTML = "<ul class='recents'>" + items.join("") + "</ul>";
      }

      carte.innerHTML =
        "<h2>" + cle + "</h2>" +
        "<p class='meta'>" + info.nombre + " fichier(s) · " + info.taille_ko + " Ko</p>" +
        recentsHTML;

      grille.appendChild(carte);
    }

    // Totaux, calculés à partir des données DÉJÀ reçues par ce fetch.
    // Object.values() transforme l'objet { lecons: {...}, quiz: {...} }
    // en tableau [ {...}, {...} ], seul format que reduce sait parcourir.
    const categories = Object.values(data);

    const totalLivrables = categories.reduce(
      function (total, cat) { return total + cat.nombre; },
      0
    );

    const poidsMo = categories.reduce(
      function (total, cat) { return total + cat.taille_ko; },
      0
    ) / 1024;

    // L'heure est prise ICI, au moment où les données sont réellement arrivées —
    // et non au chargement de la page, qui précède la réponse du serveur.
    const heureChargement = new Date().toLocaleTimeString("fr-FR");

    document.getElementById("totaux").textContent =
      totalLivrables + " livrables · " +
      poidsMo.toFixed(1).replace(".", ",") + " Mo" +
      " — chargé à " + heureChargement;
  })
  .catch(function(erreur) {
    document.getElementById("statut").textContent =
      "Erreur lors du chargement : " + erreur.message;
  });
