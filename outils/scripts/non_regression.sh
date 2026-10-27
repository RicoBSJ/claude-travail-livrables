#!/bin/zsh
# non_regression.sh — rejoue les contrôles communs sur le corpus du dépôt et compare au dernier passage accepté.
#
#   outils/scripts/non_regression.sh            passes A/A2/A3/A4 des attributions (sans aspiration, ~2 min) sur toutes les
#                                               leçons et veilles + décompte sur les 85 veilles + les 14 témoins
#                                               d'avant correction (qui doivent sortir en 1) ; diff avec la référence.
#   outils/scripts/non_regression.sh --complet  ajoute le contrôle d'attributions COMPLET (avec aspiration) sur les
#                                               trois témoins à citations (doivent sortir en 0) et sur les témoins
#                                               d'avant correction de non_regression/temoins_attributions_avant_correction/
#                                               (doivent sortir en 1) — long, dépend du réseau : un exit 3 est
#                                               retenté une fois après NR_ATTENTE s (60), puis affiché, jamais refusé.
#   outils/scripts/non_regression.sh --accepter enregistre le passage courant comme nouvelle référence, APRÈS avoir
#                                               lu le diff et compris chaque changement de verdict.
#   outils/scripts/non_regression.sh --docs f…  mode DOCUMENTS (quelques secondes) : pour chaque .docx donné, passes
#                                               A/A2/A3/A4 et, pour une veille, décompte ; comparé à la référence du
#                                               document — un document ne doit pas régresser, un document nouveau doit
#                                               être à 0 bloquant. C'est ce que le hook lance quand un push touche des
#                                               livrables ou des veilles (les jobs publient par là).
#
# Sort en 0 si aucun verdict n'a changé, en 1 sinon (ou si un témoin ne sort plus en 1). Les documents nouveaux
# depuis la référence sont signalés, pas comparés : un job qui publie ne crée pas une régression.
# Hook : outils/scripts/hooks/pre-push lance ce script avant tout push qui touche un contrôle commun
# (installation : git config core.hooksPath outils/scripts/hooks).
# Règle (JOBS.md, 12/09/2026) : toute retouche de controle_attributions.py ou controle_decompte.py se rejoue ici,
# dans les deux sens, et le diff des verdicts se lit — pas seulement le décompte. Dix-huit défauts ont été trouvés
# en rejouant, aucun en relisant.
set -u
ROOT="/Users/utilisateur/kDrive/Claude_Travail"
NR="$ROOT/outils/scripts/non_regression"
REF="$NR/reference"
CUR="$NR/courant"
PY=/usr/bin/python3
mkdir -p "$CUR"
MODE="${1:-}"

# ── ORTHOGRAPHE DES CONSIGNATIONS (27/10/2026). J'ai écrit « kDrib » pour « kDrive » dans
#    JOBS.md, et c'est un `grep -c` qui l'a attrapé, pas ma relecture : rien ne contrôlait
#    l'orthographe des deux fichiers sur lesquels on s'appuiera dans six mois. Le contrôle ne
#    juge QUE les noms techniques (ils ne se déclinent pas) et prend le corpus pour
#    dictionnaire ; ses bornes et les quatre sources de bruit mesurées sont dans son en-tête.
#    Défini en FONCTION parce qu'il est appelé à DEUX endroits — le mode rapide ci-dessous et
#    la position « tous les modes » plus bas — et qu'une logique copiée ne garde rien (15/10).
bloc_orthographe () {
  local OUT="$CUR/orthographe.txt" CORP="$CUR/orthographe_corpus.txt" ORTH_KO=0 LU
  local ATTENDU_ORTH=12        # le lot de bornes du contrôle ; le garde lit le DÉNOMINATEUR
  echo "▶ Orthographe des consignations — un nom technique mal écrit (aucun réseau, 0,7 s)"
  if env -i $PY "$ROOT/outils/scripts/controle_orthographe.py" --autotest > "$OUT" 2>&1; then
    tail -1 "$OUT"
    LU=$(sed -n 's/.* [0-9]\{1,\}\/\([0-9]\{1,\}\) bornes de l.orthographe.*/\1/p' "$OUT")
    if [ "${LU:-0}" != "$ATTENDU_ORTH" ]; then
      echo "  ✗ ${LU:-0} borne(s) jouée(s), $ATTENDU_ORTH attendue(s) — un lot amputé ne prouve rien :"
      echo "    rétablis la borne retirée, ou mets ATTENDU_ORTH à jour en disant pourquoi."
      ORTH_KO=1
    fi
  else
    grep '✗' "$OUT" | head -6
    echo "  ✗ LE CONTRÔLE D'ORTHOGRAPHE NE TIENT PLUS SES BORNES — soit il ne voit plus la"
    echo "    coquille de l'incident (kDrib ~ kDrive, distance 2), soit il s'est élargi et"
    echo "    accuse la morphologie française ou un mot mis en capitales. Les deux sens sont ici."
    ORTH_KO=1
  fi
  if env -i $PY "$ROOT/outils/scripts/controle_orthographe.py" > "$CORP" 2>&1; then
    grep 'ZONE MORTE' "$CORP" | sed 's/^/  ⚠ /'    # non bloquant, mais LU : une alerte qu'on n'imprime pas n'existe pas (26/10)
    tail -1 "$CORP"
  else
    cat "$CORP"
    echo "  ✗ UNE CONSIGNATION PORTE UN NOM TECHNIQUE MAL ÉCRIT — la ligne est donnée ci-dessus."
    echo "    Corrige le mot, ou, si ce nom est légitime, écris-le au moins 5 fois ou explique"
    echo "    ici pourquoi la borne doit bouger."
    ORTH_KO=1
  fi
  return $ORTH_KO
}

# ── mode --consignes : ce que le hook lance quand un push ne touche QUE les consignations.
#    Sans lui, ce push ne déclenchait AUCUN mode — mesuré le 27/10 — donc le contrôle n'aurait
#    jamais tourné sur elles et serait resté décoratif, le défaut même corrigé la veille.
if [ "$MODE" = "--consignes" ]; then
  bloc_orthographe; exit $?
fi

# ── DÉSARMEMENT DE L'ENVIRONNEMENT GIT (27/10/2026). `git push` exporte GIT_DIR à ses hooks, et
#    depuis que `.git` est un fichier d'une ligne hors de l'arbre ce chemin est ABSOLU : un `cd`
#    n'isole plus rien. Trois fichiers du dépôt appellent `git` sous un hook — run_job.sh,
#    non_regression_runner.sh et le hook lui-même — et portent depuis un `unset` des huit variables.
# 🔴 POURQUOI UNE BORNE DE PRÉSENCE, ET NON UN TÉMOIN D'EFFET : aucun témoin du dépôt ne peut
#    exercer un désarmement dans le sens conforme. MESURÉ, pas raisonné — aucun script du dépôt ne
#    POSE GIT_DIR (le `GIT_SSH_COMMAND` excepté), donc le harnais lance toujours ses témoins dans
#    un environnement déjà propre, où retirer les trois `unset` ne change RIEN. Seul le lancement
#    DEPUIS LE HOOK les exerce, et ce lancement n'est pas un témoin. On ne peut pas prouver l'effet,
#    on exige donc la ligne — et surtout qu'elle soit PREMIÈRE : le 27/10 le `unset` du hook était
#    posé APRÈS `ROOT="$(git rev-parse …)"`, et le hook refusait le push en annonçant « un verdict
#    a changé », motif FAUX. Une borne de présence seule aurait déclaré ce fichier conforme.
#    Même type de garde que le ② de l'assertion de tableau (18/10) : exiger le littéral.
bloc_desarmement () {
  local OUT="$CUR/desarmement_git.txt" DES_KO=0 LU
  local ATTENDU_DES=13         # le garde lit le DÉNOMINATEUR, jamais le nombre de réussies (26/10)
  echo "▶ Désarmement de l'environnement git — la ligne est-elle là, et PREMIÈRE ? (aucun réseau, 0,1 s)"
  if env -i $PY "$ROOT/outils/scripts/non_regression/desarmement_git.py" > "$OUT" 2>&1; then
    tail -1 "$OUT"
    LU=$(sed -n 's/.* [0-9]\{1,\}\/\([0-9]\{1,\}\) bornes du désarmement.*/\1/p' "$OUT")
    if [ "${LU:-0}" != "$ATTENDU_DES" ]; then
      echo "  ✗ ${LU:-0} borne(s) jouée(s), $ATTENDU_DES attendue(s) — un lot amputé ne prouve rien :"
      echo "    rétablis la borne retirée, ou mets ATTENDU_DES à jour en disant pourquoi."
      DES_KO=1
    fi
  else
    grep '✗' "$OUT" | head -6
    echo "  ✗ UN DES TROIS SCRIPTS NE DÉSARME PLUS L'ENVIRONNEMENT GIT, OU LE FAIT TROP TARD."
    echo "    Conséquence mesurée le 27/10 : le dépôt jetable du runner a résolu vers LE VRAI"
    echo "    DÉPÔT, qui est passé en core.bare=true pendant un push. Rétablis le `unset` des"
    echo "    huit variables AVANT le premier appel à git, ou dis ici pourquoi la borne bouge."
    DES_KO=1
  fi
  return $DES_KO
}

# ── mode --desarmement : ce que le hook lance quand un push touche run_job.sh ou le runner,
#    qui ne sont PAS dans SURVEILLES et ne déclenchent donc que les mutations du runner —
#    lesquelles tournent sans GIT_DIR, et ne voient rien. Même raison que --consignes la veille.
if [ "$MODE" = "--desarmement" ]; then
  bloc_desarmement; exit $?
fi

# Effectif ATTENDU de chaque lot de témoins (23/09/2026). Les trois boucles de témoins contrôlaient ce
# qu'elles trouvaient et annonçaient un total ÉCRIT EN DUR : « ✓ 14/14 en exit 1 » s'imprimait quel que
# soit le nombre de fichiers réellement passés. Le 23/09, pendant un test du hook, un témoin avait quitté
# son dossier et le script annonçait toujours 14/14. Pire : zsh saute une boucle dont le motif ne matche
# rien (« no matches found »), donc un lot VIDÉ — dossier supprimé, fichiers renommés, glob d'un document
# vivant qui ne matche plus après un rangement — faisait passer le contrôle sans en exécuter une ligne.
# Désormais chaque lot déclare son effectif ici, le script compte ce qu'il a réellement contrôlé, et TOUT
# écart refuse. Ajouter ou retirer un témoin, c'est mettre à jour le nombre correspondant ci-dessous.
# Les trois boucles portent le qualificateur zsh (N) : sans lui, un lot VIDE fait mourir le script sur
# « no matches found » avant même le diff des verdicts — refus, mais sans message lisible. Avec (N), le
# motif vide rend zéro fichier, le compteur reste à 0 et le contrôle ci-dessous dit ce qui manque.
ATTENDU_DECOMPTE=15   # temoins_decompte_avant_correction/ — 15 depuis le 02/10/2026 :
                      #   + ai-act/2026-10-02 TELLE QUE LIVRÉE (en-tête 8 sources, corps 9)
ATTENDU_DEC_CONFORMES=3  # temoins_decompte_conformes/ — doivent sortir en 0.
                      # ⚠️ POURQUOI CE LOT EXISTE (02/10/2026). Un témoin « d'avant correction » ne
                      # prouve que la MORSURE, jamais la JUSTESSE : la veille ai-act du 02/10 telle que
                      # livrée sort en 1 avec le contrôle bogué COMME avec le contrôle corrigé — elle ne
                      # discrimine rien. Ce qui discrimine, c'est sa version CORRIGÉE : exit 1 avec
                      # l'ancien contrôle (qui perdait une entrée sur les listes mêlant « ✅ Nom » et
                      # « Consultée… : Nom »), exit 0 avec le contrôle corrigé. Sans ce lot, rien dans ce
                      # harnais n'empêche de ramener le décalage d'appariement.
                      # ⚠️ TROIS FORMES DE LISTE, TROIS TÉMOINS — matrice mesurée le 02/10/2026 contre
                      # trois mutations du contrôle (copies jetables, jamais commitées) :
                      #   m1 = « Consultée… » classée avant le test du deux-points (ma 1re tentative de
                      #        correctif, qui réparait le 02/10 et cassait trois autres notes)
                      #   m2 = fermeture de groupe retirée (le défaut réellement corrigé le 02/10)
                      #   m3 = marqueurs de correction en ligne non retirés
                      #   ┌──────────────────────────────┬──────┬──────┬──────┬──────┐
                      #   │ témoin (doit sortir en 0)    │ sain │  m1  │  m2  │  m3  │
                      #   ├──────────────────────────────┼──────┼──────┼──────┼──────┤
                      #   │ ai-act 2026-10-02            │  0   │  0   │  1   │  1   │
                      #   │ ai-act 2026-09-18            │  0   │  1   │  0   │  0   │
                      #   │ imac   2026-08-30            │  0   │  1   │  0   │  0   │
                      #   └──────────────────────────────┴──────┴──────┴──────┴──────┘
                      # Chaque mutation est attrapée par au moins un témoin, et AUCUN témoin ne les
                      # attrape toutes : retirer l'un des trois rend une des trois mutations invisible.
                      # ⚠️ Le témoin du 02/10 ne couvre m3 que parce que son marqueur de correction cite
                      # le décompte d'origine EN CHIFFRES. Il avait d'abord été écrit en lettres pour
                      # contourner le bug m3 ; ce contournement le rendait aveugle à sa propre correction.
                      # Un marqueur qui cite fidèlement est donc aussi ce qui rend le test possible.
ATTENDU_CONFORMES=11  # 3 documents vivants (stoïcisme 14, appli-ia 07, placement 14) + temoins_attributions_conformes/ (8 copies figées)
                      # 11 depuis le 15/10/2026 : 2026-06-25_lecon-stoicisme_04_courbes.docx entre pour ㊱,
                      # les guillemets COURBES “ ” — c'est le SEUL document des 283 dont des citations de
                      # six mots ou plus tombaient hors de toute capture. Recensement complet, pas échantillon.
                      # 10 depuis le 11/10/2026 : 2026-10-01_lecon-astrologie-karmique_09_locale.docx entre pour
                      # garder ㉟ (un nombre français écrit à l'anglaise sur la page citée). ⚠️ CE TÉMOIN SORT EN 3,
                      # durablement : deux de ses citations sont sur des pages que le contrôle ne peut pas lire. Ce
                      # n'est pas son code de sortie qui prouve quelque chose, c'est sa LIGNE — comme pour ㉜.
                      # 9 depuis le 11/10/2026 : 2026-06-10_lecon-enneagramme_02_declaree.docx entre pour garder
                      # l'EXEMPTION de ㉞ — un lien dont le document declare qu'il ne resout pas n'est pas une faute.
                      # 8 depuis le 10/10/2026 : 2026-10-10_lecon-placement-financier_18_passeD.docx entre
                      # pour garder la PASSE D, qui n'est pas dans la référence et qu'aucun verdict ne protège.
                      # 4e copie figée le 09/10/2026 : la leçon Ennéagramme n°06 APRÈS correction, témoin de
                      # l'exemption de ㉜ — ses quatre citations d'ouvrages y sont DÉCLARÉES reformulations,
                      # et elle doit donc sortir en 0 SANS aucune ligne « SOURCE NOMMÉE SANS PAGE ». C'est le
                      # seul témoin qui garde la déclaration : si la détection devenait aveugle aux mots
                      # « reformulation / non consulté / d'après », il refuserait un document juste.
                      # 3e copie figée le 27/09/2026 : appli-ia n°10, témoin de ㉛ — deux requêtes SQL de son
                      # exercice (« SELECT COUNT(*) as n FROM livrables WHERE slug LIKE @m ») étaient lues comme
                      # des citations anglaises et bloquaient un document juste. Elle doit sortir en 0.
#   5 depuis le 26/09/2026 : la leçon placement-financier n°03 AVEC SES MARQUEURS DE CORRECTION
#   GUILLEMETÉS est entrée dans le lot. C'est le seul témoin qui garde l'exemption des marqueurs
#   dans les passes B, B-FR et B-NOM : il DOIT sortir en 0, et il sortait en 1 avant le correctif
#   du 26/09 (mesuré dans les deux sens). Si une formulation citée pour mémoire redevient un jour
#   une attribution, c'est lui qui le dira — aucun autre témoin conforme ne porte de marqueur.
ATTENDU_AVANT=9       # temoins_attributions_avant_correction/ — 9 depuis le 11/10/2026 :
                      # 2026-06-10_lecon-enneagramme_02_avant.docx entre pour garder ㉞ (un nom de domaine
                      # qui ne resout pas est un lien mort). C'est le SEUL des 394 hotes du depot dans ce cas.
#   la leçon Ennéagramme n°06 d'AVANT sa correction est entrée dans le lot ce jour-là. C'est le SEUL
#   témoin qui exerce la passe ㉜ : elle citait QUATRE ouvrages entre guillemets, en français, sans
#   qu'aucun texte ait été ouvert, et le contrôle n'en signalait qu'UN comme bloquant — le seul à côté
#   duquel un domaine était nommé. Les trois autres désignaient un LIVRE, et ㉖ ne déclenche que sur un
#   domaine. Ce témoin doit sortir en 1 (pour la citation de Palmer, via ㉖) ET porter au moins une
#   ligne « SOURCE NOMMÉE SANS PAGE » (via ㉜). Le code de sortie seul ne prouverait rien : il sortirait
#   en 1 sur la seule citation de Palmer même si ㉜ perdait toute sa dent.
#   7 depuis le 25/09/2026 :
#   la leçon appli-ia n°05 d'avant le 11/09 (commit 4ed6de0) est entrée dans le lot ce jour-là.
#   C'est le SEUL témoin qui exerce la passe C2 : « Vite v8.2.2 — vérifiée sur vite.dev/guide/
#   le 28/08/2026 » alors que la page ne l'a jamais portée. Les six autres témoins exercent B,
#   B-NOM et A6 ; le sens REFUS de C2 n'avait aucun témoin permanent, et la branche a été
#   retouchée deux fois le 25/09/2026 (acquittement de la dérive déclarée, et retrait du repli
#   qui cherchait le numéro de remplacement dans toute la fenêtre).

# ── 0 bis. AUTO-TESTS DE chercher.py — DANS TOUS LES MODES, --docs COMPRIS (15/10/2026)
# `chercher.py` n'est pas un contrôle de publication : c'est l'outil par lequel Claude vérifie
# qu'une citation, un chiffre ou une date figure bien sur une page aspirée, SANS que la page
# entre dans son contexte. Il ne peut donc pas être gardé par un témoin .docx ni par la
# référence. Mais ses bornes sont exactement celles que le dépôt a déjà payées cher :
#   • le « \? » devant la classe d'espaces — bug de la passe D réparé le 10/10/2026, reproduit
#     à l'identique à l'écriture de chercher.py le 15/10 (nombres présents donnés pour absents) ;
#   • le point JAMAIS séparateur de milliers — borne de ㉟ du 11/10, deux faux appariements
#     mesurés (« 7 918 » dans le « 7.918 » de doi.org, « 1 049 » dans le « 1.049 » d'apple.com) ;
#   • un jeton se cherche ponctuation CONSERVÉE — borne du 12/10 ;
#   • et le degré ④ doit MONTRER ce que la page écrit à la place, règle du 14/10 née de quatre
#     quasi-fausses accusations en deux jours.
# 21 auto-tests, 0,1 s, AUCUN appel réseau — donc il tourne même à la porte des pushs de job.
# Les neuf mutations qui les prennent en défaut sont dans le docstring de chercher.py.
if [ -x "$ROOT/outils/scripts/chercher.py" ]; then
  echo "▶ Auto-tests de chercher.py (appariement exact, aucun réseau)"
  # ⚠ PAS de pipe ici. La première écriture était « ... --autotest | tail -1 », qui teste le
  # code de sortie de TAIL : le sabotage s'affichait et le harnais sortait en 0 quand même.
  # Mesuré le 15/10/2026 à la pose du garde. Un garde qui ne fait pas sortir en 1 est décoratif.
  CH_OUT="$CUR/chercher_autotest.txt"
  if env -i $PY "$ROOT/outils/scripts/chercher.py" --autotest > "$CH_OUT" 2>&1; then
    tail -1 "$CH_OUT"
  else
    grep '✗' "$CH_OUT" | head -5
    echo "  ✗ chercher.py A PERDU UNE BORNE — un « ABSENT » de cet outil ne vaut plus rien"
    exit 1
  fi
