# ✅ Check-list — Bien rédiger un prompt
# Générique · Tous sujets · Tous LLMs

---

## BLOC 1 — AVANT DE RÉDIGER

- [ ] J'ai formulé ma demande en une phrase claire (sujet + verbe + résultat attendu)
- [ ] J'ai identifié le destinataire final du livrable (moi / équipe / direction / autre)
- [ ] J'ai choisi le format de sortie attendu (liste / tableau / texte structuré / code / autre)
- [ ] J'ai listé les contraintes non négociables (budget / délai / longueur / registre)
- [ ] J'ai vérifié que ma demande ne mélange pas plusieurs objectifs distincts
  → Si oui : découper en plusieurs prompts séquentiels

---

## BLOC 2 — LE RÔLE

- [ ] J'ai assigné un rôle expert précis (pas "expert en X" générique)
  → ❌ "Tu es un expert en santé"
  → ✅ "Tu es un consultant RBPP HAS spécialisé en ESSMS handicap adulte"
- [ ] Le rôle est cohérent avec la demande (formateur ≠ juriste ≠ analyste)
- [ ] J'ai précisé le niveau de spécialisation attendu si pertinent
  → Ex : "niveau cadre intermédiaire médico-social, pas niveau chercheur universitaire"

---

## BLOC 3 — LE CONTEXTE

- [ ] J'ai fourni le contexte minimal nécessaire pour éviter les réponses génériques
  → Qui je suis · Où j'exerce · Pour qui je produis · Quelles contraintes terrain
- [ ] J'ai précisé les éléments hors-scope (ce que je ne veux PAS)
- [ ] Si le sujet est technique : j'ai indiqué le niveau de connaissance préalable supposé du lecteur

---

## BLOC 4 — L'ANCRAGE ET LES SOURCES

- [ ] J'ai indiqué si l'IA doit s'appuyer sur des sources précises
  → Ex : "Tes réponses s'appuient sur les RBPP HAS et le CASF uniquement"
- [ ] J'ai ajouté une règle anti-hallucination explicite
  → Ex : "Si tu n'as pas de source fiable, dis-le. Jamais de référence inventée."
- [ ] Si le sujet l'exige : j'ai demandé un niveau de fiabilité pour chaque affirmation
  → haute / moyenne / incertaine
- [ ] J'ai prévu une étape de vérification des sources (tour de relance dédié)

---

## BLOC 5 — LE FORMAT DE SORTIE

- [ ] J'ai précisé le format exact attendu
  → Liste à puces / tableau / titres H1-H2 / prose / code / fiche / autre
- [ ] J'ai indiqué la longueur approximative si importante
  → Ex : "1 page max" / "5 à 7 points" / "moins de 300 mots"
- [ ] J'ai précisé le registre (institutionnel / accessible / technique / pédagogique)
- [ ] J'ai interdit ce que je ne veux pas
  → Ex : "Pas de prose continue" / "Pas d'introduction généraliste" / "Pas de conclusion morale"

---

## BLOC 6 — LA CLARIFICATION PRÉALABLE

- [ ] J'ai demandé à l'IA de me poser des questions AVANT de produire
  → Ex : "Avant de commencer, pose-moi 3 à 5 questions ciblées"
- [ ] J'ai limité le nombre de questions pour éviter le tunnel d'interrogatoire
  → Entre 3 et 5 questions maximum
- [ ] Les questions portent sur : destinataire · format · contraintes · périmètre · sources

---

## BLOC 7 — LA QUALITÉ ET LA CRITIQUE

- [ ] J'ai intégré une étape de remise en question de la production
  → Ex : "Identifie 3 à 5 faiblesses de ce que tu viens de produire"
- [ ] J'ai demandé une version améliorée après la critique (pas juste un diagnostic)
- [ ] J'ai précisé les angles à challenger en priorité
  → Applicabilité terrain / Biais / Sources manquantes / Objections probables

---

## BLOC 8 — LA RÉUTILISABILITÉ (reverse engineering)

- [ ] À la fin du workflow, j'ai demandé le prompt parfait qui aurait produit ce résultat
  → Ex : "Génère le prompt autonome qui aurait produit ce résultat dès le départ"
- [ ] Ce prompt généré est : autonome · complet · compact · sans contexte externe requis
- [ ] Je l'ai sauvegardé pour réutilisation future

---

## BLOC 9 — VÉRIFICATION FINALE AVANT ENVOI

- [ ] Mon prompt tient en une lecture : pas besoin de le relire pour le comprendre
- [ ] Chaque instruction est actionnable (l'IA peut l'exécuter sans interprétation)
- [ ] Je n'ai pas utilisé de termes vagues : "pertinent", "intéressant", "complet", "bon"
  → Remplacer par des critères mesurables
- [ ] J'ai relu en me mettant à la place de l'IA : est-ce que je saurais exactement quoi faire ?
- [ ] Si le prompt dépasse 10 lignes : j'ai vérifié qu'il n'y a pas de contradictions internes

---

## ANTI-PATTERNS À ÉVITER

| ❌ À éviter | ✅ À faire à la place |
|---|---|
| "Fais-moi quelque chose sur X" | "Produis une fiche check-list sur X pour [destinataire]" |
| "Tu es un expert" (sans précision) | "Tu es un [rôle précis] spécialisé en [domaine exact]" |
| Demander tout en un seul prompt | Séquencer en tours : clarification → production → sources → critique |
| Oublier le destinataire | Toujours préciser pour qui est le livrable final |
| Accepter le premier résultat | Systématiquement demander critique + amélioration |
| Ne pas vérifier les sources | Toujours demander le sourçage avec niveau de fiabilité |
| Jeter le prompt après usage | Capturer le prompt reverse-engineered pour réutilisation |

---

## TEMPLATE MINIMAL (à compléter en 2 minutes)

```
Rôle      : Tu es [expert précis] spécialisé en [domaine].
Contexte  : [Qui je suis · Où j'exerce · Pour qui je produis]
Demande   : [Ce que je veux obtenir en 1 phrase]
Format    : [Liste / tableau / fiche / synthèse / autre] — [longueur max]
Destinataire : [Direction / Équipe / ARS / Familles / Autre]
Contraintes  : [Budget / Délai / Registre / Hors-scope]
Sources   : [Sources à mobiliser — Jamais de référence inventée]
Avant de commencer : pose-moi 3 à 5 questions ciblées.
```

---

*Référence workflow complet : `Prompts/workflow_5etapes_claudeai.md`*
