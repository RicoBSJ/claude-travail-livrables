# NotebookLM — Architecture & Workflow

## Structure des notebooks

| Notebook | Sources à charger | Usages principaux |
|---|---|---|
| **RBPP** | PDFs HAS, grilles officielles, veilles RBPP, procédures internes | Interrogation recommandations · Auto-diagnostic écart · Livrables formation |
| **Evaluation_HAS** | Référentiel HAS 2022, grilles auto-éval, CR réunions qualité, procédures | Préparation évaluation externe · Plan d'amélioration · Argumentaires preuves |
| **SERAFIN-PH** | Documents SERAFIN-PH, circulaires CNSA, veilles, notes de cadrage | Anticipation bascule 2027 · Veille réglementaire |
| **Formation_Equipe** | PDFs HAS, fiches synthèse, fiches de poste AES/ME/ES, veilles | Formation initiale · Onboarding · Parcours d'intégration sourcé |
| **CPOM** | Documents CPOM, bilans d'activité, indicateurs, procédures, CR CA | Préparation contractuelle · Arguments chiffrés · Suivi engagements |

---

## ⚠️ Formats acceptés par NotebookLM

| Format | Accepté ? | Action requise |
|---|---|---|
| PDF | ✅ Oui | Charger directement |
| Google Docs | ✅ Oui | Lier via Google Drive |
| Google Slides | ✅ Oui | Lier via Google Drive |
| URL web | ✅ Oui | Coller l'URL (HAS, CNSA, legifrance…) |
| YouTube | ✅ Oui | Coller l'URL |
| Audio (MP3/WAV) | ✅ Oui | Charger directement |
| DOCX / PPTX / Excel | ❌ Non natif | → Exporter en PDF via Office 365 avant import |

**Workflow de conversion Office 365 → PDF :**
1. Ouvrir le fichier (Word ou PowerPoint)
2. Fichier → Exporter → Créer un document PDF
3. Déposer dans `Sources_PDF/` du notebook concerné
4. Charger dans NotebookLM

---

## Types de documents utiles par notebook

### Sources externes (PDFs officiels)
- Recommandations RBPP HAS/ANESM (téléchargeables sur has-sante.fr)
- Référentiel évaluation HAS 2022
- Grilles d'évaluation officielles HAS
- Circulaires CNSA (SERAFIN-PH)
- Textes CASF (export legifrance.gouv.fr en PDF)

### Sources internes (à exporter en PDF)
- Procédures et protocoles de l'établissement
- Comptes-rendus de réunion (CVS, réunions d'équipe, CA)
- Fiches de poste AES / Moniteur-éducateur / Éducateur spécialisé
- Bilans d'activité et indicateurs CPOM
- Notes de cadrage et projets d'établissement

### Sources produites (veilles et synthèses)
- Veilles hebdomadaires (format .md → copier dans Google Docs ou exporter en PDF)
- Fiches synthèse RBPP
- Documents Word produits → exporter en PDF

---

## Workflow d'utilisation

```
1. Préparer les sources
   └── Convertir DOCX/PPTX → PDF via Office 365
   └── Déposer dans Sources_PDF/ du notebook concerné

2. Charger dans NotebookLM
   └── Nouveau notebook → Ajouter sources → Charger PDFs
   └── Ajouter les URLs web utiles (HAS, CNSA…)

3. Configurer le Notebook Guide
   └── Copier le contenu de Prompts/notebook_guide_[NOM].md
   └── Coller dans "Notebook Guide" (icône crayon ou paramètres)

4. Interroger
   └── Utiliser les requêtes types du guide comme base
   └── Préciser systématiquement : [Format souhaité] + [Destinataire]

5. Exploiter les outputs
   └── Copier dans Word pour finalisation
   └── Audio Overview → podcasts synthèse pour l'équipe
```

---

## Limites NotebookLM à connaître

- Max **50 sources** par notebook → prévoir une sélection rigoureuse par thème
- Max **~500 000 mots** par source → les très gros PDF peuvent poser problème
- **Pas de mémoire entre sessions** : le Notebook Guide est la seule persistance
- **Audio Overview en anglais par défaut** → préciser "en français" dans le Notebook Guide
- **Pas d'accès internet en temps réel** → les sources sont la seule base de connaissance ; mettre à jour manuellement

---

## Arborescence locale

```
NotebookLM/
├── README.md                              ← ce fichier
├── RBPP/
│   ├── Sources_PDF/                       ← PDFs à charger dans NotebookLM
│   └── Prompts/
│       └── notebook_guide_RBPP.md
├── Evaluation_HAS/
│   ├── Sources_PDF/
│   └── Prompts/
│       └── notebook_guide_Evaluation_HAS.md
├── SERAFIN-PH/
│   ├── Sources_PDF/
│   └── Prompts/
│       └── notebook_guide_SERAFIN-PH.md
├── Formation_Equipe/
│   ├── Sources_PDF/
│   └── Prompts/
│       └── notebook_guide_Formation_Equipe.md
└── CPOM/
    ├── Sources_PDF/
    └── Prompts/
        └── notebook_guide_CPOM.md
```