fi

# ── 0 ter. AUTO-TESTS DE lire_page.py — DANS TOUS LES MODES (19/10/2026)
# Même nature que chercher.py : ce n'est pas un contrôle de publication, c'est l'outil par lequel
# une page aspirée est lue SANS entrer entière en contexte. Il est né d'une erreur mesurée : le
# prompt de rbpp-pipeline avait reçu le 18/10 la consigne « lis ce .txt (sed -n, grep -n) », qui
# est INAPPLICABLE — aspirer.py écrase tous les blancs, donc une page aspirée est UNE SEULE LIGNE
# (mesuré : 0 saut de ligne, 46 869 caractères pour le flux HAS-Actualité). sed -n rendait le
# fichier entier et grep -n la ligne entière. Le créneau suivant est passé de 59 % à 93 % du
# plafond, de 47 à 72 tours, avec 2,4 fois plus de cache lu.
# SA BORNE EST STRUCTURELLE, et l'auto-test ① la vérifie : la sortie est strictement plus petite
# que la page. Les sept bornes couvrent aussi le pliage casse/accents, le plafond d'occurrences
# qui ANNONCE son reste, le renvoi à chercher.py sur une absence, et la lecture du .brut d'un
# flux RSS (CDATA, pubDate, --depuis).
# ⚠ PAS de pipe : la leçon du 15/10 vaut ici aussi — « ... --autotest | tail -1 » testerait le
#   code de sortie de tail, et le sabotage s'afficherait sans faire sortir en 1.
if [ -x "$ROOT/outils/scripts/lire_page.py" ]; then
  echo "▶ Auto-tests de lire_page.py (lecture bornée, aucun réseau)"
  LP_OUT="$CUR/lire_page_autotest.txt"
  if env -i $PY "$ROOT/outils/scripts/lire_page.py" --autotest > "$LP_OUT" 2>&1; then
    tail -1 "$LP_OUT"
  else
    grep '✗' "$LP_OUT" | head -5
    echo "  ✗ lire_page.py A PERDU UNE BORNE — une page aspirée pourrait entrer entière en contexte"
    exit 1
  fi
fi

# ── 0 quater. AUTO-TESTS DU DÉCOMPTE DES LIENS (㊳ bis, 20/10/2026)
# Les neuf prompts doivent écrire « 🔗 Liens : N testés · X retenus · Y écartés (codes : …) » dans
# leur récapitulatif, et controle_livrable_du_job.py relève cette ligne dans le log du run pour
# signaler tout 000. Le motif doit tolérer ce qu'un récapitulatif écrit vraiment — accents absents,
# tirets au lieu des points médians — ET refuser la prose : « liens testés et morts », la phrase
# que controle-livrables porte depuis toujours, ne doit PAS être lue comme un décompte, sinon le
# contrôle inventerait des nombres. Six bornes, aucun réseau, aucun fichier.
if [ -x "$ROOT/outils/scripts/controle_livrable_du_job.py" ]; then
  echo "▶ Auto-tests du décompte des liens (㊳ bis, aucun réseau)"
  LD_OUT="$CUR/liens_autotest.txt"
  if env -i $PY "$ROOT/outils/scripts/controle_livrable_du_job.py" --autotest > "$LD_OUT" 2>&1; then
    tail -1 "$LD_OUT"
    # 🔴 24/10/2026 — UN LOT AMPUTÉ PASSAIT AU VERT. Le bloc ne lisait que le code de sortie :
    #    retirer un témoin faisait imprimer « ✓ 2/2 » et le harnais était content. Le motif vient
    #    d'être ÉLARGI (champ verbeux, gras Markdown) et la règle du 15/10 veut qu'un motif
    #    desserré garde un témoin qui doit être ACCEPTÉ — sans compte attendu, rien n'empêcherait
    #    de le resserrer demain en supprimant ce témoin. Même garde que ATTENDU_5BIS.
    ATTENDU_LIENS=12
    LU_LIENS=$(sed -n 's/.* [0-9]\{1,\}\/\([0-9]\{1,\}\) bornes du décompte des liens.*/\1/p' "$LD_OUT")
    if [ "$LU_LIENS" != "$ATTENDU_LIENS" ]; then
      echo "  ✗ ${LU_LIENS:-0} borne(s) de décompte jouée(s), $ATTENDU_LIENS attendue(s) — un lot"
      echo "    amputé passerait au vert, et le motif élargi le 24/10 pourrait être resserré sans bruit"
      exit 1
    fi
  else
    grep '✗' "$LD_OUT" | head -5
    echo "  ✗ LE DÉCOMPTE DES LIENS A PERDU UNE BORNE — un 000 redeviendrait invisible"
    exit 1
  fi
fi

# ── 0 quinquies. LA TABLE DOSSIER → JOB VOIT-ELLE LES JOBS SUPPRIMÉS ? (24/10/2026)
# ㊳ lie un livrable au run qui l'a produit par le DOSSIER de ce livrable. Cette table venait de
# jobs_config.json seule, donc SUPPRIMER UN JOB rendait ses livrables invisibles — pas refusés,
# INVISIBLES : sortie vide, exit 0, ligne 🔗 disparue. 135 des 294 .docx du dépôt vivent dans un
# dossier sans job, et comme un job supprimé ne produit plus rien de neuf, le trou ne mordait que
# sur un document CORRIGÉ : corriger une leçon d'un parcours clos contournait ㊳ en entier.
# ⚠️ TOUT EST FABRIQUÉ ICI, RIEN DE VIVANT — la leçon du 22/10, où un témoin ancré sur
#    l'avancement réel d'un parcours a bloqué TOUS les pushs du dépôt le jour où le bilan est
#    sorti. Le nombre de jobs supprimés dont il reste un log est VOLATILE : run_job.sh purge les
#    logs à 30 jours. Un compte attendu sur l'arborescence réelle périmerait donc tout seul.
# Les deux sens, et les deux pièges : un dossier sans log ne doit RIEN se voir attribuer (sinon la
# table invente un job), et la config doit GAGNER même quand un log porte le nom qu'on déduirait
# — sans quoi « has-actualite » repasserait de rbpp-pipeline à un « has-actualite-veille » qui
# n'existe pas, ce qui défairait la correction du 20/10. Aucun réseau, aucun document, 0,1 s.
if [ -x "$ROOT/outils/scripts/controle_livrable_du_job.py" ]; then
  echo "▶ Témoin de la table dossier → job (arborescence fabriquée, aucun job réel)"
  FX="$CUR/table_fixture"
  rm -rf "$FX"
  mkdir -p "$FX/livrables/lecons/dzogchen" "$FX/livrables/lecons/entretien-motivationnel" \
           "$FX/livrables/lecons/nocode-ia" "$FX/sources/veille/has-actualite" "$FX/logs"
  cat > "$FX/jobs_config.json" <<'JSON'
{"jobs": [{"id": "rbpp-pipeline",
           "livrable": "sources/veille/rbpp/ + sources/veille/has-actualite/"}]}
JSON
  : > "$FX/logs/dzogchen-lecon_20261013_080300.log"
  : > "$FX/logs/nocode-ia-veille_20260801_080300.log"
  : > "$FX/logs/has-actualite-veille_20261024_000000.log"   # LE PIÈGE : la config doit gagner
  TB="$CUR/table.txt"
  env -i $PY "$ROOT/outils/scripts/controle_livrable_du_job.py" --table "$FX" "$FX/logs" \
      > "$TB" 2>&1
  TB_KO=0
  exige_table() {   # $1 = motif attendu, $2 = ce qu'il garde
    if grep -qE "$1" "$TB"; then echo "  ✓ $2"; else
      echo "  ✗ $2"; echo "    ligne absente de --table : $1"; TB_KO=1; fi
  }
  exige_table 'supprimé +dzogchen +→ dzogchen-lecon +\(1 log' \
    "un dossier de job SUPPRIMÉ est attribué dès qu'un log porte son id"
  exige_table 'supprimé +nocode-ia +→ nocode-ia-veille' \
    "les deux suffixes sont essayés — un dossier de leçons servi par un id en « -veille »"
  exige_table 'config +has-actualite +→ rbpp-pipeline' \
    "la config GAGNE sur la déduction, même quand un log porte le nom déduit (20/10 intact)"
  exige_table '○ entretien-motivationnel : aucun log' \
    "un dossier sans aucun log ne se voit RIEN attribuer — la table n'invente pas de job"
  if grep -qE 'supprimé +has-actualite' "$TB"; then
    echo "  ✗ « has-actualite » est passé à un job DÉDUIT — la correction du 20/10 est défaite"
    TB_KO=1
  fi
  exige_table 'table : 4 dossier\(s\) attribué\(s\) — 2 de la config, 2 de job\(s\) supprimé\(s\), 1 hors de portée' \
    "le décompte de la table : un dossier perdu en silence ne passerait pas au vert"
  if [ "$TB_KO" = 1 ]; then
    echo "  ✗ LA TABLE DOSSIER → JOB A PERDU UNE BORNE — un livrable corrigé pourrait repasser"
    echo "    sous ㊳ sans être vu, et le contrôle ne dirait RIEN plutôt que de refuser"
    exit 1
  fi
fi

# ---- Intégrité des .pptx du dépôt (17/10/2026) ----
# Le contrôle de volume posé le 17/10 dans les neuf prompts ne regarde que les .docx. Or
# `rbpp-pipeline` produit aussi des quiz et des infographies PowerPoint, et ses deux règles
# critiques — dimensions négatives, géométrie elliptique — existent parce qu'elles venaient
# de bugs rendant le fichier INOUVRABLE par PowerPoint. Un .pptx vide passerait exactement
# comme la veille du 17/10 est passée : les fichiers sont auto-committés et poussés.
# ⚠️ ET LA VÉRIFICATION D'ORIGINE NE REGARDAIT QU'UNE DIAPOSITIVE : la forme
#    « unzip -p … ppt/slides/slide1.xml | grep -o '<a:ext cx="-' » ne voyait que slide1.xml,
#    alors qu'un quiz en porte deux cents.
# BORNES MESURÉES SUR LES 56 .pptx DU DÉPÔT ET LEURS 3 917 DIAPOSITIVES : zéro diapositive
# sans texte, zéro dimension négative, minimum 92,8 caractères par diapositive (médiane
# 753,8). Les deux assertions ont donc ZÉRO faux positif sur l'existant. 1,5 s, sans réseau.
if [ -d "$ROOT/livrables/quiz" ]; then
  PX_OUT="$CUR/pptx_integrite.txt"
  env -i $PY - "$ROOT" > "$PX_OUT" 2>&1 <<'PYPX'
import glob, re, sys, zipfile
racine = sys.argv[1]
ko = []
fs = sorted(glob.glob(racine + "/livrables/quiz/*.pptx")
            + glob.glob(racine + "/livrables/infographies/*.pptx"))
for f in fs:
    nom = f.split("/")[-1]
    try:
        z = zipfile.ZipFile(f)
        sl = sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
                    key=lambda t: int(re.search(r"\d+", t.split("/")[-1]).group()))
        if not sl:
            ko.append("%s : AUCUNE DIAPOSITIVE" % nom); continue
        for n in sl:
            x = z.read(n).decode("utf-8", "replace")
            if not "".join(re.findall(r"<a:t>([^<]*)</a:t>", x)).strip():
                ko.append("%s : DIAPOSITIVE SANS TEXTE (%s)" % (nom, n.split("/")[-1])); break
            if re.search(r'<a:ext cx="-|<a:ext[^>]*cy="-', x):
                ko.append("%s : DIMENSION NEGATIVE (%s)" % (nom, n.split("/")[-1])); break
            # règle critique 2 : géométrie des pétales. ⚠️ TROIS FILTRES INDISPENSABLES,
            # chacun mesuré le 17/10/2026 : on ne garde que roundRect/ellipse (les
            # connecteurs radiaux ont la MÊME taille qu'un pétale et le chevauchent par
            # construction), on dédoublonne par position (chaque pétale est DEUX formes,
            # le visuel et son libellé), et on ne regarde que les pétales (titre et
            # colonnes de fond occupent légitimement les bandes haute et basse).
            pet = set()
            for mm in re.finditer(r"<p:sp>.*?</p:sp>", x, re.S):
                q = mm.group(0)
                gg = re.search(r'<a:prstGeom prst="([^"]+)"', q)
                if not gg or gg.group(1) not in ("roundRect", "ellipse"): continue
                oo = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"\s*/>\s*<a:ext cx="(\d+)" cy="(\d+)"', q)
                if not oo: continue
                ox, oy, cx, cy = (int(v)/914400.0 for v in oo.groups())
                if abs(cx-2.40) <= 0.36 and abs(cy-1.30) <= 0.195:
                    pet.add((round(ox,3), round(oy,3), round(cx,3), round(cy,3)))
            pet = sorted(pet); stop = False
            for (ox, oy, cx, cy) in pet:
                if oy < 1.19 or oy + cy > 7.01:
                    ko.append("%s : PETALE HORS ZONE (%s) y %.2f->%.2f"
                              % (nom, n.split("/")[-1], oy, oy+cy)); stop = True; break
            if stop: break
            for i2 in range(len(pet)):
                for j2 in range(i2+1, len(pet)):
                    ax, ay, aw, ah = pet[i2]; bx, by, bw, bh = pet[j2]
                    dx = min(ax+aw, bx+bw) - max(ax, bx); dy = min(ay+ah, by+bh) - max(ay, by)
                    if dx > 0.10 and dy > 0.10:
                        ko.append("%s : PETALES QUI SE CHEVAUCHENT (%s) %.2f x %.2f"
                                  % (nom, n.split("/")[-1], dx, dy)); stop = True; break
                if stop: break
            if stop: break
    except Exception as e:
        ko.append("%s : ILLISIBLE (%s)" % (nom, e))
if ko:
    print("\n".join(ko))
else:
    print("__OK__ %d" % len(fs))
PYPX
  if grep -q "^__OK__" "$PX_OUT"; then
    echo "  ✓ $(sed 's/__OK__ //' "$PX_OUT") .pptx intègres : texte présent, dimensions positives, géométrie des pétales conforme"
  else
    echo "▶ Intégrité des .pptx — DÉFAUT(S)"
    sed 's/^/     /' "$PX_OUT"
    echo "  ✗ un .pptx sans texte ou à dimension négative est inouvrable ou vide, et il"
    echo "    serait auto-committé comme un succès. Voir outils/templates/REGLES_PPTX.md."
    exit 1
  fi
fi

# ---- Les prompts prescrivent « children: », pas « run: » (17/10/2026) ----
# Le 17/10/2026, un lancement manuel d'ai-act a suivi À LA LETTRE la consigne de son prompt,
# « Construire chaque Paragraph avec la propriété run: new TextRun({...}) ». Cette propriété
# est SILENCIEUSEMENT IGNORÉE par la version de docx installée : le .docx produit était un
# XML VALIDE de 11,4 Ko, portait ses 10 hyperliens, PASSAIT le contrôle d'intégrité que le
# prompt lui-même impose — et ne contenait que 2 088 caractères, les seules lignes de liens.
# Mesure isolée : « run: » rend une chaîne vide, « children: » et « text: » rendent le texte.
# ⚠️ AUCUN LIVRABLE DU DÉPÔT N'EN A ÉTÉ ABÎMÉ (298 documents balayés, les sept plus courts
#    vérifiés un par un : de vraies notes brèves). Le piège était LATENT.
# ⚠️ ET RIEN NE SURVEILLAIT LES PROMPTS : jobs_config.json n'était dans aucun déclencheur du
#    hook. Il est désormais dans SURVEILLES.
#
# 🔴 L'ASSERTION EST POSITIVE, ET LA PREMIÈRE VERSION ÉTAIT NÉGATIVE — ELLE S'EST MORDUE.
#    Elle cherchait « run: new TextRun » hors d'un « PAS « », et mon propre commentaire du
#    contrôle de volume écrit « Cause : la propriete « run: new TextRun » » : le garde a donc
#    refusé une config saine, et c'était le troisième garde que je cassais moi-même dans la
#    journée. Une liste de formulations à exclure est intrinsèquement fragile — il faudrait
#    la rallonger à chaque fois qu'on écrit sur le sujet.
#    DONC : on exige la PRÉSENCE de la bonne forme, qui n'a aucune surface de faux positif.
#    Tout prompt qui parle de « new TextRun » doit contenir « children: [new TextRun ». Un
#    retour à « run: » supprime cette chaîne et est attrapé ; un prompt neuf qui prescrirait
#    « run: » ne la contiendrait pas davantage. Sans réseau, instantané.
if [ -f "$ROOT/jobs_config.json" ]; then
  PR_OUT="$CUR/prompts_textrun.txt"
  env -i $PY - "$ROOT/jobs_config.json" > "$PR_OUT" 2>&1 <<'PYPR'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
manque = [j["id"] for j in d["jobs"]
          if "new TextRun" in j["prompt"] and "children: [new TextRun" not in j["prompt"]]
if manque:
    print("\n".join(sorted(manque)))
PYPR
  if [ -s "$PR_OUT" ]; then
    echo "▶ Prompts des jobs — LA FORME « children: [new TextRun » MANQUE"
    sed 's/^/     /' "$PR_OUT"
    echo "  ✗ ce(s) prompt(s) parle(nt) de TextRun sans prescrire « children: ». Si la"
    echo "    consigne est « run: new TextRun », docx l'ignore en silence et le .docx produit"
    echo "    est un XML valide, lié, et VIDE — le contrôle d'intégrité ne l'attrape qu'avec"
    echo "    l'assertion de volume ajoutée le 17/10/2026."
    exit 1
  else
    echo "  ✓ tout prompt parlant de TextRun prescrit « children: [new TextRun »"
  fi
fi

# ---- Qui aspire doit lire BORNÉ (19/10/2026) ----
# Un prompt qui appelle aspirer.py met une page sur disque ; s'il ne dit pas COMMENT la lire, la
# page entre entière en contexte. Mesuré : la consigne « sed -n, grep -n » du 18/10 était
# inapplicable (une page aspirée est une seule ligne), et le créneau suivant est passé de 59 % à
# 93 % du plafond. L'exigence est POSITIVE, comme celle de « children: » — on demande la présence
# de la bonne forme, pas l'absence des mauvaises, parce qu'une liste de formulations à exclure se
# mord elle-même (leçon du 17/10).
# ⚠ Borne : seuls les prompts qui aspirent sont concernés — aujourd'hui rbpp-pipeline, et lui
#   seul ; les huit autres sont muets sur aspirer.py, le garde y est inerte et le dit.
if [ -f "$ROOT/jobs_config.json" ]; then
  ASP_OUT="$CUR/prompts_lecture.txt"
  env -i $PY - "$ROOT/jobs_config.json" > "$ASP_OUT" 2>&1 <<'PYASP'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
aspirent = [j["id"] for j in d["jobs"] if "aspirer.py" in j["prompt"]]
manque = [j["id"] for j in d["jobs"]
          if "aspirer.py" in j["prompt"] and "lire_page.py --autour" not in j["prompt"]]
if manque:
    print("  x ce(s) prompt(s) aspirent une page sans prescrire de lecture bornée :")
    print("    " + ", ".join(sorted(manque)))
    print("    sans « lire_page.py --autour », la page entre ENTIÈRE en contexte — c'est le")
    print("    passage de 59 % à 93 % du plafond mesuré sur rbpp-pipeline le 19/10/2026.")
    sys.exit(1)
print("  ✓ tout prompt qui aspire une page prescrit « lire_page.py --autour » (%s)"
      % (", ".join(sorted(aspirent)) if aspirent else "aucun prompt n'aspire — garde INERTE"))
# 🔗 20/10/2026 — et tout prompt qui TESTE des URL doit en rendre le décompte. Exigence POSITIVE
#    sur la forme exacte que le contrôle relève : sans elle, un lien jeté sur un 000 reste
#    invisible, puisqu'un livrable ne garde pas trace de ce qu'il n'a pas cité.
teste = [j["id"] for j in d["jobs"] if '-w "%{http_code}"' in j["prompt"]]
sans = [j["id"] for j in d["jobs"]
        if '-w "%{http_code}"' in j["prompt"] and "🔗 Liens : N testés" not in j["prompt"]]
