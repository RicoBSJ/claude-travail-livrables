// app.js — Point d'entrée du Portail Livrables
//
// Ce fichier ne fait QUE de l'orchestration : il enchaîne les étapes sans
// savoir ni comment on parle au serveur (api.js) ni comment on écrit dans la
// page (rendu.js). Il doit se lire comme un résumé de ce que fait l'application.
//
// Découpage en modules le 09/08/2026 : app.js faisait 80 lignes d'un seul bloc.
//
// ⚠️ DEUX POINTS TECHNIQUES À CONNAÎTRE
//
// 1. La balise dans index.html porte type="module" :
//        <script src="/app.js" type="module"></script>
//    Sans cet attribut, le navigateur refuse les mots-clés import et export.
//
// 2. Les chemins d'import doivent porter l'extension .js — "./api.js" et non
//    "./api". Le navigateur ne devine pas l'extension, contrairement à Node.js.
//
// À noter : un module est différé (defer) par défaut. Sa position en fin de
// <body> n'est donc plus indispensable, mais on la conserve : elle reste
// correcte et évite d'avoir à réexpliquer l'ordre d'exécution.

import { chargerInventaire } from "./api.js";
import { afficherStatut, afficherCartes, afficherTotaux } from "./rendu.js";

chargerInventaire()
  .then(function (data) {
    afficherStatut("Inventaire chargé — " + Object.keys(data).length + " catégories.");
    afficherCartes(data);
    afficherTotaux(data);
  })
  .catch(function (erreur) {
    afficherStatut("Erreur lors du chargement : " + erreur.message);
  });
