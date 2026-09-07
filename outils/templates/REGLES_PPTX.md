# Règles de génération PPTX — quiz et infographies

> Sorti de `CLAUDE.md` le 07/09/2026 (levier 3) : seul `rbpp-pipeline` produit des PPTX,
> ces règles n'ont donc pas à être chargées par les treize autres jobs. **Son prompt porte
> désormais l'instruction explicite de lire ce fichier avant toute génération PPTX.**
>
> ⚠️ Les deux « règles critiques » de la section infographies viennent de bugs réels qui
> rendaient le fichier **inouvrable par PowerPoint** : ne pas les contourner.
> Templates associés : `outils/templates/quiz_style.js`, `infographie_style.js`, `word_style.js`.

## Quiz PowerPoint

- ~100 questions QCM par quiz
- Alternance stricte : slide question / slide réponse
- Slide question : question + 4 propositions (A, B, C, D)
- Slide réponse : bonne réponse mise en évidence + explication courte
- Style : fond bleu marine `#1B3A6B`, texte blanc, police Calibri
- Couverture équilibrée de l'ensemble du document source
- Niveau adapté aux professionnels du médico-social
- Livrable → `livrables/quiz/`

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

pres.writeFile({ fileName: "livrables/quiz/quiz_output.pptx" });
console.log("✅ Quiz généré avec succès.");
```


---

## Infographies PowerPoint (format pétale)

- Fleur avec 6 à 8 pétales selon le nombre de thèmes
- Disposition radiale, centrée, pétales symétriques
- Fond blanc, couleurs distinctes par pétale (palette harmonieuse)
- Police Calibri, format 16:9
- Titre au centre de la fleur
- Livrable → `livrables/infographies/`

### ⚠️ Règle critique 1 — Lignes de connexion radiales (dimensions positives)

PowerPoint refuse d'ouvrir un PPTX si une forme a une dimension négative (`cx="-..."`).
Lors du dessin de lignes du centre vers des pétales positionnés à gauche ou au-dessus,
`w = x2 - x1` ou `h = y2 - y1` peut devenir négatif.

**Toujours utiliser ce helper** :
```javascript
function addLine(slide, x1, y1, x2, y2, color, width = 2) {
  const x = Math.min(x1, x2);
  const y = Math.min(y1, y2);
  const w = Math.max(Math.abs(x2 - x1), 0.01);
  const h = Math.max(Math.abs(y2 - y1), 0.01);
  slide.addShape("line", {
    x, y, w, h,
    line: { color, width },
    flipH: x2 < x1,
    flipV: y2 < y1
  });
}
```

### ⚠️ Règle critique 2 — Géométrie elliptique (éviter les chevauchements)

Slide LAYOUT_WIDE = 13.33 × 7.5". Plus large que haut → disposition CIRCULAIRE génère du
chevauchement avec titre/footer. Utiliser une ELLIPSE (Rx > Ry).

**Paramètres validés** pour 6 à 8 pétales :
```javascript
const CX = 6.665, CY = 4.10;       // centre légèrement décalé
const Rx = 3.40, Ry = 2.00;        // ellipse : Rx > Ry
const R_CENTER = 1.05;              // cercle central
const PETALE_W = 2.40, PETALE_H = 1.30;  // pétales compacts

// Zones occupées :
// Titre principal     : y ∈ [0.20, 0.75]  (fontSize 28)
// Sous-titre          : y ∈ [0.78, 1.10]  (fontSize 16)
// Zone pétales/centre : y ∈ [1.20, 7.00]
// Pied de page        : y ∈ [7.15, 7.40]  (fontSize 10)
```

**Vérification post-génération** :
```bash
unzip -p [fichier].pptx ppt/slides/slide1.xml | grep -o '<a:ext cx="-' | wc -l
# doit retourner 0 — seul compte 0 ou non-0
# ⚠️ grep -o … | wc -l, PAS grep -c : slide1.xml tient sur UNE SEULE LIGNE. Mesuré le 07/09/2026 :
#    grep -c '<a:ext cx=' → 1, alors que le compte réel est 44. La forme -c ne répond juste que par
#    chance ici (présence/absence) ; sur un décompte elle mentirait.
```