if sans:
    print("  x ce(s) prompt(s) testent des URL sans prescrire le décompte des écartées :")
    print("    " + ", ".join(sorted(sans)))
    print("    la ligne « 🔗 Liens : N testés · X retenus · Y écartés (codes : …) » est la SEULE")
    print("    trace d'un lien jeté sur un 000 — le livrable n'en garde aucune.")
    sys.exit(1)
print("  ✓ les %d prompt(s) qui testent des URL prescrivent le décompte des écartées" % len(teste))
PYASP
  rc=$?
  cat "$ASP_OUT"
  if [ "$rc" != "0" ]; then exit 1; fi
fi

# ---- LES ASSERTIONS DE TABLEAU DES PROMPTS, ET LA PREUVE QU'ELLES MORDENT (18/10/2026) ----
# Le 18/10/2026 la veille iMac a livré ZÉRO tableau Word pour 38 lignes à barres verticales : ses
# trois tableaux de prix étaient des paragraphes séparés par « | ». Le contrôle d'intégrité que le
# prompt impose a répondu « OK — XML conforme, 12 lien(s), 99 paragraphe(s) de texte (marge 87) » :
# il vérifie l'XML, les balises, les liens et le VOLUME de texte, jamais un tableau. C'est la même
# forme que l'incident du 17/10 — un contrôle qui dit OK sur un document dégradé —, un cran moins
# grave : là le corps avait disparu, ici c'est la mise en forme.
# 🔴 DEUX PROMPTS, DEUX PLANCHERS, CHACUN MESURÉ SUR SA PROPRE SÉRIE.
#    · imac-veille, plancher 2 : sur ses 19 éditions, les 15 consécutives du 19/07 au 11/10 portent
#      3 à 6 tableaux (médiane 4, minimum 3) ; les trois seules autres à zéro datent des 14/06,
#      21/06 et 13/07, avant la stabilisation du format. Plancher à 2 et non à 3 parce que le CR
#      ALLÉGÉ du prompt ne prescrit que les deux tableaux de prix de référence.
#    · rbpp-pipeline, plancher 1 ET BORNÉ AU CHEMIN « /rbpp/ » : sa structure ne nomme QU'UN
#      tableau (points clés), et le job a DEUX sorties — la note RBPP, et la note d'Étape 7 des
#      semaines sans nouvelle RBPP, qui part dans has-actualite/ où les 16 éditions du dépôt
#      n'ont aucun tableau. Non bornée, l'assertion refuserait une note d'Étape 7 conforme, et
#      c'est le chemin qu'a pris l'exécution du 12/10/2026. Coût historique assumé : 3 des 14
#      notes RBPP auraient été refusées, et les trois rendaient leurs points clés en liste.
#      Cause mécanique : ses DEUX lignes require n'importaient pas Table — corrigé le 18/10.
#    · serafin-ph-veille, plancher 3 : PORTAGE PRÉVENTIF, cette série n'a PAS eu l'incident — 27
#      éditions sur 27 portent des tableaux, minimum 4 atteint 14 fois, médiane 4, maximum 8.
#      Plancher à 3 et non à 4 pour deux raisons indépendantes : sa structure nomme explicitement
#      TROIS tableaux (sources, tableau de bord, points de vigilance), et la note allégée de semaine
#      creuse doit rester possible — l'édition du 14/10, semaine creuse assumée, porte ses 4.
# ⛔ ET LA MESURE INTERDIT DE LES PORTER AUX NEUF PROMPTS : les 21 veilles ai-act, les 16
#    has-actualite et les 8 rgpd n'ont AUCUN tableau — ai-act n'en prescrit aucun, c'est voulu — et
#    10 des 11 leçons entretien-motivationnel non plus. Ce serait 45 refus légitimes.
# 🧪 TROIS GARDES, ET AUCUN N'EST REDONDANT — LE SABOTAGE L'A MONTRÉ.
#    (1) le prompt doit PORTER l'assertion : « TABLEAUX MANQUANTS », x.count("<w:tbl>") et
#        « TableRow ». Exigence POSITIVE, comme celle de « children: », parce qu'une liste de
#        formulations à exclure se mord elle-même (leçon du 17/10).
#    (2) il doit porter SON PLANCHER AU LITTÉRAL (« if tbl < 2: », « if tbl < 3: »). Sans cette
#        exigence, ramener un plancher de 2 à 1 laissait les deux premiers témoins verts : un
#        témoin à 0 tableau reste refusé par un plancher à 1. C'est le trou que les mutants
#        borderline de serafin ferment par le comportement, et celui-ci par le texte.
#    (3) l'assertion EXTRAITE DU PROMPT — on appelle le contrôle, on ne le recopie pas (leçon du
#        15/10 sur l'auto-test de chercher.py) — jouée sur cinq témoins FIGÉS de
#        non_regression/temoins_tableaux/, chacun avec son CODE DE SORTIE **et** SA LIGNE :
#        imac 11/10 (5 tbl) → 0 « 5 tableau(x) » · imac 18/10 avant correction (0 tbl) → 1
#        « TABLEAUX MANQUANTS » · serafin 14/10 (4 tbl) → 0 « 4 tableau(x) » · mutant serafin à
#        3 tbl → 0 « 3 tableau(x) », qui doit être ACCEPTÉ (convention du 10/10 : un motif qu'on
#        resserre a besoin d'un témoin accepté) · mutant serafin à 2 tbl → 1.
#        Les deux mutants sont DÉRIVÉS d'une édition réelle par retrait des derniers <w:tbl>, et
#        c'est dit : ce ne sont pas des livrables, ce sont des bornes.
#        Les copies sont FIGÉES : une correction future d'un fichier publié ne peut pas périmer un
#        témoin — leçon du 15/10 sur le témoin vivant qui annote une propriété volatile.
# ⚠️ IL SORT EN 1 LUI-MÊME : la branche --docs remet STATUT=0 à l'entrée, donc un garde placé
#    avant elle qui se contenterait de STATUT=1 serait décoratif (leçon déjà payée).
if [ -f "$ROOT/jobs_config.json" ]; then
  TBL_OUT="$CUR/prompt_tableaux.txt"
  env -i $PY - "$ROOT/jobs_config.json" "$ROOT/outils/scripts/non_regression/temoins_tableaux" \
      > "$TBL_OUT" 2>&1 <<'PYTBL'
import json, os, re, subprocess, sys
CFG, TD = sys.argv[1], sys.argv[2]
ATTENDU = 8                      # nombre de témoins qui DOIVENT être joués
CAS = {
    "imac-veille": ("if tbl < 2:", [
        ("conforme_2026-10-11_veille_imac_5_tableaux.docx", 0, "5 tableau(x)"),
        ("sans_tableau_2026-10-18_veille_imac.docx", 1, "TABLEAUX MANQUANTS")]),
    "serafin-ph-veille": ("if tbl < 3:", [
        ("conforme_2026-10-14_veille_SERAFIN-PH_4_tableaux.docx", 0, "4 tableau(x)"),
        ("mutant_SERAFIN-PH_3_tableaux_doit_passer.docx", 0, "3 tableau(x)"),
        ("mutant_SERAFIN-PH_2_tableaux_doit_etre_refuse.docx", 1, "TABLEAUX MANQUANTS")]),
    # rbpp-pipeline a DEUX chemins de sortie : la note RBPP, dont la structure prescrit un tableau
    # de points clés, et la note d'Étape 7 (semaine sans nouvelle RBPP) qui part dans
    # sources/veille/has-actualite/ et n'en prescrit AUCUN — les 16 éditions de cette série n'en
    # ont pas une. L'assertion est donc bornée au chemin « /rbpp/ », et le TROISIÈME témoin est un
    # témoin ACCEPTÉ qui épingle l'exemption : sans lui, rien n'empêcherait de retirer la borne
    # demain et de refuser une note d'Étape 7 conforme (convention du 10/10).
    "rbpp-pipeline": ("if rbpp and tbl < 1:", [
        ("rbpp/conforme_2026-04-26_veille_rbpp_troubles-schizophreniques_8_tableaux.docx", 0, "8 tableau(x)"),
        ("rbpp/sans_tableau_2026-06-06_veille_rbpp_autisme-recommandations.docx", 1, "TABLEAUX MANQUANTS"),
        ("has-actualite/exempt_2026-10-12_veille_has-actualite.docx", 0,
         "hors note RBPP, assertion de tableau non applicable")]),
}
d = json.load(open(CFG, encoding="utf-8"))
prompts = {j["id"]: j["prompt"] for j in d["jobs"]}
ko, vus = 0, 0
for jid, (plancher, temoins) in sorted(CAS.items()):
    p = prompts.get(jid)
    if p is None:
        print("  o %s absent de la config — son assertion de tableau n'est plus gardée," % jid)
        print("    et ce n'est PAS une réussite : retire-la de CAS si le job est supprimé.")
        ko = 1
        continue
    for forme in ("TABLEAUX MANQUANTS", 'x.count("<w:tbl>")', "TableRow", plancher):
        if forme not in p:
            print("  x le prompt %s ne porte plus « %s » :" % (jid, forme))
            print("    l'assertion de tableau a sauté, ou son plancher a été déplacé.")
            ko = 1
    # 🔴 CHAQUE ligne require('docx') de CE prompt doit importer Table — et il peut y en avoir
    #    plusieurs : rbpp-pipeline en portait DEUX, toutes deux sans Table, et c'est la cause
    #    mécanique de ses trois notes sans tableau. Un « TableRow in p » ne suffit pas : il reste
    #    vrai si UNE SEULE des deux lignes est rétablie. On vérifie donc chaque occurrence.
    #    ⚠️ Borné aux prompts de CAS : ai-act-veille porte lui aussi une ligne incomplète, mais sa
    #    structure ne prescrit AUCUN tableau et ses 21 éditions n'en ont aucun — l'exiger de lui
    #    serait un faux refus.
    for m in re.finditer(r"const \{([^}]*)\} = require\('docx'\)", p):
        if "Table" not in m.group(1):
            print("  x le prompt %s porte une ligne require('docx') SANS Table :" % jid)
            print("    %s" % m.group(1).strip()[:100])
            print("    le générateur ne pourra pas construire les tableaux que la structure prescrit.")
            ko = 1
    blocs = [b for b in re.findall(r"python3 - <<'PY'\n(.*?)\nPY\n", p, re.S)
             if "<chemin complet du .docx produit>" in b]
    if len(blocs) != 1:
        print("  x %d bloc(s) d'intégrité extractible(s) du prompt %s, 1 attendu" % (len(blocs), jid))
        ko = 1
        continue
    for nom, att, ligne in temoins:
        doc = os.path.join(TD, nom)
        if not os.path.exists(doc):
            print("  x témoin de tableau manquant : %s" % nom)
            ko = 1
            continue
        vus += 1
        code = blocs[0].replace("<chemin complet du .docx produit>", doc)
        r = subprocess.run(["/usr/bin/python3", "-"], input=code, capture_output=True, text=True)
        sortie = (r.stdout + r.stderr).strip()
        if r.returncode != att:
            print("  x %s / témoin « %s » sort en %d au lieu de %d — %s"
                  % (jid, nom[:38], r.returncode, att, sortie[:80]))
            print("    " + ("L'ASSERTION NE MORD PLUS : un .docx sans ses tableaux serait publié."
                            if att else "L'ASSERTION MORD À TORT : une édition normale serait refusée."))
            ko = 1
        elif ligne not in sortie:
            print("  x %s / témoin « %s » sort bien en %d, mais SANS sa ligne « %s » :"
                  % (jid, nom[:38], att, ligne))
            print("    le code de sortie ne dit pas COMBIEN de tableaux ont été vus.")
            ko = 1
if vus != ATTENDU:
    print("  x %d témoin(s) de tableau joué(s), %d attendu(s) — rétablis temoins_tableaux/," % (vus, ATTENDU))
    print("    ou mets ATTENDU à jour si une assertion est retirée d'un prompt.")
    ko = 1
if not ko:
    print("  ✓ assertions de tableau (imac ≥ 2, serafin-ph ≥ 3, rbpp ≥ 1 hors Étape 7) : portées avec")
    print("    leur plancher, et elles mordent — %d/%d témoins figés, chacun avec sa ligne" % (vus, ATTENDU))
sys.exit(ko)
PYTBL
  rc=$?
  cat "$TBL_OUT"
  if [ "$rc" != "0" ]; then exit 1; fi
fi

# ── 0 sexies. LA TOLÉRANCE « PAGE NON LUE » DU BLOC 5 BIS (25/10/2026)
# 🔴 QUATRIÈME INCIDENT DE LA MÊME CLASSE : UN TÉMOIN VIVANT DONT LE VERDICT DÉPEND D'UNE
#    PROPRIÉTÉ VOLATILE. Les 23 et 25/10/2026, promenade.imcce.fr est tombé — DNS résolu, aucune
#    réponse TCP, curl exit 28 AVEC et SANS le faisceau, donc ni TLS ni nous — et le bloc des
#    étapes 5 bis a déclaré « faux positif du contrôle » son témoin conforme d'astrologie n°10 :
#    « ⑦ PAGE SANS RÉPONSE, NON DÉCLARÉE (…/221.html : code 000 après 3 essais) ». Le document
#    n'avait pas changé d'un octet, le refus du contrôle était EXACT, et le harnais sortait en 1 :
#    LE HOOK REFUSAIT TOUS LES PUSHS DU DÉPÔT, exactement comme le motif ⑩ le 15/10 et comme le
#    témoin de supprimer_job.sh le 22/10. Mesuré au passage : pendant la panne, un seul passage du
#    contrôle astro prend 2 min 14 s au lieu de 11 s (3 essais × 40 s de --max-time).
#    🟢 La décision est prise AU HARNAIS, pas dans les contrôles : en production, ⑦ doit continuer
#    à refuser une page muette non déclarée. Ce qui est faux, c'est de lire ce refus comme la
#    RÉGRESSION D'UN DÉPÔT. Le duo n'est donc pas joué — et le harnais le DIT, il ne le tait pas.
#    Les neuf bornes tournent sur un serveur HTTP local et un hôte .invalid (RFC 2606, qui ne
#    résout jamais PAR NORME) : aucun tiers, donc cette garde-là ne peut pas périmer à son tour.
if [ -x "$NR/tolerance_page_morte.py" ]; then
  echo "▶ Auto-tests de la tolérance « page non lue » du bloc 5 bis (serveur local, aucun tiers)"
  TPM_OUT="$CUR/tolerance_page_morte_autotest.txt"
  if env -i $PY "$NR/tolerance_page_morte.py" --autotest > "$TPM_OUT" 2>&1; then
    tail -1 "$TPM_OUT"
    # même garde qu'ATTENDU_LIENS et ATTENDU_MARQ : un lot amputé passerait au vert, et c'est
    # L'EXCUSE qui décide si le refus d'un témoin bloque le push de tout le dépôt.
    ATTENDU_TOL=10
    LU_TOL=$(sed -n 's/.* [0-9]\{1,\}\/\([0-9]\{1,\}\) bornes de tolerance_page_morte.*/\1/p' "$TPM_OUT")
    if [ "$LU_TOL" != "$ATTENDU_TOL" ]; then
      echo "  ✗ ${LU_TOL:-0} borne(s) de tolérance jouée(s), $ATTENDU_TOL attendue(s) — un lot amputé"
      echo "    passerait au vert, et l'excuse pourrait s'élargir sans bruit."
      exit 1
    fi
  else
    grep '✗' "$TPM_OUT" | head -5
    echo "  ✗ LA TOLÉRANCE « PAGE NON LUE » A PERDU UNE BORNE — si elle excuse une page VIVANTE, un"
    echo "    vrai faux positif de contrôle passerait désormais pour une panne de réseau."
    exit 1
  fi
fi

# ── 0 septies. LA CLASSIFICATION DU BALAYAGE D'ADRESSES (25/10/2026)
# `balayer_adresses.py` est le seul outil du dépôt qui relise les adresses d'un livrable que
# PERSONNE n'a touché : les contrôles n'ouvrent que les pages du document qu'on leur donne, et le
# harnais ne voit que les documents d'un push. Le balayage lui-même n'est PAS câblé ici — une page
# tierce morte n'est pas une régression du dépôt, même raison que `--manques` — mais sa
# CLASSIFICATION est de la logique du dépôt, et elle encode la leçon du 18/10 :
# 🔴 UN DÉFAUT DE TLS NE DIT PAS QU'UNE PAGE EST MORTE. Mesuré le 25/10 sur quatre des vingt
#    injoignables du premier balayage, faisceau compris : exit 60 (certificat) pour
#    entretienmotivationnel.org, cité par 7 documents ; exit 35 (connexion TLS) pour
#    service-public.gouv.fr ; exit 28 (délai) pour media4.obspm.fr ; exit 6 (hôte non résolu) pour
#    davidstamile.com. Les quatre rendaient le même « 000 ». Classer les quatre pareil, c'était
#    écrire en face d'une page vivante qu'elle est morte — exactement ce que `has-sante.fr` a
#    coûté le 18/10 avant le faisceau. Seuls MORTE (404/410) et DNS (hôte disparu) condamnent.
if [ -x "$ROOT/outils/scripts/balayer_adresses.py" ]; then
  echo "▶ Auto-tests de la classification du balayage d'adresses (aucun réseau)"
  BAL_OUT="$CUR/balayage_autotest.txt"
  if env -i $PY "$ROOT/outils/scripts/balayer_adresses.py" --autotest > "$BAL_OUT" 2>&1; then
    tail -1 "$BAL_OUT"
    # même garde qu'ATTENDU_LIENS, ATTENDU_MARQ et ATTENDU_TOL : le total est CALCULÉ depuis le lot,
    # donc un lot amputé imprimerait un « N/N » plus petit sans que rien ne refuse.
    ATTENDU_BAL=41
    LU_BAL=$(sed -n 's/.* \([0-9]\{1,\}\)\/[0-9]\{1,\} bornes de balayer_adresses.*/\1/p' "$BAL_OUT")
    if [ "$LU_BAL" != "$ATTENDU_BAL" ]; then
      echo "  ✗ ${LU_BAL:-0} borne(s) de classification jouée(s), $ATTENDU_BAL attendue(s) — un lot"
      echo "    amputé imprimerait un total plus petit et passerait au vert."
      exit 1
    fi
  else
    grep '✗' "$BAL_OUT" | head -5
    echo "  ✗ LA CLASSIFICATION DU BALAYAGE A PERDU UNE BORNE — un défaut de TLS pourrait redevenir"
    echo "    « lien mort », et on corrigerait des adresses vivantes."
    exit 1
  fi
fi

# ── 0 octies. LE FAISCEAU DE CERTIFICATS EST-IL COMPLET ? (26/10/2026)
# `ca_bundle.py` ne connaissait QU'UN intermédiaire, écrit en dur : celui que l'AIA du certificat
# de `has-sante.fr` désigne. Le 26/10, `cnsa.fr` est tombé du MÊME défaut — certificat réémis le
# 14/10/2026, chaîne intermédiaire absente, `curl` 60 sur les 38 documents qui citent la CNSA —
# mais avec un AUTRE émetteur, « Sectigo Qualified Website Authentication CA R39 ». Il a donc fallu
# un SECOND maillon, et le chemin en dur l'aurait ignoré en silence.
# 🔴 LE DÉFAUT QUE CES BORNES GARDENT EST EXACTEMENT CELUI-LÀ : un `.pem` déposé dans `ca/` et
#    jamais chargé. Rien ne l'aurait dit — ni une erreur, ni un `✗` : le faisceau se serait
#    reconstruit sans lui, et les pages de l'hôte concerné seraient restées « NON LUES », donc
#    indiscernables d'une citation absente. C'est le même angle mort qu'un lien écarté sur un 000.
# ⚠️ Aucun réseau, aucun tiers : ces bornes comparent le faisceau en cache à ce que `ca/` contient,
#    et exercent le VRAI `intermediaires()` en déplaçant `CA_DIR` vers une arborescence fabriquée.
#    Elles ne peuvent donc PAS périmer sur la panne d'un site — la leçon des 15, 22 et 23/10.
if [ -f "$ROOT/outils/scripts/ca_bundle.py" ]; then
  echo "▶ Auto-tests du faisceau de certificats (aucun réseau)"
  CAB_OUT="$CUR/ca_bundle_autotest.txt"
  # ⚠ PAS de pipe : « ... --autotest | tail -1 » testerait le code de `tail` (leçon du 15/10).
  if env -i $PY "$ROOT/outils/scripts/ca_bundle.py" --autotest > "$CAB_OUT" 2>&1; then
    tail -1 "$CAB_OUT"
    # même garde qu'ATTENDU_BAL, ATTENDU_TOL, ATTENDU_LIENS et ATTENDU_MARQ : le total est CALCULÉ
    # depuis le lot, donc un lot amputé imprimerait un « N/N » plus petit sans que rien ne refuse.
    ATTENDU_CA=6
    LU_CA=$(sed -n 's/.* [0-9]\{1,\}\/\([0-9]\{1,\}\) bornes du faisceau.*/\1/p' "$CAB_OUT")
    if [ "$LU_CA" != "$ATTENDU_CA" ]; then
      echo "  ✗ ${LU_CA:-0} borne(s) de faisceau jouée(s), $ATTENDU_CA attendue(s) — un lot amputé"
      echo "    imprimerait un total plus petit et passerait au vert."
      exit 1
    fi
  else
    grep '✗' "$CAB_OUT" | head -5
    echo "  ✗ LE FAISCEAU DE CERTIFICATS EST INCOMPLET — un intermédiaire versionné dans ca/ n'est"
    echo "    pas chargé. Les pages de l'hôte concerné redeviendraient « NON LUES » en silence,"
    echo "    et leurs sources seraient écartées sur un 000 qui ne dit rien de la page."
    exit 1
  fi
