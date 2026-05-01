Génère un quiz PowerPoint de 100 questions sur les RBPP (Recommandations de Bonnes Pratiques Professionnelles) HAS/ANESM.

1. Identifie les fichiers PDF disponibles dans `Sources/RBPP/`. Si le dossier est vide, demande à l'utilisateur quel document source utiliser.
2. Lis le document source en entier avant de commencer.
3. Génère 100 questions QCM couvrant l'ensemble des thèmes du document de façon équilibrée. Chaque question a :
   - Un énoncé clair (niveau professionnel médico-social)
   - 4 propositions (A, B, C, D) dont une seule est correcte
   - La bonne réponse identifiée
   - Une explication courte (2-3 phrases max)
4. Sauvegarde les questions dans `En_cours/questions_rbpp.json` (format JSON structuré).
5. Génère le fichier PowerPoint via le script Node.js avec pptxgenjs :
   - Fond bleu marine `#1B3A6B`, texte blanc, police Calibri, format 16:9
   - Alternance stricte : slide question / slide réponse
   - Slide question : question + 4 propositions (A, B, C, D)
   - Slide réponse : bonne réponse en vert `#00FF99` + explication
6. Vérifie si un fichier existe déjà dans `Livrables/Quiz/` avec le même nom avant de sauvegarder. Si oui, demande confirmation.
7. Sauvegarde le livrable dans `Livrables/Quiz/quiz_rbpp_YYYYMMDD.pptx`.
8. Nettoie `En_cours/` en supprimant les fichiers intermédiaires (après confirmation).
9. Confirme avec un résumé : nombre de questions, thèmes couverts, chemin du fichier généré.
