# CLAUDE.md — Instructions permanentes pour Claude Code

## Contexte professionnel

Je travaille dans le secteur médico-social français, au sein d'établissements de type ESSMS
(foyer de vie, FAM, MAS, SAVS, SAMSAH). Mes productions servent à la formation professionnelle
des équipes et à la démarche qualité.

Les thématiques récurrentes incluent :
- RBPP HAS/ANESM : bientraitance, autodétermination, habitat, troubles du comportement
- Thérapies non médicamenteuses (TNmP) : Snoezelen, PBS, NPI-ES, CMAI
- Droits des personnes accompagnées (TDI/TSA et autres vulnérabilités)
- Qualité de vie au travail (QVT) et prévention de la maltraitance

---

## Structure du projet

```
Claude_Travail/
├── CLAUDE.md               ← ce fichier
├── jobs_config.json        ← configuration des jobs planifiés (CronCreate)
├── Sources/
│   ├── RBPP/               ← PDFs HAS/ANESM bruts (sous-dossier par RBPP)
│   ├── TNmP/               ← fichiers Excel TNmP
│   ├── QVCT/               ← documents QVCT
│   └── Veille/             ← toutes les veilles produites (SERAFIN, RBPP, HAS, NO-CODE+IA)
├── Templates/
│   ├── quiz_style.js       ← template quiz PowerPoint (multi-palette RBPP/CNT/TNmP)
│   ├── infographie_style.js← template infographies (format pétale et cartes)
│   └── word_style.js       ← template documents Word
├── En_cours/               ← scripts temporaires + node_modules (à nettoyer après chaque tâche)
├── Livrables/
│   ├── Quiz/               ← convention : quiz_[type]_[slug]_YYYY-MM-DD.pptx
│   ├── Infographies/       ← convention : infographie_[type]_[slug]_YYYY-MM-DD.pptx
│   ├── Leçons/             ← leçons Word hebdomadaires (NO-CODE+IA)
│   └── Documents/          ← documents Word divers
├── Ressources/             ← documentation de référence externe (MCP, outils, guides)
└── Prompt/
    ├── session_YYYY-MM-DD_prompts.txt  ← logs de sessions actives
    └── Archives/           ← anciens prompts .rtf
```

### Conventions de nommage des livrables

| Type | Format | Exemple |
|------|--------|---------|
| Veille | `YYYY-MM-DD_veille_[sujet].docx` | `2026-04-06_veille_SERAFIN-PH.docx` |
| Quiz | `quiz_[type]_[slug]_YYYY-MM-DD.pptx` | `quiz_rbpp_projet-personnalise_2026-04-06.pptx` |
| Infographie | `infographie_[type]_[slug]_YYYY-MM-DD.pptx` | `infographie_rbpp_tsa-enfant-adolescent_2026-02-12.pptx` |
| Leçon NO-CODE+IA | `YYYY-MM-DD_lecon-nocode-ia_NN_[slug].docx` | `2026-04-10_lecon-nocode-ia_01_ia-agentique-production.docx` |

---

## Stack technique

- **Runtime** : Node.js
- **Librairie PPTX** : pptxgenjs
- **Librairie Word** : docx (npm)
- **Librairie PDF** : pdf-parse (lecture), pdfkit (création)
- **Langue des scripts** : JavaScript (Node.js)
- Toujours vérifier si `node_modules` existe avant d'installer des dépendances
- Toujours utiliser `npm install` dans `En_cours/` pour les scripts temporaires

---

## Règles générales

- Lire le fichier source en entier avant de commencer à générer quoi que ce soit.
- Utiliser les templates existants dans `Templates/` si disponibles.
- Sauvegarder les livrables finaux dans le bon sous-dossier de `Livrables/`.
- Utiliser `En_cours/` pour les scripts et fichiers intermédiaires.
- Nettoyer `En_cours/` après chaque tâche terminée.
- Pour toute action irréversible (suppression, écrasement), demander confirmation d'abord.
- Afficher un plan structuré avant de générer un fichier long (>20 slides ou >10 pages).