fi

# ── 0 decies. LES TROIS ÉTAPES 5 BIS SONDENT-ELLES AVEC LE FAISCEAU ? (26/10/2026)
#    Elles appelaient `curl` SANS `--cacert` quand tout le reste du dépôt le passe depuis le
#    18/10. Mesuré sur l'hôte même que `controle_psychopathologie.py` sonde — deux URL
#    `has-sante.fr/jcms/` citées par ses leçons : 000 · exit 60 sans le faisceau, 200 · exit 0
#    avec. ET LE DÉFAUT ÉTAIT SILENCIEUX : son motif (1) s'écrit `if pdfs and not any(…)`,
#    donc une page vide le rend INERTE — il ne refusait pas à tort, il ne voyait rien.
#    Le portage a rendu QUATRE refus exacts sur treize leçons (vérifiés à la main : 1 à 12 PDF
#    liés sur la page jcms, zéro dans les ressources du document).
#    ⚠️ Et le portage à `controle_ai_act.py` est PRÉVENTIF, il faut le dire : aucun de ses
#    22 documents ne cite un hôte où le faisceau change la réponse. Même honnêteté que le
#    portage préventif de l'assertion de tableau à `serafin-ph` le 18/10.
#    AUCUN RÉSEAU, 0,1 s — donc joué dans TOUS les modes, comme les auto-tests du faisceau.
if [ -f "$ROOT/outils/scripts/non_regression/faisceau_5bis.py" ]; then
  echo "▶ Témoin du faisceau dans les trois étapes 5 bis (aucun réseau)"
  CB5_OUT="$CUR/faisceau_5bis.txt"
  if env -i $PY "$ROOT/outils/scripts/non_regression/faisceau_5bis.py" > "$CB5_OUT" 2>&1; then
    tail -1 "$CB5_OUT"
    # ⚠️ LE GARDE DE COMPTE N'EST PAS REDONDANT (23 et 24/10/2026, deux fois mesuré) : sans
    #    lui, retirer une borne du lot fait imprimer « ✓ 6/6 » et sortir en 0.
    ATTENDU_CB5=7
    LU_CB5=$(sed -n 's/.* [0-9]\{1,\}\/\([0-9]\{1,\}\) bornes du faisceau des étapes 5 bis.*/\1/p' "$CB5_OUT")
    if [ "$LU_CB5" != "$ATTENDU_CB5" ]; then
      echo "  ✗ $LU_CB5 borne(s) tenue(s), $ATTENDU_CB5 attendue(s) — un lot amputé ne prouve rien :"
      echo "    rétablis la borne retirée, ou mets ATTENDU_CB5 à jour en disant pourquoi."
      exit 1
    fi
  else
    grep '✗' "$CB5_OUT" | head -7
    echo "  ✗ UNE ÉTAPE 5 BIS SONDE SANS LE FAISCEAU DE CERTIFICATS — les pages de l'hôte"
    echo "    concerné rendraient 000, et le motif (1) de psychopathologie redeviendrait INERTE"
    echo "    au lieu de refuser : un défaut invisible, pas un faux refus."
    exit 1
  fi
fi

# ── 0 undecies. LE MOTIF (1) DE PSYCHOPATHOLOGIE RESTE-T-IL BORNÉ AUX PAGES DE RBPP ? (26/10/2026)
#    Le portage du faisceau, le matin même, a rendu ACTIF un motif inerte depuis le 18/10, et
#    devenu actif il a mordu sur un COMMUNIQUÉ DE PRESSE — il exigeait des ressources de la
#    leçon l'annexe thématique d'une page d'actualité. Borné à l'étiquette de type que chaque
#    page HAS se donne, mesurée sur les 17 pages jcms du corpus : `Recommandation de bonne
#    pratique` (9), `Communiqué de presse` (1), `Flash sécurité patient` (1), `Article HAS` (2),
#    aucune pour les 4 portails. Effet mesuré sur les 20 leçons : 0 verdict changé,
#    UNE SEULE raison de refus retirée (la leçon 07 reste en exit 1 sur son autre motif).
#    ⚠️ La borne ⑤ est la seule qui sépare ce bornage d'un `"…" in page` naïf, et la ⑨ est la
#    seule qui empêche de rendre l'exemption SILENCIEUSE — le défaut fermé le matin même.
#    🆕 27/10/2026 — IL GARDE AUSSI LE DÉCOMPTE DES EXEMPTIONS ET SON ALERTE. L'angle mort est
#    symétrique : un renommage du gabarit HAS rendrait TOUTES les pages exemptes et le motif
#    inerte. ⛔ Mais « 100 % d'exemptions » SEUL est un état légitime — mesuré, la leçon 17 ne
#    cite qu'une page à PDF, un Flash sécurité patient : 1 sur 1. L'alerte est donc « 100 %
#    ET aucune étiquette lue », signature du renommage, et sur les 11 visites de page à PDF du
#    corpus une étiquette a été lue 11 fois sur 11 → zéro fausse alerte mesurée. La borne ⑭
#    est celle qui doit être ACCEPTÉE : sans elle, rien n'empêche de faire crier l'alerte sur
#    un document conforme.
#    AUCUN RÉSEAU, témoins figés en HTML inline — joué dans TOUS les modes.
if [ -f "$ROOT/outils/scripts/non_regression/etiquette_has.py" ]; then
  echo "▶ Témoin de l'étiquette HAS — le motif (1) borné aux RBPP (aucun réseau)"
  ETQ_OUT="$CUR/etiquette_has.txt"
  if env -i $PY "$ROOT/outils/scripts/non_regression/etiquette_has.py" > "$ETQ_OUT" 2>&1; then
    tail -1 "$ETQ_OUT"
    # ⚠️ LE GARDE LIT LE DÉNOMINATEUR, c'est-à-dire le nombre de bornes JOUÉES. Avec le
    #    numérateur, retirer une borne laissait « 9/9 » : défaut mesuré le 26/10 sur mes deux
    #    propres gardes (ATTENDU_CA et ATTENDU_CB5), les deux étaient décoratifs.
    ATTENDU_ETIQ=17          # 10 -> 17 le 27/10/2026 : 6 bornes du décompte des exemptions, + la remontée de l'alerte
    LU_ETIQ=$(sed -n "s/.* [0-9]\{1,\}\/\([0-9]\{1,\}\) bornes de l'étiquette HAS.*/\1/p" "$ETQ_OUT")
    if [ "$LU_ETIQ" != "$ATTENDU_ETIQ" ]; then
      echo "  ✗ $LU_ETIQ borne(s) jouée(s), $ATTENDU_ETIQ attendue(s) — un lot amputé ne prouve rien :"
      echo "    rétablis la borne retirée, ou mets ATTENDU_ETIQ à jour en disant pourquoi."
      exit 1
    fi
  else
    grep '✗' "$ETQ_OUT" | head -9
    echo "  ✗ LE MOTIF (1) DE PSYCHOPATHOLOGIE N'EST PLUS BORNÉ AUX PAGES DE RBPP — soit il"
    echo "    refusera une leçon pour un communiqué de presse, soit il est redevenu INERTE et"
    echo "    ne dira plus rien du tout. Les deux sens sont gardés ici — et depuis le 27/10 le"
    echo "    décompte des exemptions avec son alerte, dont la borne qui doit être ACCEPTÉE."
    exit 1
  fi
fi

bloc_orthographe || exit 1
bloc_desarmement || exit 1

# ── 0. mode documents : quelques .docx, comparés un à un à la référence
if [ "$MODE" = "--docs" ]; then
  shift; STATUT=0
  [ $# -eq 0 ] && { echo "  (aucun document)"; exit 0; }
  # ㊳ (16/10/2026) UN LIVRABLE POUSSÉ VIENT-IL D'UNE EXÉCUTION RÉUSSIE ?
  # 🔴 BLOQUANT depuis le 16/10/2026, sur décision explicite — avec une EXEMPTION PAR
  # DÉCLARATION sans laquelle il serait un piège : il s'appuie sur le run qui a produit le
  # fichier, un fait qui ne change jamais, donc le livrable du 16/10 et chacune de ses
  # corrections futures seraient refusés indéfiniment. Le document doit DIRE lui-même qu'il
  # vient d'une exécution échouée ET qu'il a été relu hors du job.
  # ⚠️ CE QUE CELA ENFREINT, ET C'EST ÉCRIT DANS LE DOCSTRING DU CONTRÔLE : la règle du
  # 14/10/2026 veut un passage en avertissement sur quelques éditions neuves avant de
  # bloquer. Ici le motif a tourné en avertissement UNE journée, sur UN cas. Ce qui borne le
  # risque n'est donc pas l'observation mais l'exemption — un faux refus se lève en écrivant
  # une phrase dans le livrable, pas en modifiant un contrôle.
  if [ -x "$ROOT/outils/scripts/controle_livrable_du_job.py" ]; then
    LJ="$CUR/livrable_du_job.txt"
    if ! env -i $PY "$ROOT/outils/scripts/controle_livrable_du_job.py" "$@" > "$LJ" 2>&1; then
      cat "$LJ"
      STATUT=1
    else
      [ -s "$LJ" ] && cat "$LJ"
    fi
  fi
  env -i $PY - "$ROOT/outils/scripts/controle_attributions.py" "$@" > "$CUR/docs_A.tsv" <<'PYH'
import sys, io, contextlib
src = open(sys.argv[1], encoding="utf-8").read()
code = src[src.index("import sys, re, html, subprocess"):src.index("# ── aspiration des pages")]
for f in sys.argv[2:]:
    sys.argv = ["x", f]; out = io.StringIO(); g = {"__name__": "__main__"}
    ko = None
    with contextlib.redirect_stdout(out):
        try: exec(code, g)
        except SystemExit as e: ko = e.code
    # 26/10/2026 — NE PLUS JETER LE REFUS DU CONTROLE. Le SEUL sys.exit de la tranche extraite
    # est « EXTRACTION IMPOSSIBLE (fichier introuvable ou illisible) » : il partait dans le
    # tampon redirige, abandonne, et la ligne suivante annoncait « 0 bloquant(s) ». Le temoin
    # positif g["t"] garde le cas d'un refus qui ne passerait plus par sys.exit.
    # ⚠️ ET LE FICHIER CORROMPU QUI EXISTE EST LE CAS LE PLUS SOURNOIS DES DEUX : extract_docx.py
    # imprime « ERROR: File is not a zip file » sur STDERR — que le controle jette, ne lisant que
    # stdout — puis emet ses marqueurs A ZERO et sort en 0. Le controle voit alors un document
    # VIDE, pas un document illisible, et rend « 0 bloquant(s) ». Le signal visible sur stdout est
    # le compte de caracteres. BORNE MESUREE SUR LES 296 DOCUMENTS DU CORPUS : zero porte
    # « TEXTE COMPLET (0 », zero porte « ERROR: », zero est sans marqueur — donc zero faux refus.
    if ko is None:
        tt = g.get("t") or ""
        if not tt or "=== TEXTE COMPLET (0 " in tt:
            ko = "le controle n'a rien extrait (document vide ou illisible)"
    if ko is not None:
        print("%s\tKO\t%s" % (f.split("/")[-1], str(ko).replace("\t", " ")[:200]))
        continue
    orph = sorted(g.get("orphelines", set())); snl = sorted(g.get("sites_non_listes", set()))
    a2 = sorted(g.get("sans_adresse", set())); a3 = sorted(g.get("mal_formes", set())); a4 = list(g.get("src_sans_adresse", [])) + list(g.get("sans_cible", []))
    print("%s\t%d\t%s" % (f.split("/")[-1], len(orph) + len(snl) + len(a2) + len(a3) + len(a4), " ; ".join(orph + snl + a2 + a3 + a4)[:300]))
PYH
  while IFS=$'\t' read -r nom n detail; do
    # 26/10/2026 — UN FICHIER ILLISIBLE N'EST PAS UN DOCUMENT À ZÉRO BLOQUANT.
    if [ "$n" = "KO" ]; then
      echo "  ✗ $nom : LE CONTRÔLE N'A PAS PU LIRE CE DOCUMENT — $detail"
      echo "    Jusqu'au 26/10/2026 ce cas imprimait « ✓ 0 bloquant(s) » : le refus du contrôle"
      echo "    partait dans un tampon abandonné. Vérifie le chemin, puis relance."
      STATUT=1; continue
    fi
    ref=$(awk -F'\t' -v n="$nom" '$1==n{print $2}' "$REF/passe_A.tsv" 2>/dev/null)
    if [ -z "$ref" ]; then etat="nouveau"; ref=0; else etat="référence $ref"; fi
    if [ "$n" -gt "$ref" ]; then echo "  ✗ $nom : $n bloquant(s) ($etat) — $detail"; STATUT=1
    else echo "  ✓ $nom : $n bloquant(s) ($etat)"; fi
  done < "$CUR/docs_A.tsv"
  for f in "$@"; do
    case "$f" in */sources/veille/*|sources/veille/*)
      env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > "$CUR/doc_dec.txt" 2>&1; rc=$?
      nom="${f#*sources/veille/}"; ref=$(awk -F'\t' -v n="$nom" '$2==n{print $1}' "$REF/decompte.tsv" 2>/dev/null)
      if [ "$rc" = "1" ] && [ "${ref:-0}" != "1" ]; then echo "  ✗ $nom : décompte INCOHÉRENT (exit 1) — $(tail -1 "$CUR/doc_dec.txt")"; STATUT=1
      else echo "  ✓ $nom : décompte exit $rc"; fi
      # 12/10/2026 — relecture à l'édition PRÉCÉDENTE et à sa fiche. Aucun appel réseau, 0,3 s :
      # ce contrôle a sa place ici, dans la porte des pushs de job, et c'est le seul motif de
      # cette porte qui regarde AILLEURS que dans le document poussé.
      if [ -f "$ROOT/outils/scripts/controle_edition_precedente.py" ]; then
        env -i $PY "$ROOT/outils/scripts/controle_edition_precedente.py" "$f" > "$CUR/doc_edprec.txt" 2>&1; rce=$?
        case "$rce" in
          1) echo "  ✗ $nom : REJEU d'une correction de l'édition précédente — $(tail -1 "$CUR/doc_edprec.txt")"; STATUT=1;;
          2) echo "  ○ $nom : pas d'édition précédente — relecture INERTE";;
          *) RL=$(grep -c "^   A RELIRE" "$CUR/doc_edprec.txt")
             echo "  ✓ $nom : aucun rejeu de l'édition précédente$([ "$RL" != "0" ] && echo " ($RL point(s) à relire)")";;
        esac
      fi;;
    esac
  done
  exit $STATUT
fi

# ── 0 nonies. LE GATE REFUSE-T-IL UN FICHIER QU'IL N'A PAS PU LIRE ? (26/10/2026)
# Jusqu'à ce jour, `--docs` sur un .docx introuvable OU corrompu imprimait « ✓ 0 bloquant(s) » et
# sortait en 0. Deux causes distinctes, les deux mesurées :
# 🔴 ① LE REFUS DU CONTRÔLE ÉTAIT JETÉ. `controle_attributions.py` dit pourtant exactement ce qu'il
#    faut — `sys.exit("EXTRACTION IMPOSSIBLE (fichier introuvable ou illisible)")`, le SEUL sys.exit
#    de la tranche extraite — mais le harnais l'attrapait par `except SystemExit as e: print("EXIT", e)`
#    DANS le `redirect_stdout`, c'est-à-dire dans un tampon abandonné. Le contrôle avait raison, le
#    harnais le faisait taire.
# 🔴 ② ET UN FICHIER CORROMPU QUI EXISTE NE DÉCLENCHE MÊME PAS CE sys.exit : `extract_docx.py` écrit
#    « ERROR: File is not a zip file » sur STDERR — que le contrôle jette, ne lisant que stdout — puis
#    émet ses marqueurs À ZÉRO et sort en 0. Le contrôle voit alors un document VIDE, pas illisible.
#    D'où le témoin positif sur le compte de caractères annoncé par stdout.
# ⚠️ CE QUE LE DÉFAUT NE COÛTAIT PAS, ET IL FAUT LE DIRE : le hook teste `[ -f ... ]` avant de passer
#    un document au gate, donc aucun push de job n'a jamais pu en souffrir. Il mordait l'invocation À
#    LA MAIN — c'est-à-dire la vérification d'une correction, où une faute de frappe rendait un vert.
# 🧪 Le témoin exerce le VRAI gate (`non_regression.sh --docs`), jamais une copie de sa logique, sur une
#    arborescence FABRIQUÉE en mktemp : rien de vivant dans le verdict (leçon du 22/10). Les trois cas
#    dans un seul appel, dont un qui doit être ACCEPTÉ — sans lui, rien n'empêcherait de réélargir.
#    Placé APRÈS la branche --docs : l'appel imbriqué ne peut donc pas récurser, et NR_SANS_TEMOIN_KO
#    le garde si quelqu'un déplaçait ce bloc plus haut un jour.
if [ -z "${NR_SANS_TEMOIN_KO:-}" ] && [ -d "$NR/temoins_passe_A_marqueurs" ]; then
  echo "▶ Témoin du gate --docs : un fichier illisible ne doit pas passer pour « 0 bloquant »"
  TKO=$(mktemp -d)
  SRC=$(ls "$NR"/temoins_passe_A_marqueurs/*dans-marqueur*.docx(N) | head -1)
  if [ -z "$SRC" ]; then
    echo "  ✗ aucun témoin figé à copier — le lot est amputé, rien n'est prouvé"
    rm -rf "$TKO"; exit 1
  fi
  cp "$SRC" "$TKO/bon.docx"
  printf 'ceci n est pas un zip
' > "$TKO/corrompu.docx"
  KO_OUT="$CUR/temoin_gate_illisible.txt"
  NR_SANS_TEMOIN_KO=1 "$ROOT/outils/scripts/non_regression.sh" --docs     "$TKO/bon.docx" "$TKO/corrompu.docx" "$TKO/absent.docx" > "$KO_OUT" 2>&1
  RC_KO=$?
  TKO_KO=0; TKO_N=0
  exige_ko() {          # $1 = fichier, $2 = ✓ ou ✗, $3 = ce qu'il garde
    local ligne
    TKO_N=$((TKO_N + 1))
    ligne=$(grep -- " $1 :" "$KO_OUT" | head -1)
    if [ -z "$ligne" ]; then
      echo "  ✗ $1 : AUCUNE ligne de verdict — le gate n'a rien dit de ce fichier ; $3"; TKO_KO=1; return
    fi
    case "$ligne" in
      *"$2"*) echo "  ✓ $3";;
      *) echo "  ✗ $1 : attendu « $2 », obtenu : ${ligne# } ; $3"; TKO_KO=1;;
    esac
  }
  # ⚠️ CHAQUE COUCHE A SA PROPRE LIGNE, ET CE N'EST PAS DÉCORATIF. Pour un fichier INTROUVABLE, « t »
  # est vide : le témoin positif suffirait donc à le détecter, et la capture du SystemExit serait
  # redondante au regard d'une exigence lâche. Or c'est elle qui fait dire POURQUOI, avec les mots du
  # contrôle ET le chemin fautif. On exige donc le libellé propre à chaque couche : « EXTRACTION
  # IMPOSSIBLE » vient du contrôle (couche ①), « rien extrait » du témoin positif sur stdout (couche ②).
  exige_ko "bon.docx"      "✓" "un document RÉEL reste accepté (le témoin qui interdit de réélargir)"
  exige_ko "corrompu.docx" "rien extrait" "un .docx corrompu qui EXISTE est refusé, pas lu comme vide (couche ②)"
  exige_ko "absent.docx"   "EXTRACTION IMPOSSIBLE" "un .docx introuvable est refusé AVEC les mots du contrôle (couche ①)"
  ATTENDU_KO=3            # un lot amputé imprimerait moins de lignes sans que rien ne refuse
  if [ "$TKO_N" != "$ATTENDU_KO" ]; then
    echo "  ✗ $TKO_N cas joué(s), $ATTENDU_KO attendu(s) — un lot amputé passerait au vert."; TKO_KO=1
  fi
  if [ "$RC_KO" = "0" ]; then
    echo "  ✗ le gate est sorti en 0 avec deux fichiers illisibles — un push manuel passerait."; TKO_KO=1
  fi
  rm -rf "$TKO"
  if [ "$TKO_KO" != "0" ]; then
    echo "  ✗ LE GATE DES PUSHS PEUT REDONNER UN VERT SUR UN FICHIER QU'IL N'A PAS LU — la"
    echo "    vérification d'une correction ne prouverait plus rien."
    exit 1
  fi
fi

# ── 1. passes A, A2, A3, A4 des attributions, sans aspiration : le fichier est exécuté jusqu'au marqueur « # ── aspiration »
echo "▶ Passes A/A2/A3/A4 (attributions, sans aspiration) sur leçons + veilles…"
find "$ROOT/livrables/lecons" "$ROOT/sources/veille" -name "*.docx" | sort > "$CUR/corpus.txt"
env -i $PY - "$ROOT/outils/scripts/controle_attributions.py" $(cat "$CUR/corpus.txt") > "$CUR/passe_A.tsv" <<'PYH'
import sys, io, contextlib
src = open(sys.argv[1], encoding="utf-8").read()
code = src[src.index("import sys, re, html, subprocess"):src.index("# ── aspiration des pages")]
for f in sys.argv[2:]:
    sys.argv = ["x", f]; out = io.StringIO(); g = {"__name__": "__main__"}
    ko = None
    with contextlib.redirect_stdout(out):
        try: exec(code, g)
        except SystemExit as e: ko = e.code
    # 26/10/2026 — NE PLUS JETER LE REFUS DU CONTROLE. Le SEUL sys.exit de la tranche extraite
    # est « EXTRACTION IMPOSSIBLE (fichier introuvable ou illisible) » : il partait dans le
    # tampon redirige, abandonne, et la ligne suivante annoncait « 0 bloquant(s) ». Le temoin
    # positif g["t"] garde le cas d'un refus qui ne passerait plus par sys.exit.
    # ⚠️ ET LE FICHIER CORROMPU QUI EXISTE EST LE CAS LE PLUS SOURNOIS DES DEUX : extract_docx.py
    # imprime « ERROR: File is not a zip file » sur STDERR — que le controle jette, ne lisant que
    # stdout — puis emet ses marqueurs A ZERO et sort en 0. Le controle voit alors un document
    # VIDE, pas un document illisible, et rend « 0 bloquant(s) ». Le signal visible sur stdout est
    # le compte de caracteres. BORNE MESUREE SUR LES 296 DOCUMENTS DU CORPUS : zero porte
    # « TEXTE COMPLET (0 », zero porte « ERROR: », zero est sans marqueur — donc zero faux refus.
    if ko is None:
        tt = g.get("t") or ""
        if not tt or "=== TEXTE COMPLET (0 " in tt:
            ko = "le controle n'a rien extrait (document vide ou illisible)"
    if ko is not None:
        print("%s\tKO\t%s" % (f.split("/")[-1], str(ko).replace("\t", " ")[:200]))
        continue
    orph = sorted(g.get("orphelines", set())); snl = sorted(g.get("sites_non_listes", set()))
    a2 = sorted(g.get("sans_adresse", set())); a3 = sorted(g.get("mal_formes", set())); a4 = list(g.get("src_sans_adresse", [])) + list(g.get("sans_cible", []))
    print("%s\t%d\t%s\t%s\t%s" % (f.split("/")[-1], len(orph) + len(snl) + len(a2) + len(a3) + len(a4), ";".join(orph), ";".join(snl), ";".join(a2 + a3 + a4)[:200]))
PYH
# 26/10/2026 — ET CE SITE-CI EST LE PLUS GRAVE DES TROIS : c'est lui qui alimente la référence.
# `--accepter` fait `cp passe_A.tsv` dans reference/ ; un « KO » accepté une fois serait comparé à
# lui-même au passage suivant ($2!=$3 faux) et le vert deviendrait DÉFINITIF. On refuse avant.
KO_A=$(awk -F'\t' '$2=="KO"' "$CUR/passe_A.tsv")
if [ -n "$KO_A" ]; then
  printf '%s\n' "$KO_A" | sed 's/^/  ✗ ILLISIBLE : /'
  echo "  ✗ UN DOCUMENT DU CORPUS EST ILLISIBLE — ne surtout pas --accepter : la référence"
  echo "    figerait « KO » et ce document ne serait plus jamais comparé à rien."
  exit 1
fi
N_A=$(wc -l < "$CUR/passe_A.tsv" | tr -d ' '); B_A=$(awk -F'\t' '$2>0' "$CUR/passe_A.tsv" | wc -l | tr -d ' ')
echo "  $N_A documents · $B_A bloquant(s)"

# ── 1 bis. LA PASSE A ÉCARTE-T-ELLE LES MARQUEURS DE CORRECTION ? (25/10/2026)
# La doctrine du dépôt oblige, en corrigeant une adresse fautive, à CONSERVER son libellé d'origine
# dans le marqueur et dans le 📝 Journal des corrections. Or la collecte d'adresses de la passe A
# lisait « avant_res » marqueurs COMPRIS, là où B, B-FR, B-NOM et D lisent « corps_hm » : reproduire
# le libellé ROUVRAIT le motif bloquant que la correction venait de fermer. Mesuré le 23/10 sur la
# veille SERAFIN-PH du 21/10, deux fois — dans le journal puis dans un marqueur —, et contourné en
# écrivant une espace après le domaine. Donc toute correction d'adresse déformait l'original.
# ⚠️ LES DEUX SENS, ET LE SECOND EST CELUI QUI COMPTE. Le témoin « dans-marqueur » est la veille
#    publiée avec son libellé RENDU À L'IDENTIQUE : il doit sortir à 0 (il sortait à 1). Le témoin
#    « hors-marqueur » porte LA MÊME adresse, en plus, dans une ligne « Source : » du corps : il
#    doit rester à 1. Sans lui, rien n'empêcherait d'exempter le corps entier — l'exemption doit
#    s'arrêter aux SPANS des marqueurs, et c'est ce témoin qui le prouve, pas le commentaire.
# Copies FIGÉES, aucun réseau : les passes A/A2/A3/A4 tournent avant l'aspiration.
echo "▶ Témoins de la passe A et des marqueurs de correction (une adresse citée pour mémoire)…"
MQ="$CUR/passe_A_marqueurs.tsv"
env -i $PY - "$ROOT/outils/scripts/controle_attributions.py" "$NR"/temoins_passe_A_marqueurs/*.docx(N) > "$MQ" <<'PYH'
import sys, io, contextlib
src = open(sys.argv[1], encoding="utf-8").read()
code = src[src.index("import sys, re, html, subprocess"):src.index("# ── aspiration des pages")]
for f in sys.argv[2:]:
    sys.argv = ["x", f]; out = io.StringIO(); g = {"__name__": "__main__"}
    ko = None
    with contextlib.redirect_stdout(out):
        try: exec(code, g)
        except SystemExit as e: ko = e.code
    # 26/10/2026 — NE PLUS JETER LE REFUS DU CONTROLE. Le SEUL sys.exit de la tranche extraite
    # est « EXTRACTION IMPOSSIBLE (fichier introuvable ou illisible) » : il partait dans le
    # tampon redirige, abandonne, et la ligne suivante annoncait « 0 bloquant(s) ». Le temoin
    # positif g["t"] garde le cas d'un refus qui ne passerait plus par sys.exit.
    # ⚠️ ET LE FICHIER CORROMPU QUI EXISTE EST LE CAS LE PLUS SOURNOIS DES DEUX : extract_docx.py
    # imprime « ERROR: File is not a zip file » sur STDERR — que le controle jette, ne lisant que
    # stdout — puis emet ses marqueurs A ZERO et sort en 0. Le controle voit alors un document
    # VIDE, pas un document illisible, et rend « 0 bloquant(s) ». Le signal visible sur stdout est
    # le compte de caracteres. BORNE MESUREE SUR LES 296 DOCUMENTS DU CORPUS : zero porte
    # « TEXTE COMPLET (0 », zero porte « ERROR: », zero est sans marqueur — donc zero faux refus.
    if ko is None:
        tt = g.get("t") or ""
        if not tt or "=== TEXTE COMPLET (0 " in tt:
            ko = "le controle n'a rien extrait (document vide ou illisible)"
    if ko is not None:
        print("%s\tKO\t%s" % (f.split("/")[-1], str(ko).replace("\t", " ")[:200]))
        continue
    orph = sorted(g.get("orphelines", set())); snl = sorted(g.get("sites_non_listes", set()))
    a2 = sorted(g.get("sans_adresse", set())); a3 = sorted(g.get("mal_formes", set())); a4 = list(g.get("src_sans_adresse", [])) + list(g.get("sans_cible", []))
    print("%s\t%d\t%s\t%s\t%s" % (f.split("/")[-1], len(orph) + len(snl) + len(a2) + len(a3) + len(a4), ";".join(orph), ";".join(snl), ";".join(a2 + a3 + a4)[:200]))
PYH
MQ_KO=0
MQ_N=$(grep -c . "$MQ")
ATTENDU_MARQ=2        # un lot amputé passerait au vert : même garde qu'ATTENDU_LIENS (24/10/2026)
ADR="cnsa.fr/recueil-obligatoire-esms"
exige_marq() {        # $1 = part du nom, $2 = bloquants attendus, $3 = l'adresse doit-elle être là, $4 = ce qu'il garde
  local ligne n orph
  ligne=$(grep -- "$1" "$MQ" | head -1)
  n=$(printf '%s' "$ligne" | cut -f2)
  orph=$(printf '%s' "$ligne" | cut -f3)
  if [ -z "$ligne" ]; then
    echo "  ✗ témoin « $1 » ABSENT du lot — $4"; MQ_KO=1; return
  fi
  if [ "${n:-X}" != "$2" ]; then
    echo "  ✗ $1 : ${n:-?} bloquant(s), $2 attendu(s) — $4"; MQ_KO=1; return
  fi
  case "$3:$orph" in
    oui:*$ADR*) echo "  ✓ $4";;
    oui:*) echo "  ✗ $1 : l'adresse n'est plus signalée hors marqueur — $4"; MQ_KO=1;;
    non:*$ADR*) echo "  ✗ $1 : l'adresse du marqueur est encore accusée — $4"; MQ_KO=1;;
    non:*) echo "  ✓ $4";;
  esac
}
exige_marq "adresse-dans-marqueur" 0 non \
  "une adresse citée POUR MÉMOIRE dans un marqueur n'est plus une page à lister"
exige_marq "adresse-hors-marqueur" 1 oui \
  "la même adresse écrite dans le CORPS bloque toujours — l'exemption s'arrête aux marqueurs"
if [ "$MQ_N" != "$ATTENDU_MARQ" ]; then
  echo "  ✗ $MQ_N témoin(s) joué(s), $ATTENDU_MARQ attendu(s) — un lot amputé passerait au vert,"
  echo "    et l'exemption posée le 25/10 pourrait être retirée ou élargie sans bruit"
  MQ_KO=1
fi
if [ "$MQ_KO" != "0" ]; then
  echo "  ✗ LA PASSE A ET LES MARQUEURS : une correction d'adresse redeviendrait impubliable sans"
  echo "    déformer le libellé d'origine, ou l'exemption aurait débordé du marqueur"
fi
# 🔴 ET SURTOUT PAS « STATUT=1 » ICI : le bloc 4 fait « STATUT=0 » à son entrée, donc un garde posé
#    avant lui est DÉCORATIF. Mesuré le 25/10/2026 : les trois sabotages imprimaient leurs ✗ et le
#    harnais sortait quand même en 0 — la règle du 15/10 (« un garde qui ne fait pas sortir en 1 est
#    décoratif ») dans un garde écrit le lendemain du jour où je l'avais réécrite. MQ_KO est donc
#    reporté APRÈS la réinitialisation, à côté de TEM_KO, qui résout le même problème depuis toujours.

# ── 2. décompte sur les veilles
echo "▶ Décompte sur les veilles…"
: > "$CUR/decompte.tsv"
for f in $(find "$ROOT/sources/veille" -name "*.docx" | sort); do
  env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > /dev/null 2>&1; rc=$?
  printf "%s\t%s\n" "$rc" "${f#$ROOT/sources/veille/}" >> "$CUR/decompte.tsv"
done
echo "  $(cut -f1 "$CUR/decompte.tsv" | sort | uniq -c | awk '{printf "exit %s : %s · ", $2, $1}')"

# ── 3. les quatorze témoins d'avant correction : tous doivent sortir en 1
echo "▶ Témoins d'avant correction (doivent sortir en 1)…"
TEM_KO=0; TEM_N=0
for f in "$NR"/temoins_decompte_avant_correction/*.docx(N); do
  TEM_N=$((TEM_N+1))
  env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > /dev/null 2>&1; rc=$?
  if [ "$rc" != "1" ]; then echo "  ✗ $(basename "$f") sort en $rc au lieu de 1"; TEM_KO=$((TEM_KO+1)); fi
done
if [ "$TEM_N" != "$ATTENDU_DECOMPTE" ]; then
  echo "  ✗ $TEM_N témoin(s) contrôlé(s), $ATTENDU_DECOMPTE attendu(s) — un lot incomplet ne prouve rien :"
  echo "    rétablis le ou les témoins manquants, ou mets ATTENDU_DECOMPTE à jour dans ce script."
  TEM_KO=$((TEM_KO+1))
fi
[ "$TEM_KO" = "0" ] && echo "  ✓ $TEM_N/$ATTENDU_DECOMPTE en exit 1"

# ── 3 bis. les témoins CONFORMES du décompte : tous doivent sortir en 0 (02/10/2026)
echo "▶ Témoins conformes du décompte (doivent sortir en 0)…"
DEC_KO=0; DEC_N=0
for f in "$NR"/temoins_decompte_conformes/*.docx(N); do
  DEC_N=$((DEC_N+1))
  env -i $PY "$ROOT/outils/scripts/controle_decompte.py" "$f" > /dev/null 2>&1; rc=$?
  if [ "$rc" != "0" ]; then echo "  ✗ $(basename "$f") sort en $rc au lieu de 0"; DEC_KO=$((DEC_KO+1)); fi
done
if [ "$DEC_N" != "$ATTENDU_DEC_CONFORMES" ]; then
  echo "  ✗ $DEC_N témoin(s) conforme(s) contrôlé(s), $ATTENDU_DEC_CONFORMES attendu(s) — un lot incomplet"
  echo "    ne prouve rien : rétablis le témoin manquant, ou mets ATTENDU_DEC_CONFORMES à jour."
  DEC_KO=$((DEC_KO+1))
fi
[ "$DEC_KO" = "0" ] && echo "  ✓ $DEC_N/$ATTENDU_DEC_CONFORMES en exit 0"
[ "$DEC_KO" != "0" ] && TEM_KO=$((TEM_KO+DEC_KO))

# ── 4. diff avec la référence
STATUT=0
if [ "$MODE" = "--accepter" ]; then
  mkdir -p "$REF"; cp "$CUR/passe_A.tsv" "$CUR/decompte.tsv" "$REF/"; date "+%d/%m/%Y %H:%M" > "$REF/date.txt"
  echo "▶ Référence enregistrée ($(cat "$REF/date.txt"))."
elif [ -f "$REF/passe_A.tsv" ]; then
  echo "▶ Diff avec la référence du $(cat "$REF/date.txt") :"
  # seuls les documents présents dans LES DEUX passages sont comparés : un document nouveau (un job vient
  # de publier) ou disparu n'est pas une régression — il est listé à part
  D1=$(join -t$'\t' -j1 <(cut -f1,2 "$REF/passe_A.tsv" | sort) <(cut -f1,2 "$CUR/passe_A.tsv" | sort) | awk -F'\t' '$2!=$3{printf "    %s : %s → %s bloquant(s)\n",$1,$2,$3}')
  D2=$(join -t$'\t' -j1 <(awk -F'\t' '{print $2"\t"$1}' "$REF/decompte.tsv" | sort) <(awk -F'\t' '{print $2"\t"$1}' "$CUR/decompte.tsv" | sort) | awk -F'\t' '$2!=$3{printf "    %s : exit %s → %s\n",$1,$2,$3}')
  NOUV=$(comm -13 <(cut -f1 "$REF/passe_A.tsv" | sort) <(cut -f1 "$CUR/passe_A.tsv" | sort) | wc -l | tr -d ' ')
  DISP=$(comm -23 <(cut -f1 "$REF/passe_A.tsv" | sort) <(cut -f1 "$CUR/passe_A.tsv" | sort) | wc -l | tr -d ' ')
  [ "$NOUV" != "0" ] && echo "  ($NOUV document(s) nouveau(x) depuis la référence — non comparés, --accepter pour les y inscrire)"
  [ "$DISP" != "0" ] && echo "  ($DISP document(s) de la référence absent(s) du corpus)"
  if [ -z "$D1" ] && [ -z "$D2" ]; then echo "  ✓ aucun verdict n'a changé"; else
    [ -n "$D1" ] && { echo "  passes A/A2/A3/A4 :"; echo "$D1"; }
    [ -n "$D2" ] && { echo "  décompte :"; echo "$D2"; }
    echo "  → lis chaque ligne ; si le changement est voulu et compris : non_regression.sh --accepter"
    STATUT=1
  fi
else
  echo "▶ Pas encore de référence : non_regression.sh --accepter pour enregistrer ce passage."
fi
[ "$TEM_KO" != "0" ] && STATUT=1
[ "${MQ_KO:-0}" != "0" ] && STATUT=1     # passe A et marqueurs (25/10/2026)

# ── 5. contrôle complet sur les témoins à citations
# RETRY (13/09/2026) : un exit 3 (page non lue — réseau, mur, délai) ne prouve rien sur la passe B ; comme le
# hook ne refuse pas sur un 3, un témoin qui sort en 3 laissait passer un push sans l'avoir testé. On retente
# UNE fois après NR_ATTENTE secondes (60 par défaut) ; un 3 qui persiste est affiché « deux essais » — toujours
# pas un refus (un site qui tombe n'est pas une régression du contrôle), mais on sait que ce passage n'a rien
# prouvé sur B, et il faut relancer --complet à la main.
ATTENTE="${NR_ATTENTE:-60}"
controle_complet() {   # $1 docx, $2 fichier de sortie → rc ; ESSAIS=1|2
  env -i $PY "$ROOT/outils/scripts/controle_attributions.py" "$1" > "$2" 2>&1; local rc=$?; ESSAIS=1
  if [ "$rc" = "3" ]; then
    sleep "$ATTENTE"
    env -i $PY "$ROOT/outils/scripts/controle_attributions.py" "$1" > "$2" 2>&1; rc=$?; ESSAIS=2
  fi
  return $rc
}
if [ "$MODE" = "--complet" ]; then
  # témoins CONFORMES : ils doivent sortir en 0. Les trois premiers sont les documents vivants (stoïcisme 14 :
  # citations anglaises appariées ; appli-ia 07 ; placement 14). S'y ajoutent les copies figées de
  # non_regression/temoins_attributions_conformes/ — chacune protège une passe contre un FAUX POSITIF :
  #   · 2026-09-15_lecon-dzogchen_16 (20/09/2026) : une phrase française prêtée à une page ANGLAISE (Lotsawa House,
  #     Tricycle) ne doit pas bloquer en B-NOM (㉙) — ses chiffres sont sur la page, ses mots français n'y sont pas.
  #     La passe l'a bloqué pendant deux heures le 20/09 et la note de contrôle a prescrit de supprimer des chiffres
  #     exacts. Un témoin qui sort en 1 = le contrôle a poussé une dent de trop.
  echo "▶ Contrôle d'attributions complet (avec aspiration) sur les témoins conformes (doivent sortir en 0)…"
  CONF_N=0
  for f in "$ROOT"/livrables/lecons/**/*stoicisme_14*.docx(N) "$ROOT"/livrables/lecons/**/*appli-ia_07*.docx(N) "$ROOT"/livrables/lecons/**/*placement-financier_14*.docx(N) "$ROOT"/outils/scripts/non_regression/temoins_attributions_conformes/*.docx(N); do
    [ -e "$f" ] || continue
    CONF_N=$((CONF_N+1))
    controle_complet "$f" "$CUR/$(basename "$f" .docx).txt"; rc=$?
    case $rc in 0) l="✓ exit 0";; 3) l="⟳ exit 3 après $ESSAIS essais — pages non lues, rien prouvé sur B : relancer --complet";; *) l="✗ exit $rc — un témoin conforme bloque : faux positif du contrôle"; STATUT=1;; esac
    [ "$ESSAIS" = "2" ] && [ "$rc" != "3" ] && l="$l (au 2e essai)"
    echo "  $l  $(basename "$f")  ($(grep -m1 '^VERDICT' "$CUR/$(basename "$f" .docx).txt" | cut -c1-80))"
    # ⚠️ LA PASSE D N'EST PAS DANS LA RÉFÉRENCE (10/10/2026). passe_A.tsv ne stocke que le NOMBRE de
    #    problèmes bloquants des passes A/A2/A3/A4 : une passe non bloquante est invisible au diff —
    #    même piège que ㉜ le 09/10 et que le motif ② d'ai-act, inerte trois semaines. On exige donc
    #    la LIGNE, dans les DEUX sens, sur ce témoin : il reprend littéralement « 1 782 € » de
    #    lafinancepourtous.com et « 38 400 € x 45 % x (158 / 170) = 16 060,24 € » de service-public.fr,
    #    trois nombres à SÉPARATEUR DE MILLIERS qui sont tous sur leurs pages. Le bug corrigé le
    #    10/10/2026 les rendait tous les trois « A VERIFIER … absente des pages citees », et un nombre
    #    réellement absent sortait avec le même libellé qu'un nombre réellement présent.
    # ⚠️ ㉟ (11/10/2026) : « 50,4 » et « 50,6 » — la période orbitale de Chiron — sont écrits
    #    « 50.4 » et « 50.6 » par le Minor Planet Center. Avant ㉟ la passe D les donnait pour
    #    ABSENTS. Ce témoin ne prouve rien par son code de sortie (il sort en 3, deux de ses
    #    citations étant sur des pages illisibles) : c'est la LIGNE qui est exigée.
    if [[ "$(basename "$f")" == "2026-10-01_lecon-astrologie-karmique_09_locale.docx" ]]; then
      TL="$CUR/$(basename "$f" .docx).txt"
      N_LOC=$(grep -cE "^ +OK +50,[46] +-> .*ecrit « 50\.[46] »" "$TL")
      if [ "$N_LOC" -ge 2 ]; then
        echo "        ↳ ✓ ㉟ tient : $N_LOC nombre(s) français retrouvé(s) sous leur graphie anglaise"
      else
        echo "        ↳ ✗ ㉟ A PERDU SA DENT : « 50,4 » et « 50,6 » ne sont plus appariés à « 50.4 » et"
        echo "          « 50.6 » du Minor Planet Center ($N_LOC/2) — la passe D a reperdu la locale."
        STATUT=1
      fi
    fi
    # ⚠️ ㊱ (15/10/2026) LES GUILLEMETS COURBES. La demande portait sur les guillemets DROITS :
    #    ils étaient déjà appariés depuis l'origine de la boucle de B/B-FR, et la mesure sur la
    #    leçon astrologie-karmique n°11 l'a prouvé — ses trois citations anglaises entre " ont été
    #    vues, deux OK et une en ㉚. Le vrai manque était les COURBES, celles que Word substitue
    #    au ". Sur les 283 documents, UN SEUL perdait des citations de six mots ou plus : celui-ci,
    #    le Manuel d'Épictète, pour cinq d'entre elles.
    #    ⚠️ CE TÉMOIN NE PROUVE RIEN PAR SON CODE DE SORTIE — il sort en 0 AVANT comme APRÈS le
    #    portage, les cinq citations gagnées étant des traductions, donc non appariables et rendues
    #    en « A RELIRE » non bloquant. C'est la LIGNE qui est exigée, comme pour ㉜, D, ㉞ et ㉟.
    #    ⚠️ Et le portage lui-même a d'abord été une RÉGRESSION, mesurée avant commit : ajouter
    #    “ ” à l'alternance fait de “ un délimiteur et TRONQUE les spans « … » qui en contiennent
    #    — 21 documents raccourcis, et une capture tronquée est introuvable sur sa page, donc
    #    « ABSENTE » faux sur une passe BLOQUANTE. D'où un balayage COMPLÉMENTAIRE, qui n'ajoute
    #    que les citations courbes ne chevauchant aucune capture déjà faite : 1 document gagne,
    #    0 ne perd rien, 0 code de sortie ne change.
    if [[ "$(basename "$f")" == "2026-06-25_lecon-stoicisme_04_courbes.docx" ]]; then
      TL="$CUR/$(basename "$f" .docx).txt"
      N_CB=$(grep -cE "A RELIRE (Ce ne sont pas les événements qui troublent|Toute chose a deux anses)" "$TL")
      if [ "$N_CB" -ge 2 ]; then
        echo "        ↳ ✓ ㊱ tient : $N_CB citation(s) entre guillemets courbes “ ” vue(s) par B-FR"
      else
        echo "        ↳ ✗ ㊱ A PERDU SA DENT : les citations d'Épictète entre “ ” sont redevenues"
        echo "          invisibles à B-FR ($N_CB/2) — le balayage complémentaire ne mord plus."
        STATUT=1
      fi
    fi
    # ⚠️ L'EXEMPTION DE ㉞ SE GARDE AUSSI (11/10/2026) : ce témoin est la même leçon, dont le lien
    #    mort est DÉCLARÉ. S'il se mettait à bloquer, ㉞ refuserait un document honnête.
    if [[ "$(basename "$f")" == "2026-06-10_lecon-enneagramme_02_declaree.docx" ]]; then
      if grep -q "LE NOM DE DOMAINE NE RESOUT PAS" "$CUR/$(basename "$f" .docx).txt"; then
        echo "        ↳ ✗ ㉞ MORD À TORT : le lien est déclaré « ⛔ LIEN MORT … NE RESOUT PAS » dans le"
        echo "          document, et A6 le signale quand même — l'exemption de déclaration est cassée."
        STATUT=1
      else
        echo "        ↳ ✓ l'exemption de ㉞ tient : un lien mort déclaré ne bloque pas"
      fi
    fi
    if [[ "$(basename "$f")" == "2026-10-10_lecon-placement-financier_18_passeD.docx" ]]; then
      TD="$CUR/$(basename "$f" .docx).txt"
      # le séparateur est l'une des trois espaces que le contrôle neutralise (normale, insécable, fine) :
      # une virgule ne doit PAS compter, sinon « OK 0,625 » serait pris pour un nombre à séparateur.
      D_OK=$(grep -cE '^ +OK +[0-9]{1,3}[   ][0-9]{3}' "$TD")
      D_KO=$(grep -cE '^ +A VERIFIER [0-9]{1,3}[   ][0-9]{3}' "$TD")
      # ⚠️ SEUIL RAMENÉ DE 3 À 1 LE 11/10/2026, et ce n'est pas un affaiblissement : c'est la
      #    découverte que ce témoin reposait sur du CONTENU DE MARQUEUR. « 38 400 » et
      #    « 16 060,24 » ne figurent, dans ce document, que dans le marqueur du ¶110, qui cite
      #    l'exemple de service-public.fr. Depuis que la passe D écarte les marqueurs comme B et
      #    B-FR le font, elle ne les voit plus — à juste titre. Le seul nombre à séparateur du
      #    CORPS en contexte d'attribution est « 1 782 » (¶26). Exiger 3 reviendrait à exiger que
      #    la passe D relise les marqueurs.
      # 🧪 LA FORCE PERDUE EST REPRISE PAR UNE SECONDE EXIGENCE DE LIGNE : la ligne d'exemption
      #    doit être là ET nommer au moins deux nombres à séparateur. Ce témoin prouve donc
      #    maintenant les DEUX correctifs du même coup — le séparateur de milliers (10/10) et
      #    l'exclusion des marqueurs (11/10).
      D_EXEMPT=$(grep -cE 'valeur\(s\) ecartee\(s\) : elles ne figurent que dans un marqueur' "$TD")
      D_EXSEP=$(grep -oE 'un chiffre cite POUR MEMOIRE.*' "$TD" | grep -oE '[0-9]{1,3}[   ][0-9]{3}' | wc -l | tr -d ' ')
      if [ "$D_OK" -ge 1 ] && [ "$D_KO" = "0" ] && [ "$D_EXEMPT" -ge 1 ] && [ "$D_EXSEP" -ge 2 ]; then
        echo "        ↳ ✓ passe D tient : $D_OK nombre(s) à séparateur apparié(s), 0 donné pour absent,"
        echo "          et $D_EXSEP nombre(s) à séparateur écarté(s) parce qu'ils ne vivent que dans un marqueur"
      else
        echo "        ↳ ✗ PASSE D A PERDU SA DENT : $D_OK apparié(s) (1 au minimum), $D_KO donné(s) pour"
        echo "          absent(s) — « 1 782 » est sur sa page —, ligne d'exemption des marqueurs : $D_EXEMPT,"
        echo "          dont $D_EXSEP nombre(s) à séparateur (2 au minimum : « 38 400 » et « 16 060,24 »,"
        echo "          qui ne vivent que dans le marqueur du ¶110)."
        echo "          Ce témoin sort en 0 de toute façon : la passe D n'est pas bloquante. Lis sa section D."
        STATUT=1
      fi
    fi
  done
  if [ "$CONF_N" != "$ATTENDU_CONFORMES" ]; then
    echo "  ✗ $CONF_N témoin(s) conforme(s) contrôlé(s), $ATTENDU_CONFORMES attendu(s) — un document vivant a changé"
    echo "    de nom ou de dossier, ou une copie figée manque : rétablis-le, ou mets ATTENDU_CONFORMES à jour."
    STATUT=1
  else
    echo "  ✓ $CONF_N/$ATTENDU_CONFORMES témoin(s) conforme(s) contrôlé(s)"
  fi
  # témoins d'AVANT correction pour le contrôle complet : ils doivent sortir en 1 (une citation prêtée à la
  # mauvaise page, ㉓ — veille iMac du 13/09/2026). Un témoin qui sort en 0 = le contrôle a perdu une dent.
  echo "▶ Témoins d'attributions d'avant correction (doivent sortir en 1)…"
  AVANT_N=0
  for f in "$ROOT"/outils/scripts/non_regression/temoins_attributions_avant_correction/*.docx(N); do
    [ -e "$f" ] || continue
    AVANT_N=$((AVANT_N+1))
    controle_complet "$f" "$CUR/temoin_attr_$(basename "$f" .docx).txt"; rc=$?
    case $rc in 1) l="✓ exit 1";; 3) l="⟳ exit 3 après $ESSAIS essais — la page de la source nommée n'a pas été lue, rien prouvé : relancer --complet";; *) l="✗ exit $rc — le témoin ne bloque plus"; STATUT=1;; esac
    [ "$ESSAIS" = "2" ] && [ "$rc" != "3" ] && l="$l (au 2e essai)"
    echo "  $l  $(basename "$f")  ($(grep -m1 'MAL ATTRIBUEE\|^ *INTERDIT\|^ *ABSENTE ' "$CUR/temoin_attr_$(basename "$f" .docx).txt" | cut -c1-90))"
    # ⚠️ UN TÉMOIN QUI SORT EN 1 NE DIT PAS POURQUOI (25/09/2026). Celui de la leçon
    #    appli-ia n°05 a plusieurs défauts : il sortirait en 1 sur sa seule citation
    #    anglaise absente, même si la passe C2 perdait toute sa dent. Or c'est LUI qui
    #    garde C2, la seule passe dont le sens REFUS n'avait aucun témoin permanent.
    #    On exige donc la LIGNE, pas seulement le code de sortie — même exigence que
    #    « lis la sortie, ne te contente pas du code de retour » (JOBS.md, 12/09/2026).
    # ⚠️ MÊME EXIGENCE POUR ㉜ (09/10/2026) : ce témoin sortirait en 1 sur la seule citation de Palmer,
    #    que ㉖ attrape. Ce qui prouve ㉜, c'est la LIGNE qui nomme l'ouvrage.
    if [[ "$(basename "$f")" == "2026-07-08_lecon-enneagramme_06_avant.docx" ]]; then
      if grep -q "SOURCE NOMMÉE SANS PAGE" "$CUR/temoin_attr_$(basename "$f" .docx).txt"; then
        echo "        ↳ ✓ ㉜ tient : $(grep -c "SOURCE NOMMÉE SANS PAGE" "$CUR/temoin_attr_$(basename "$f" .docx).txt") citation(s) prêtée(s) à un ouvrage toujours nommée(s)"
      else
        echo "        ↳ ✗ ㉜ A PERDU SA DENT : aucune citation prêtée à un ouvrage n'est plus signalée."
        echo "          Ce témoin sort en 1 pour la citation de Palmer (㉖) — lis sa sortie complète."
        STATUT=1
      fi
    fi
    # ⚠️ MÊME EXIGENCE POUR ㉞ (11/10/2026) : ce témoin n'a qu'UN défaut, et c'est le lien mort.
    #    S'il sortait en 1 pour autre chose, on ne saurait pas que A6 a perdu le HTTP 000 — d'où la LIGNE.
    if [[ "$(basename "$f")" == "2026-06-10_lecon-enneagramme_02_avant.docx" ]]; then
      if grep -q "LE NOM DE DOMAINE NE RESOUT PAS" "$CUR/temoin_attr_$(basename "$f" .docx).txt"; then
        echo "        ↳ ✓ ㉞ tient : le nom de domaine qui ne résout pas est toujours un lien mort"
      else
        echo "        ↳ ✗ ㉞ A PERDU SA DENT : www.davidstamile.com ne résout pas (HTTP 000, curl 6) et"
        echo "          n'est plus signalé. A6 est redevenue aveugle au 000 — lis sa section A6."
        STATUT=1
      fi
    fi
    if [[ "$(basename "$f")" == "2026-08-28_lecon-appli-ia_05.docx" ]]; then
      if grep -q "INTERDIT   8.2.2" "$CUR/temoin_attr_$(basename "$f" .docx).txt"; then
        echo "        ↳ ✓ C2 tient : « 8.2.2 près de vite.dev/guide » toujours INTERDIT"
      else
        echo "        ↳ ✗ C2 A PERDU SA DENT : « 8.2.2 près de vite.dev/guide » n'est plus refusé."
        echo "          Ce témoin sort peut-être en 1 pour une autre raison — lis sa sortie complète."
        STATUT=1
      fi
    fi
  done
  if [ "$AVANT_N" != "$ATTENDU_AVANT" ]; then
    echo "  ✗ $AVANT_N témoin(s) contrôlé(s), $ATTENDU_AVANT attendu(s) — un lot incomplet ne prouve rien :"
    echo "    rétablis le ou les témoins manquants, ou mets ATTENDU_AVANT à jour dans ce script."
    STATUT=1
  else
    echo "  ✓ $AVANT_N/$ATTENDU_AVANT témoin(s) d'avant correction contrôlé(s)"
  fi

  # ── 5 ter. LES TROIS ÉTAPES 5 BIS SORTIES DES PROMPTS — QUATRE DUOS ─────────
  # `controle_astrologie_karmique.py` (7 motifs) et `controle_psychopathologie.py`
  # (4 motifs) étaient inlinés dans leurs prompts — 12 398 et 5 520 octets réémis à
  # chaque tour. Sortis le 08/10/2026, ils sont devenus des scripts du dépôt que
  # PLUS AUCUN HARNAIS NE TESTAIT : une retouche de l'un des deux ne se serait vue
  # nulle part. Chacun se prouve ici DANS LES DEUX SENS.
  #   • un témoin CONFORME doit sortir en 0 (le contrôle laisse passer ce qui est juste) ;
  #   • une MUTATION du même document, fabriquée par muter_docx.py et détruite après,
  #     doit sortir en 1 (le contrôle mord encore).
  # ⚠️ POURQUOI UNE MUTATION ET PAS UN TÉMOIN FIGÉ DE REFUS. Au 08/10/2026, les seuls
  # documents que controle_astrologie_karmique.py refusait le faisaient sur SIX FAUX POSITIFS
  # du motif ⑤ — des exonymes français (« Cérès » pour « Ceres », « Alger » pour « Algiers »,
  # « Centre » pour « Center ») et l'étiquette de section « Citation » ; figer un de ces refus
  # aurait inscrit le bug dans le harnais, qui aurait échoué le jour de sa correction. 🟢 CE
  # JOUR EST ARRIVÉ LE 09/10/2026 : le correctif du prompt `stoicisme` a été porté, les six
  # faux positifs ont disparu, et la leçon n°10 sort désormais en 0. Le raisonnement ci-dessus
  # est donc HISTORIQUE — mais la mutation reste le bon instrument, pour une autre raison : un
  # témoin figé de refus prouve qu'un contrôle refuse encore un document DONNÉ, la mutation
  # prouve qu'il refuse encore une FAUTE, et c'est elle qui survit à une correction du document.
  # ⚠️ ET LA MUTATION DOIT TOMBER LÀ OÙ LE MOTIF REGARDE. Le motif ⑤ n'examine que les
  # paragraphes qui portent un lien dont la page répond 200 : un paragraphe AJOUTÉ en fin de
  # document ne l'atteint jamais. D'où le motif « nompropre », qui MODIFIE le premier paragraphe
  # à la fois lié et porteur d'un marqueur de source. Mesuré le 09/10/2026 : il sort en 1 sur le
  # seul motif ⑤.
  # ⚠️ EN --complet SEULEMENT : ces scripts rouvrent CHAQUE page listée du document (dix
  # pour la leçon d'astrologie, dont quatre fiches du MPC de 600 000 à 900 000 caractères ;
  # douze pour la veille ai-act, en 5 s). En --docs, qui est la porte des pushs de job et
  # doit rester en secondes, ils n'ont rien à faire.
  # 🆕 09/10/2026 — TROISIÈME DUO : controle_ai_act.py (11 motifs, 12 303 octets), sorti du
  # prompt d'ai-act-veille le même jour. Sa mutation est « alerte » : un paragraphe
  # « 🟢 Niveau d'alerte : VERT » injecté dans une note qui annonce des faits marquants,
  # ce qui déclenche son motif (6) — le seul des onze qui ne coûte AUCUN appel réseau.
  # ⚠️ ET CE CÂBLAGE A RÉVÉLÉ UN BUG DE muter_docx.py, resté invisible depuis le 08/10 :
  # sa branche « document portant un journal des corrections » insérait la mutation entre
  # <w:p> et <w:pPr> du paragraphe du titre, qui n'était alors plus un <w:p>…</w:p>
  # complet ; plus aucun paragraphe ne contenait « Journal des corrections », et le
  # contrôle lisait tout le journal. Le mutant restait un XML valide, donc rien ne le
  # disait, et le témoin d'astrologie n°09 — qui porte un journal — passait depuis deux
  # jours sur un document malformé. Corrigé : on repère le SPAN du paragraphe, et
  # muter_docx.py vérifie désormais l'XML, l'équilibre des <w:p> et la position de la
  # mutation avant le journal.
  echo "▶ Étapes 5 bis du dépôt (témoin conforme en 0, mutation en 1)…"
  # Quatre duos pour trois scripts : l'astrologie en a DEUX, et SUR DEUX DOCUMENTS DIFFÉRENTS.
  #   • n°09 + « ligature » → prouve que le motif ① mord ;
  #   • n°10 + « nompropre » → prouve que le motif ⑤ mord.
  # ⚠️ LE CHOIX DE LA n°10 N'EST PAS INDIFFÉRENT, c'est lui qui garde le correctif des exonymes
  # dans L'AUTRE SENS. La n°10 est le document qui portait les six faux positifs du motif ⑤ ;
  # elle sort en 0 depuis le portage du 09/10/2026, et elle est la SEULE chose du dépôt qui
  # retomberait en 1 si quelqu'un défaisait sa (sa(), EXO_, STRUCT_). Une mutation prouve qu'un
  # contrôle MORD ; un témoin conforme bien choisi prouve qu'il NE MORD PAS À TORT — il fallait
  # les deux, et c'est pourquoi ce duo-là ne réutilise pas le témoin de « ligature ».
  # Coût : 11 s par passage du contrôle astro, mesuré — négligeable sur un --complet de 7 min.
  # 6 depuis le 10/10/2026 : deux duos ajoutés sur controle_ai_act.py en portant norm4 — « citation »
  # (le motif (1) doit continuer à refuser une citation fabriquée) et « 0:typo » (il ne doit PAS
  # refuser une citation que la page écrit avec une espace avant sa ponctuation).
  ATTENDU_5BIS=7
  CB_N=0
  CB_SKIP=0
  MUTDIR=$(mktemp -d "${TMPDIR:-/tmp}/nr5bis.XXXXXX")
  # Le chemin du témoin est relatif à la racine du dépôt : le troisième duo est une VEILLE,
  # pas une leçon, et l'ancien préfixe livrables/lecons/ était codé en dur (09/10/2026).
  for duo in \
    "controle_astrologie_karmique.py|livrables/lecons/astrologie-karmique/2026-10-01_lecon-astrologie-karmique_09_chiron-corps-reel-blessure-symbolique.docx|ligature" \
    "controle_psychopathologie.py|livrables/lecons/psychopathologie/2026-10-05_lecon-psychopathologie_19_ethique-consentement-contrainte-sante-mentale.docx|fraction" \
    "controle_ai_act.py|sources/veille/ai-act/2026-10-09_veille_ai-act.docx|alerte" \
    "controle_astrologie_karmique.py|livrables/lecons/astrologie-karmique/2026-10-08_lecon-astrologie-karmique_10_lilith-points-fictifs-statut-objets.docx|nompropre" \
    "controle_ai_act.py|sources/veille/ai-act/2026-10-09_veille_ai-act.docx|citation" \
    "controle_ai_act.py|sources/veille/ai-act/2026-10-09_veille_ai-act.docx|0:typo" \
    "controle_ai_act.py|sources/veille/ai-act/2026-10-09_veille_ai-act.docx|taille"; do
    SC="${duo%%|*}"; RESTE="${duo#*|}"; REL="${RESTE%%|*}"; MOTIF="${RESTE##*|}"
    # ⚠️ CONVENTION « 0:motif » (10/10/2026) : le mutant doit être ACCEPTÉ, pas refusé. Un
    #    normaliseur qu'on ÉLARGIT doit se prouver DANS LES DEUX SENS — une mutation qui doit
    #    sortir en 1 garde sa dent, une mutation qui doit sortir en 0 garde l'élargissement.
    #    Sans la seconde, rien n'empêche de resserrer le normaliseur demain : les quatre autres
    #    duos continueraient de passer.
    ATTENDU_MUT=1
    case "$MOTIF" in 0:*) ATTENDU_MUT=0; MOTIF="${MOTIF#0:}";; esac
    DOC="$ROOT/$REL"
    if [ ! -f "$DOC" ] || [ ! -f "$ROOT/outils/scripts/$SC" ]; then
      echo "  ✗ $SC : témoin ou script introuvable ($REL) — rétablis-le, ou mets ce bloc à jour."
      STATUT=1; continue
    fi
    CB_N=$((CB_N + 1))
    env -i /usr/bin/python3 "$ROOT/outils/scripts/$SC" "$DOC" > "$CUR/5bis_$MOTIF.txt" 2>&1; rc=$?
    # ⚠️ 27/10/2026 — L'ALERTE DU CONTRÔLE EST REMONTÉE ICI, SANS QUOI PERSONNE NE LA LIT. Ce
    #    bloc CAPTURE la sortie des 5 bis dans un fichier et n'imprime qu'un ✓/✗ ; et le job
    #    psychopathologie est supprimé depuis le 15/10, donc aucune exécution planifiée ne lit
    #    plus cette sortie. Une alerte que rien ne remonte est décorative — règle du 15/10.
    #    NON BLOQUANTE : la cause serait le gabarit d'un TIERS, pas une régression du dépôt.
    grep -h 'ALERTE ÉTIQUETTE HAS' "$CUR/5bis_$MOTIF.txt" 2>/dev/null | sed 's/^/  ⚠ /'
    if [ "$rc" != "0" ]; then
      # ⟳ TOLÉRANCE « PAGE NON LUE » (25/10/2026) — voir le bloc 0 sexies et l'en-tête du script
      #   appelé. Quatre conditions, toutes nécessaires : synthèse de refus de forme connue ·
      #   AUTANT de lignes nommant une page QUE de motifs annoncés · chaque page dans les rels DU
      #   TÉMOIN (un contrôle saboté qui imprimerait une excuse ne s'excuse pas) · injoignable
      #   MESURÉE ici, faisceau compris. Le sens d'échec du comptage est le refus.
      # ⚠️ Et la mutation n'est PAS jouée : son verdict dépend des mêmes pages. Un duo non joué
      #   est un duo NON GARDÉ — c'est assumé, et compté ligne par ligne plus bas.
      if TOL=$(env -i $PY "$NR/tolerance_page_morte.py" "$CUR/5bis_$MOTIF.txt" "$DOC" 2>&1); then
        echo "  ⟳ $SC : duo « $MOTIF » NON JOUÉ — $TOL"
        CB_SKIP=$((CB_SKIP + 1))
      else
        echo "  ✗ $SC : le témoin conforme sort en $rc — faux positif du contrôle : $(tail -1 "$CUR/5bis_$MOTIF.txt")"
        echo "    (tolérance « page non lue » REFUSÉE : $TOL)"
        STATUT=1
      fi
    else
      MUT="$MUTDIR/mutant_$MOTIF.docx"
      if ! /usr/bin/python3 "$NR/muter_docx.py" "$DOC" "$MUT" "$MOTIF" > /dev/null 2>&1; then
        echo "  ✗ $SC : la mutation « $MOTIF » n'a pas pu être fabriquée — rien n'est prouvé."
        STATUT=1
      else
        env -i /usr/bin/python3 "$ROOT/outils/scripts/$SC" "$MUT" > "$CUR/5bis_mut_$MOTIF.txt" 2>&1; rcm=$?
        if [ "$rcm" = "$ATTENDU_MUT" ]; then
          echo "  ✓ $SC : témoin conforme exit 0, mutation « $MOTIF » exit $ATTENDU_MUT$([ "$ATTENDU_MUT" = "0" ] && echo " (acceptation attendue)")"
        elif [ "$ATTENDU_MUT" = "0" ]; then
          echo "  ✗ $SC : la mutation « $MOTIF » sort en $rcm au lieu de 0 — LE CONTRÔLE MORD À TORT"
          echo "    (une citation que la page écrit avec une espace avant sa ponctuation est refusée :"
          echo "     le portage de norm4 a été défait, ou resserré)"
          echo "    $(tail -1 "$CUR/5bis_mut_$MOTIF.txt")"
          STATUT=1
        else
          echo "  ✗ $SC : la mutation « $MOTIF » sort en $rcm au lieu de 1 — LE CONTRÔLE NE MORD PLUS"
          echo "    $(tail -1 "$CUR/5bis_mut_$MOTIF.txt")"
          STATUT=1
        fi
      fi
      rm -f "$MUT"
    fi
  done
  rmdir "$MUTDIR" 2>/dev/null
  if [ "$CB_N" != "$ATTENDU_5BIS" ]; then
    echo "  ✗ $CB_N étape(s) 5 bis contrôlée(s), $ATTENDU_5BIS attendue(s) — un lot incomplet ne"
    echo "    prouve rien : rétablis le script ou le témoin manquant, ou mets ATTENDU_5BIS à jour."
    STATUT=1
  fi
  # ⚠️ UN DUO NON JOUÉ NE SE TAIT PAS. L'excuse évite un faux refus, elle ne prouve rien : pendant
  #    la panne d'un tiers, les motifs de ce duo ne sont plus gardés DU TOUT. Dit à chaque passage.
  if [ "$CB_SKIP" != "0" ]; then
    echo "  ⚠️ $CB_SKIP duo(s) 5 bis non joué(s) sur $CB_N — page(s) injoignable(s) côté tiers, mesurée(s)"
    echo "     par le harnais : ces motifs ne sont PAS gardés dans ce passage. Rejoue --complet quand"
    echo "     le site répond, avant de croire le bloc 5 bis vert."
  fi

  # ── 5 ter bis. DÉLIMITATION DES BLOCS D'ARTICLE DE controle_ai_act.py (16/10/2026) ──
  # Le motif (2) confrontait au lien de SON bloc des noms d'actes et des citations
  # appartenant aux blocs SUIVANTS : le corps d'un bloc s'arrêtait à la première ligne vide,
  # or la veille du 16/10 n'en met aucune entre ses articles. Le corps de l'« Article 1 »
  # courait sur 10 569 caractères au lieu de 1 392, et la note recevait DEUX refus bloquants
  # pour des chaînes qui ne sont pas les siennes — dont « Publication 09 October 2026 », que
  # la passe B-FR appariait en OK au même moment sur la bonne page. Les deux contrôles se
  # contredisaient, et c'était celui-ci qui avait tort.
  # ⚠️ CE TÉMOIN NE PEUT PAS ÊTRE JUGÉ SUR SON SEUL CODE DE SORTIE : il sort en 1 AVANT comme
  #    APRÈS le correctif, puisqu'il garde un refus légitime — « EU AI Act » prêté à un
  #    article qui parle de l'« EU AI Office ». C'est la LIGNE qui est exigée, et dans LES
  #    DEUX SENS : une ligne INTERDITE (le lien de l'Article 1, qui ne doit plus apparaître
  #    dans aucun refus) et une ligne REQUISE (le refus légitime, qui doit subsister).
  #    Sans la ligne interdite, on ne saurait pas que le saignement de bloc est revenu ;
  #    sans la ligne requise, un motif entièrement mort passerait pour corrigé.
  echo "▶ Délimitation des blocs d'article de controle_ai_act.py (16/10/2026)"
  BL_D="$ROOT/outils/scripts/non_regression/temoins_ai_act_blocs"
  BL_F="$BL_D/2026-10-16_veille_ai-act_blocs.docx"
  if [ -f "$BL_F" ]; then
    BL_OUT="$CUR/ai_act_blocs.txt"
    env -i $PY "$ROOT/outils/scripts/controle_ai_act.py" "$BL_F" > "$BL_OUT" 2>&1
    BL_RC=$?
    # ⚠️ DEUX LIGNES INTERDITES — une par saignement, car il y en avait DEUX :
    #    ① le lien de l'« Article 1 », quand le corps courait jusqu'à la première ligne vide ;
    #    ② tout « ACTE NOMMÉ ABSENT », car l'acte « EU AI Act » venait du titre d'une AUTRE
    #       source avalée par le dernier bloc. Cette copie figée n'a aucun refus d'acte juste.
    # ET UNE LIGNE REQUISE : le refus d'héritage, qui est le VRAI défaut que cette copie
    #    conserve — le paragraphe DDADUE sans lien ni « non vérifié ». Sans elle, un motif
    #    entièrement mort passerait pour corrigé.
    BL_SAIGNE=$(grep -c "special-meeting-ai-scientific-panel" "$BL_OUT")
    BL_ACTE=$(grep -c "ACTE NOMMÉ ABSENT" "$BL_OUT")
    BL_VRAI=$(grep -c "HÉRITAGE SANS SOURCE NI RÉSERVE" "$BL_OUT")
    if [ "$BL_RC" = 1 ] && [ "$BL_SAIGNE" = 0 ] && [ "$BL_ACTE" = 0 ] && [ "$BL_VRAI" -ge 1 ]; then
      echo "  ✓ les blocs tiennent : aucun refus prêté à un autre bloc, et le vrai défaut subsiste"
    else
      [ "$BL_SAIGNE" != 0 ] && echo "  ✗ LE SAIGNEMENT DE BLOC EST REVENU : $BL_SAIGNE refus prêté(s) au lien de"
      [ "$BL_SAIGNE" != 0 ] && echo "    l'Article 1 pour des chaînes qui appartiennent aux blocs suivants."
      [ "$BL_ACTE" != 0 ] && echo "  ✗ $BL_ACTE refus d'ACTE : le dernier bloc avale de nouveau le titre d'une"
      [ "$BL_ACTE" != 0 ] && echo "    autre source (« Timeline for the Implementation of the EU AI Act »)."
      [ "$BL_VRAI" = 0 ] && echo "  ✗ le vrai défaut a disparu : le paragraphe DDADUE sans lien ni « non vérifié »"
      [ "$BL_VRAI" = 0 ] && echo "    n'est plus refusé — le motif (5) ne mord plus du tout."
      [ "$BL_RC" != 1 ] && echo "  ✗ code de sortie $BL_RC, 1 attendu"
      STATUT=1
    fi
  else
    echo "  ✗ témoin absent : $BL_F"
    STATUT=1
  fi

  # ── 5 quater. RELECTURE À L'ÉDITION PRÉCÉDENTE ET À SA FICHE (12/10/2026) ────
  # `controle_edition_precedente.py` est le premier contrôle du dépôt qui regarde AILLEURS que
  # dans le document qu'on lui donne. Il n'est donc PAS dans la référence (passe_A.tsv ne stocke
  # que les passes A/A2/A3/A4 d'un document isolé) : comme ㉜, la passe D, ㉞ et ㉟, il lui faut
  # son témoin et une EXIGENCE DE LIGNE.
  # LE DUO EST UN VRAI INCIDENT, FIGÉ DANS LES DEUX ÉTATS. L'entrée 7 du journal de la veille
  # iMac du 04/10/2026 retirait « TSMC » du procédé du M6, « le fondeur n'étant pas nommé sur la
  # page citée ». L'édition du 11/10 l'a réécrit « 2 nm (TSMC N2) » — correction défaite, sept
  # jours plus tard, dans le document même que la note avait relu pour sa continuité.
  #   • temoins_edition_precedente/rejeu/      : le 11/10 AVANT correction → doit sortir en 1
  #     ET porter la ligne « INTERDIT « TSMC » ». Sans la ligne, n'importe quel autre jeton
  #     ferait passer le témoin : le code de sortie seul ne prouve pas QUEL rejeu est vu.
  #   • temoins_edition_precedente/conforme/   : le 11/10 APRÈS correction → doit sortir en 0.
  # Chaque dossier porte sa propre copie de l'édition N-1 et de la FICHE de celle-ci, puisque le
  # contrôle les cherche à côté du document : deux fichiers de même nom ne peuvent pas cohabiter.
  echo "▶ Relecture à l'édition précédente (rejeu en 1 avec sa ligne, conforme en 0)…"
  # 🔴 TROISIÈME TÉMOIN AJOUTÉ LE 14/10/2026, APRÈS UN FAUX REFUS EN PRODUCTION. Le contrôle a
  # refusé trois fois le push du job serafin-ph-veille du 14/10 sur deux jetons — « Inaccessible »
  # (de « ⛔ Inaccessible (404) ») et « Semaine » (de « Semaine creuse ») : deux mots ordinaires,
  # capitalisés parce qu'ils ouvrent une cellule, et que la série emploie chaque semaine. La borne a
  # été resserrée (dénonciation EXIGÉE, et jeton hors tête de citation). ⚠️ ET LES DEUX TÉMOINS
  # EXISTANTS NE GARDENT PAS CE RESSERREMENT : sabotage vérifié le 14/10/2026 — en retirant
  # l'exigence de dénonciation, « rejeu » sort toujours en 1 AVEC sa ligne TSMC et « conforme »
  # toujours en 0, tandis que la paire SERAFIN rebascule en 1. C'est la même leçon que la convention
  # « 0: » du 10/10 : un motif qu'on RESSERRE a besoin d'un témoin qui doit être ACCEPTÉ, sinon rien
  # n'empêche de le réélargir demain et de refuser à nouveau un livrable juste.
  # 🔴 QUATRIÈME ET CINQUIÈME TÉMOINS, LE 19/10/2026 — DEUXIÈME FAUX REFUS EN PRODUCTION.
  # Le motif ① a refusé trois fois le push de la veille has-actualite du 19/10 sur le jeton
  # « Commission », retiré du corps du 12/10 par une correction JUSTE (la note y attribuait trois
  # validations « à la Commission en charge du social et du médico-social (CSMS) », qu'aucune page
  # n'écrivait). Le 19/10 écrit « Commission de la transparence (21/10) — hors secteur social &
  # médico-social », fait EXACT et vérifié sur le calendrier HAS. Les deux axes du 14/10 ne
  # séparaient pas ce cas : la citation EST dénoncée, le jeton n'est PAS en tête.
  # LA BORNE RETENUE — un jeton revenu ne bloque que s'il revient ACCOMPAGNÉ d'un autre mot de sa
  # citation à moins de 80 caractères, le vocabulaire de la série étant écarté (un mot présent 5
  # fois ou plus dans le corps de N-1). Trois autres bornes ont été mesurées puis abandonnées,
  # dont une qui cassait le témoin FONDATEUR : le détail est dans l'en-tête du contrôle.
  # LES DEUX NOUVEAUX TÉMOINS SONT LES DEUX CÔTÉS DE CETTE BORNE, et le second DOIT ÊTRE ACCEPTÉ :
  #   • rejeu_2031/            : la veille imac du 18/10 AVANT correction → 1, avec sa ligne
  #     « INTERDIT « 2031 » » — le vrai rejeu, où « Microsoft » accompagne à 47 caractères ;
  #   • faux_refus_commission/ : la veille has-actualite du 19/10 → 0, avec sa ligne
  #     « À RELIRE « Commission » » — le mot revient SEUL, le seul accompagnateur non calendaire
  #     étant « CSMS » à 128 caractères. Sans l'exigence de ligne, un retour au blocage
  #     inconditionnel laisserait ce témoin vert sur un simple exit 0 impossible à distinguer.
  ATTENDU_EDPREC=5
  EP_N=0; EPD="$NR/temoins_edition_precedente"
  for cas in "rejeu|1|INTERDIT « TSMC »|2026-10-11_veille_imac.docx|2026-10-04_veille_imac" \
             "conforme|0||2026-10-11_veille_imac.docx|2026-10-04_veille_imac" \
             "faux_refus|0||2026-10-14_veille_SERAFIN-PH.docx|2026-10-07_veille_SERAFIN-PH" \
             "rejeu_2031|1|INTERDIT « 2031 »|2026-10-18_veille_imac.docx|2026-10-11_veille_imac" \
             "faux_refus_commission|0|À RELIRE « Commission »|2026-10-19_veille_has-actualite.docx|2026-10-12_veille_has-actualite"; do
    NOM="${cas%%|*}"; RST="${cas#*|}"; ATT="${RST%%|*}"; RST2="${RST#*|}"
    LIGNE="${RST2%%|*}"; RST3="${RST2#*|}"; FICH="${RST3%%|*}"; PREC="${RST3##*|}"
    DOC="$EPD/$NOM/$FICH"
    if [ ! -f "$DOC" ] || [ ! -f "$EPD/$NOM/$PREC.docx" ] \
       || [ ! -f "$EPD/$NOM/$PREC.fiche.md" ]; then
      echo "  ✗ témoin « $NOM » incomplet — il lui faut l'édition N, l'édition N-1 et la fiche de N-1."
      STATUT=1; continue
    fi
    EP_N=$((EP_N + 1))
    env -i /usr/bin/python3 "$ROOT/outils/scripts/controle_edition_precedente.py" "$DOC" \
        > "$CUR/edprec_$NOM.txt" 2>&1; rc=$?
    if [ "$rc" != "$ATT" ]; then
      echo "  ✗ témoin « $NOM » sort en $rc au lieu de $ATT — $(tail -1 "$CUR/edprec_$NOM.txt")"
      [ "$ATT" = "1" ] && echo "    LA RELECTURE NE MORD PLUS : une correction défaite ne serait plus vue."
      [ "$ATT" = "0" ] && echo "    LA RELECTURE MORD À TORT : une édition honnête serait refusée$([ "$NOM" = "faux_refus" ] && echo " — c'est le faux refus du 14/10/2026 qui revient")."
      STATUT=1
    elif [ -n "$LIGNE" ] && ! grep -q "$LIGNE" "$CUR/edprec_$NOM.txt"; then
      echo "  ✗ témoin « $NOM » sort bien en 1, mais SANS la ligne « $LIGNE » :"
      echo "    le code de sortie ne dit pas QUEL rejeu est vu — le jeton attendu n'est plus détecté."
      STATUT=1
    else
      echo "  ✓ témoin « $NOM » exit $ATT$([ -n "$LIGNE" ] && echo " avec sa ligne « $LIGNE »")"
    fi
  done
  if [ "$EP_N" != "$ATTENDU_EDPREC" ]; then
    echo "  ✗ $EP_N témoin(s) de relecture contrôlé(s), $ATTENDU_EDPREC attendu(s) — rétablis le"
    echo "    dossier manquant, ou mets ATTENDU_EDPREC à jour."
    STATUT=1
  fi
fi
# ---- Témoins de ㊳ : livrable issu d'un run échoué (16/10/2026) ----
# ㊳ est BLOQUANT depuis le 16/10, et sa seule porte de sortie est une DÉCLARATION du
# document lui-même. Les deux sens se prouvent donc, et le code de sortie suffit ici —
# contrairement à la plupart des motifs du dépôt, celui-ci n'a qu'un verdict binaire.
# ⚠️ Le sens REFUS se joue sur une copie placée dans un chemin qui s'apparie au job : le
#    contrôle lie un document à son run par la DATE de son nom et le dossier de sa série.
#    La copie figée réutilisée est celle de temoins_ai_act_blocs, qui date d'AVANT la
#    correction du 16/10 — elle n'a donc aucun journal, donc aucune déclaration. Aucun
#    nouveau témoin n'est figé pour cela.
if [ "$MODE" != "--docs" ] && [ -x "$ROOT/outils/scripts/controle_livrable_du_job.py" ]; then
  echo "▶ Témoins de ㊳ (livrable d'un run échoué : refusé, sauf s'il le déclare)"
  LJ_KO=0
  LJ_VIVANT="$ROOT/sources/veille/ai-act/2026-10-16_veille_ai-act.docx"
  LJ_FIGE="$ROOT/outils/scripts/non_regression/temoins_ai_act_blocs/2026-10-16_veille_ai-act_blocs.docx"
  if [ -f "$LJ_VIVANT" ] && [ -f "$LJ_FIGE" ]; then
    # sens ACCEPTANT : le document corrigé DÉCLARE son échec et sa relecture
    LJ_A="$CUR/lj_accepte.txt"
    if env -i $PY "$ROOT/outils/scripts/controle_livrable_du_job.py" "$LJ_VIVANT" > "$LJ_A" 2>&1 \
       && grep -q "DÉCLARÉ par le document" "$LJ_A"; then
      echo "  ✓ sens acceptant : le livrable qui DÉCLARE son échec et sa relecture passe"
    else
      echo "  ✗ sens acceptant : un livrable qui déclare tout ce qu'il faut est REFUSÉ —"
      echo "    ㊳ bloquant sans exemption praticable est un piège, pas un garde."
      LJ_KO=1
    fi
    # sens REFUS : la copie d'avant correction ne déclare rien
    LJ_T="$CUR/sources/veille/ai-act"
    mkdir -p "$LJ_T"
    cp "$LJ_FIGE" "$LJ_T/2026-10-16_veille_ai-act.docx"
    LJ_R="$CUR/lj_refuse.txt"
    if env -i $PY "$ROOT/outils/scripts/controle_livrable_du_job.py" \
         "$LJ_T/2026-10-16_veille_ai-act.docx" > "$LJ_R" 2>&1; then
      echo "  ✗ sens refus : un livrable d'un run ÉCHOUÉ sans aucune déclaration PASSE —"
      echo "    ㊳ ne mord plus, et rien n'empêche de publier ce que personne n'a vérifié."
      LJ_KO=1
    elif ! grep -q "REFUSÉ" "$LJ_R"; then
      echo "  ✗ sens refus : exit 1 obtenu mais sans la ligne « REFUSÉ » — on ne saurait pas"
      echo "    POURQUOI le push est bloqué, et un refus muet se contourne au lieu de se lire."
      LJ_KO=1
    else
      echo "  ✓ sens refus : le livrable d'un run échoué qui ne déclare rien est refusé"
    fi
    [ "$LJ_KO" = 1 ] && STATUT=1
  else
    echo "  ✗ témoin(s) absent(s) — le vivant ou la copie figée manque"
    STATUT=1
  fi
fi

# ---- Témoins de supprimer_job.sh (15/10/2026) ----
# supprimer_job.sh exécute les SIX gestes d'une suppression de job, et son GARDE-FOU est la
# seule chose qui l'empêche de partir trop tôt : il appelle controle_clauses_parcours.py et
# refuse tant que les leçons réelles sont sous le compte annoncé. Sans témoin, personne ne
# saurait que ce garde-fou a cessé de mordre — et le prix d'un garde-fou muet est un BILAN
# de parcours jamais produit, comme l'inverse a déjà coûté une 11e leçon à revenus-passifs.
# ⚠️ CES TÉMOINS N'EXERCENT QUE LES DIRECTIONS LISIBLES SEULES, et c'est délibéré : le chemin
#    --confirmer écrit dans jobs_config.json, relance setup_launchd.sh et retire un .plist du
#    HOME. Le jouer ici endommagerait launchd pour de vrai. CE QUI RESTE DONC NON COUVERT :
#    que les six gestes soient tous accomplis. Cela a été validé à la main le 15/10/2026 sur
#    les trois suppressions du jour, et l'est à chaque usage par les vérifications finales du
#    script (config, .plist et launchctl doivent concorder ; ids du skill = ids de la config).
# Sans réseau, sans jeton, moins d'une seconde. Pas en --docs : c'est la porte des documents.
if [ "$MODE" != "--docs" ] && [ -x "$ROOT/outils/scripts/supprimer_job.sh" ]; then
  echo "▶ Témoins de supprimer_job.sh (le garde-fou doit refuser avant le bilan)"
  SJ="$ROOT/outils/scripts/supprimer_job.sh"
  SJ_KO=0
  # LES DEUX CONFIGS SONT FABRIQUÉES ICI puis détruites, comme une mutation : l'une déclare
  # pour le parcours témoin le nombre de leçons RÉELLEMENT sur le disque (parcours complet,
  # le garde-fou doit laisser passer), l'autre ce nombre PLUS UN (parcours incomplet, il doit
  # refuser). Un témoin figé se périmerait à chaque leçon.
  # 🔴 22/10/2026 — ET C'EST EXACTEMENT CE QUI EST ARRIVÉ AU SCÉNARIO DE REFUS. Il tournait
  #    contre la config RÉELLE et sur `astrologie-karmique-lecon`, dont le parcours était à
  #    11/12 le jour où ces témoins ont été écrits : il exigeait « exit 1 · il manque ». Le
  #    bilan livré le 22/10 à 9h33 a porté le parcours à 12/12, le garde-fou a — correctement
  #    — laissé passer, et le témoin a crié « exit 0, 1 attendu ». LE HARNAIS EST ALORS SORTI
  #    EN 1 ET BLOQUAIT TOUS LES PUSHS DU DÉPÔT, comme le motif ⑩ de controle_ai_act le 15/10.
  #    Mesuré au même endroit, version HEAD et version corrigée : plan identique, exit 0 pour
  #    les deux — le témoin s'était périmé seul, aucun code n'avait changé. Troisième fois que
  #    « un témoin VIVANT qui annote une propriété volatile périme tout seul » se vérifie.
  #    ⚠️ Et les cinq scénarios étaient ancrés sur le job qu'on allait SUPPRIMER : la
  #    suppression seule les aurait tous fait répondre « job inconnu ». D'où le job témoin
  #    ci-dessous, qui doit être un parcours de leçons ENCORE dans la config.
  # ⚠️ 17/10/2026 — ON COMPARE AVANT/APRÈS, PAS À UN ARBRE PROPRE. La première version
  #    exigeait que les quatre fichiers soient NON MODIFIÉS dans l'arbre de travail : elle
  #    confondait « sale » et « sali par le test ». Mesuré ce jour : l'édition des prompts de
  #    trois jobs rendait jobs_config.json modifié, et le témoin criait « les appels de plan
  #    ont MODIFIÉ 1 fichier(s) » — un faux refus qui bloquait le push de ce correctif même.
  #    Ce qu'il faut vérifier, c'est que les appels de plan ne changent RIEN : on photographie
  #    l'état avant, on le rephotographie après, et on compare les deux.
  SJ_AV=$(cd "$ROOT" && git status --porcelain jobs_config.json outils/scripts/run_job.sh \
          outils/scripts/setup_launchd.sh .claude/skills/lancer-job/SKILL.md 2>/dev/null); SJ_AVE=$?
  SJ_JOBT="hypnose-lecon"
  SJ_CFG="$CUR/cfg_parcours_complet.json"
  SJ_CFGI="$CUR/cfg_parcours_incomplet.json"
  env -i $PY - "$ROOT" "$SJ_CFG" "$SJ_CFGI" "$SJ_JOBT" <<'PYSJ' || { echo "  ✗ configs de test non fabriquées"; SJ_KO=1; }
import glob, json, re, subprocess, sys
racine, complet, incomplet, jid = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
parcours = re.sub(r"-lecon$", "", jid)
n = len(glob.glob(racine + "/livrables/lecons/" + parcours + "/*.docx"))
assert n > 0, "aucune leçon sur le disque pour " + parcours
# 🔴 22/10/2026 — ON RÉÉCRIT LES TROIS FORMES QUE LE CONTRÔLE SAIT LIRE, PAS UNE DEVINÉE.
#    Première version : re.subn(r"\b\d+ LEÇONS"). Elle rendait 1 substitution — donc
#    « réussie » — et controle_clauses_parcours.py lisait toujours « annoncé 20 », parce que
#    son annonce() cherche « en N LEÇONS », « (N leçons) » ou « — N leçons : », et que ce job
#    porte la DEUXIÈME. Une substitution qui compte ses coups ne prouve pas qu'elle a touché
#    ce que le lecteur lit : d'où la VÉRIFICATION DE BOUT EN BOUT ci-dessous, qui rappelle le
#    contrôle sur la config fabriquée et exige le compte voulu.
FORMES = ((r"en\s+\d+\s+LEÇONS", "en %d LEÇONS"), (r"\(\d+\s+leçons\)", "(%d leçons)"),
          (r"—\s*\d+\s+leçons\s*:", "— %d leçons :"), (r"limite de \d+", "limite de %d"))
for cible, annonce in ((complet, n), (incomplet, n + 1)):
    d = json.load(open(racine + "/jobs_config.json", encoding="utf-8"))
    vus = 0
    for x in d["jobs"]:
        if x["id"] == jid:
            total = 0
            for motif, remp in FORMES:
                x["prompt"], k = re.subn(motif, remp % annonce, x["prompt"], flags=re.I)
                total += k
            assert total, "aucune forme de compte annoncé trouvée dans %s" % jid
            vus += 1
    assert vus == 1, "%s absent de la config" % jid
    json.dump(d, open(cible, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    vu = subprocess.run([sys.executable, racine + "/outils/scripts/controle_clauses_parcours.py",
                         cible], capture_output=True, text=True).stdout
    ligne = [l for l in vu.splitlines() if l.strip().startswith(jid)]
    assert ligne, "%s absent de la sortie du contrôle des clauses" % jid
    lu = int(re.search(r"annoncé\s+(\d+)", ligne[0]).group(1))
    assert lu == annonce, ("config %s : le contrôle lit « annoncé %d », %d voulu — la "
                           "substitution n'a pas touché la forme qu'il lit"
                           % (cible.split("/")[-1], lu, annonce))
PYSJ
  # scénario | code attendu | motif exigé dans la sortie (vide = aucun)
  for cas in "refus_avant_bilan|1|il manque|$SJ_JOBT|--config $SJ_CFGI" \
             "parcours_complet|0|le parcours a atteint|$SJ_JOBT|--config $SJ_CFG" \
             "job_inconnu|3|job inconnu|job-qui-nexiste-pas|" \
             "usage_sans_argument|2|Usage|  |" \
             "confirmer_avec_config|2|agissent sur le dépôt réel|$SJ_JOBT|--confirmer --config $SJ_CFG"; do
    IFS='|' read -r SJ_NOM SJ_ATT SJ_MOT SJ_JOB SJ_OPT <<< "$cas"
    SJ_OUT="$CUR/supprimer_job_$SJ_NOM.txt"
    # ⚠️ 15/10/2026 — « ${=SJ_OPT} » ET PAS « ${SJ_OPT} » : ce harnais est en ZSH, qui ne
    #    découpe PAS une expansion non quotée, contrairement à bash. Écrit sans le « = »,
    #    « --config /chemin » partait comme UN SEUL argument et supprimer_job.sh rendait
    #    « option inconnue » — exit 2 au lieu de 0, sur deux des cinq scénarios. Le témoin
    #    a donc commencé par accuser le script d'un défaut qui était dans le témoin.
    SJ_ARGS=(${=SJ_OPT})
    if [ "$SJ_JOB" = "  " ]; then
      "$SJ" > "$SJ_OUT" 2>&1; SJ_RC=$?
    else
      "$SJ" "$SJ_JOB" "${SJ_ARGS[@]}" > "$SJ_OUT" 2>&1; SJ_RC=$?
    fi
    if [ "$SJ_RC" != "$SJ_ATT" ]; then
      echo "  ✗ $SJ_NOM : exit $SJ_RC, $SJ_ATT attendu"
      SJ_KO=1
    elif [ -n "$SJ_MOT" ] && ! grep -qF "$SJ_MOT" "$SJ_OUT"; then
      echo "  ✗ $SJ_NOM : exit $SJ_ATT mais la sortie ne porte pas « $SJ_MOT »"
      echo "    Un code de sortie seul ne dit pas POURQUOI le script a refusé."
      SJ_KO=1
    fi
  done
  # ⚠️ ET LA VÉRIFICATION QUI COMPTE AUTANT QUE LES CINQ : aucun de ces appels ne doit avoir
  #    touché quoi que ce soit. Un garde-fou qui refuse APRÈS avoir écrit ne garde rien.
  SJ_AP=$(cd "$ROOT" && git status --porcelain jobs_config.json outils/scripts/run_job.sh \
          outils/scripts/setup_launchd.sh .claude/skills/lancer-job/SKILL.md 2>/dev/null); SJ_APE=$?
  SJ_SALE=0
  [ "$SJ_AV" != "$SJ_AP" ] && SJ_SALE=1
  SJ_PLIST=$(ls "$HOME/Library/LaunchAgents"/com.claudetravail.*.plist 2>/dev/null | wc -l | tr -d ' ')
  SJ_JOBS=$(env -i $PY -c "import json;print(len(json.load(open('$ROOT/jobs_config.json'))['jobs']))")
  # 🔴 27/10/2026 — UN `git status` QUI ÉCHOUE NE VAUT PAS « RIEN N'A CHANGÉ ». Les deux photos
  #    sont prises avec 2>/dev/null : si git refuse de répondre, elles sont TOUTES DEUX VIDES,
  #    donc ÉGALES, et le témoin concluait « les appels de plan sont inertes ». Même classe que
  #    le `$SEMENCE` non vide du runner : un garde satisfait par un état cassé. Reproduit sur un
  #    dépôt en `core.bare=true` — l'état exact où l'incident GIT_DIR a laissé celui-ci — qui rend
  #    « fatal : cette opération doit être effectuée dans un arbre de travail », donc la chaîne
  #    vide. ⚠️ LATENT, PAS EXERCÉ : le bloc du runner tourne ligne 1851, APRÈS ces photos, donc
  #    le témoin a été honnête pendant l'incident — c'est le passage SUIVANT qui aurait menti.
  #    On lit donc le CODE DE SORTIE, pas seulement la différence des deux sorties.
  if [ "$SJ_AVE" != "0" ] || [ "$SJ_APE" != "0" ]; then
    echo "  ✗ git status n'a pas pu répondre (codes $SJ_AVE puis $SJ_APE) — on ne sait donc PAS si"
    echo "    les appels de plan ont touché quelque chose. Vérifie l'état du dépôt : core.bare,"
    echo "    et le fichier .git de l'arbre de travail."
    SJ_KO=1
  elif [ "$SJ_SALE" != "0" ]; then
    echo "  ✗ les appels de plan ont CHANGÉ l'état d'un fichier suivi — ils doivent être inertes"
    echo "    avant : ${SJ_AV:-(propre)}"
    echo "    après : ${SJ_AP:-(propre)}"
    SJ_KO=1
  elif [ "$SJ_PLIST" != "$SJ_JOBS" ]; then
    echo "  ✗ $SJ_PLIST .plist pour $SJ_JOBS job(s) — un agent a été touché par un appel de plan"
    SJ_KO=1
  fi
  rm -f "$SJ_CFG"
  if [ "$SJ_KO" = 0 ]; then
    echo "  ✓ 5/5 scénarios — le garde-fou refuse avant le bilan, accepte un parcours complet,"
    echo "        et les appels de plan n'ont rien touché ($SJ_JOBS jobs, $SJ_PLIST .plist)"
  else
    STATUT=1
  fi
fi

# ---- Le classeur de suivi contre jobs_config.json (15/10/2026) ----
# Le classeur `livrables/documents/*_Les N Jobs.xlsx` est le SEUL endroit où un humain lit la
# liste des jobs, et c'était le seul que RIEN ne vérifiait : controle_clauses_parcours.py
# compare le prompt aux .docx, audit_vault.py les fiches aux documents, et personne ne
# comparait le classeur à la config. Résultat mesuré le 15/10/2026 : l'ancien classeur
# portait CINQ jobs supprimés et s'intitulait « Tes 14 jobs » pour 9 réels — parce que
# maj_xlsx_jobs.py, qui y écrit après chaque job réussi, ne met à jour QU'UNE COLONNE et ne
# touche jamais au jeu de lignes. Il est structurellement incapable de suivre une suppression.
# Sans réseau, instantané. Pas en --docs : c'est la porte des documents.
if [ "$MODE" != "--docs" ] && [ -x "$ROOT/outils/scripts/refaire_classeur.py" ]; then
  CL_OUT="$CUR/refaire_classeur.txt"
  if env -i $PY "$ROOT/outils/scripts/refaire_classeur.py" --verifier > "$CL_OUT" 2>&1; then
    grep -E "^ +✓" "$CL_OUT" | sed 's/^ */  /'
  else
    echo "▶ Classeur de suivi — DISCORDANCE avec jobs_config.json"
    grep -E "^ +✗|^ +→" "$CL_OUT" | sed 's/^ */  /'
    STATUT=1
  fi
fi

# ---- Témoins du runner (27/09/2026) ----
# run_job.sh décide ce qui est retenté et ce qui est PUBLIÉ pour les 14 jobs, et rien ne le
# testait : le fail-fast du plafond était mort depuis 19 jours sans qu'aucun contrôle puisse
# le dire. Sept scénarios de décision, quelques secondes, sans réseau ni jeton.
# Pas en mode --docs : celui-là est la porte des pushs de job, il reste focalisé sur les
# documents. Le job controle-livrables passe en --complet, donc la couverture est hebdomadaire.
# En --complet (le mode du job controle-livrables, qui accepte déjà 4-5 min de réseau) on
# joue AUSSI les mutations : 30 s au lieu de 4, et c'est la seule passe automatique qui
# vérifie que ces témoins mordent encore. En mode normal, les dix témoins seuls.
if [ "$MODE" != "--docs" ] && [ -x "$ROOT/outils/scripts/non_regression_runner.sh" ]; then
  RUNNER_ARGS=()
  [ "$MODE" = "--complet" ] && RUNNER_ARGS=(--mutations)
  if ! "$ROOT/outils/scripts/non_regression_runner.sh" "${RUNNER_ARGS[@]}"; then
    echo "  ✗ les témoins du runner ont changé de comportement (voir ci-dessus)"
    STATUT=1
  fi
fi

# dernière ligne, toujours : ce qui lit la sortie en arrière-plan (job controle-livrables) attend celle-ci —
# l'en-tête « Témoins d'attributions » s'imprime AVANT le dernier contrôle, il ne prouve pas la fin
echo "▶ Terminé — exit $STATUT"
exit $STATUT