---

## Quiz PowerPoint

- ~100 questions QCM par quiz
- Alternance stricte : slide question / slide réponse
- Slide question : question + 4 propositions (A, B, C, D)
- Slide réponse : bonne réponse mise en évidence + explication courte
- Style : fond bleu marine `#1B3A6B`, texte blanc, police Calibri
- Couverture équilibrée de l'ensemble du document source
- Niveau adapté aux professionnels du médico-social
- Livrable → `Livrables/Quiz/`

### Script type (pptxgenjs)
```javascript
const pptx = require("pptxgenjs");
const fs = require("fs");

// Charger les questions depuis un JSON généré au préalable
const questions = JSON.parse(fs.readFileSync("questions.json", "utf8"));

let pres = new pptx.default();
pres.layout = "LAYOUT_WIDE"; // 16:9

questions.forEach((q, i) => {
  // Slide question
  let slideQ = pres.addSlide();
  slideQ.background = { color: "1B3A6B" };
  slideQ.addText(`Q${i + 1}. ${q.question}`, {
    x: 0.5, y: 0.5, w: "90%", fontSize: 24, color: "FFFFFF", bold: true
  });
  q.options.forEach((opt, j) => {
    slideQ.addText(`${["A", "B", "C", "D"][j]}. ${opt}`, {
      x: 0.5, y: 2 + j * 0.8, w: "90%", fontSize: 18, color: "FFFFFF"
    });
  });

  // Slide réponse
  let slideR = pres.addSlide();
  slideR.background = { color: "1B3A6B" };
  slideR.addText(`✅ Réponse : ${q.answer}`, {
    x: 0.5, y: 0.5, w: "90%", fontSize: 24, color: "00FF99", bold: true
  });
  slideR.addText(q.explanation, {
    x: 0.5, y: 2, w: "90%", fontSize: 18, color: "FFFFFF"
  });
});

pres.writeFile({ fileName: "Livrables/Quiz/quiz_output.pptx" });
console.log("✅ Quiz généré avec succès.");
```

---

## Infographies PowerPoint (format pétale)

- Fleur avec 6 à 8 pétales selon le nombre de thèmes
- Disposition radiale, centrée, pétales symétriques
- Fond blanc, couleurs distinctes par pétale (palette harmonieuse)
- Police Calibri, format 16:9
- Titre au centre de la fleur
- Livrable → `Livrables/Infographies/`

---

## Documents Word

- Style professionnel, structuré avec titres et sous-titres
- Français, registre professionnel médico-social
- Livrable → `Livrables/Documents/` (documents divers) ou `Livrables/Leçons/` (leçons hebdomadaires)

---

## Veille HAS/ANESM

- Source : https://www.has-sante.fr
- Résumé d'une page max : titre, date, public cible, points clés
- Nom du fichier : `YYYY-MM-DD_veille_HAS.md`
- Livrable → `Sources/Veille/`

## Veille NO-CODE + IA (hebdomadaire, vendredi 8h03)

- Sources : the-decoder.com, huggingface.co/blog, simonwillison.net, openai.com/blog/rss.xml, make.com/en/blog, blog.n8n.io, zapier.com/blog, webflow.com/blog
- Format : leçon active (20% théorie / 80% pratique) avec hyperliens cliquables
- Nom du fichier : `YYYY-MM-DD_lecon-nocode-ia_NN_[slug].docx`
- Livrable → `Livrables/Leçons/`
- Note : openai.com/news retourne 403 → utiliser openai.com/blog/rss.xml

---

## Ce que je n'aime pas

- Slides surchargées en texte
- Formulations trop académiques ou trop familières
- Fichiers intermédiaires oubliés dans `En_cours/`
- Actions irréversibles sans confirmation préalable
- Scripts qui écrasent un livrable existant sans prévenir
