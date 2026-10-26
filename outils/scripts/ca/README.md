# Chaîne de certificat manquante — intermédiaire servi à la main

## Pourquoi ce dossier existe (17-18/10/2026)

Le 17/10/2026, `has-sante.fr` est devenu **injoignable au `curl`** depuis ce poste, sur toutes
ses URL et après plusieurs essais : `HTTP 000 · curl 60`. `WebFetch` échouait de même
(« unable to verify the first certificate »). Seul `WebSearch` passait, parce qu'il interroge
un index et n'ouvre pas de connexion TLS au serveur.

**Deux causes indépendantes, mesurées :**

1. **Le serveur de la HAS n'envoie pas sa chaîne intermédiaire.** `openssl s_client` ne reçoit
   que le certificat terminal — `0 s: CN=*.has-sante.fr` — et rend
   `Verify return code: 21 (unable to verify the first certificate)`. Le certificat a été
   réémis le **8 octobre 2026** ; la chaîne a été cassée à cette occasion. Les navigateurs
   compensent (intermédiaires en cache, récupération AIA) ; `curl`, `openssl` et `WebFetch` non.
2. **Le bundle que `curl` lit est périmé.** `/usr/bin/curl` est celui d'Apple, lié à
   LibreSSL/SecureTransport, et pointe sur `/etc/ssl/cert.pem` — **128 certificats, daté du
   16 août 2025**, et **sans la racine `Sectigo Public Server Authentication Root R46`**
   (vérifié en extrayant chaque certificat et en lisant son sujet, pas au `grep` : un bundle
   PEM n'a pas d'étiquettes lisibles, et un `grep 'Sectigo'` y rend 0 même quand la racine y est).
   `brew upgrade ca-certificates` ne corrige pas cela : il entretient
   `/usr/local/etc/ca-certificates/cert.pem` — **200 certificats, mai 2026, racine R46
   présente** — que le `curl` d'Apple ne lit pas.

**Il fallait les deux.** Avec la racine seule, `curl` échoue encore (la chaîne est coupée au
milieu). Avec l'intermédiaire seul, elle ne remonte à aucune racine approuvée.

## Ce que contient ce dossier

`sectigo-public-server-auth-ca-ov-r36.pem` — l'intermédiaire
`Sectigo Public Server Authentication CA OV R36`, récupéré à l'adresse que l'extension
**AIA du certificat de la HAS** désigne elle-même :
`http://crt.sectigo.com/SectigoPublicServerAuthenticationCAOVR36.crt`.
Émis par `Sectigo Public Server Authentication Root R46`, valide du 22/03/2021 au 21/03/2036.

⚠️ **Ce n'est PAS un contournement de la vérification TLS.** Rien n'est désactivé : on fournit
au client ce que le serveur omet, et la chaîne est validée **entièrement**, jusqu'à une racine
publique que la distribution Mozilla approuve. La différence avec un `-k` ou un
`verify=False` est totale : ceux-là acceptent n'importe quel certificat, celui-ci n'accepte
que la chaîne réelle.

## Ce que le dépôt n'a PAS fait, et pourquoi

**Le magasin de confiance du système n'a pas été modifié** : ajouter une racine de
certification à une machine est une décision de sécurité qui revient à son propriétaire, pas
à un script de ce dépôt. Les scripts construisent un bundle **en cache**, dans
`outils/scripts/logs/` (gitignoré), par concaténation du bundle de `brew` et de cet
intermédiaire, et le passent à `curl` par `--cacert`. Si le bundle de `brew` est absent, les
scripts ne passent aucun `--cacert` et retrouvent le comportement d'avant.

## Mesure avant adoption — 415 hôtes du corpus, les deux bundles

**Zéro régression · trois gains**, tous confirmés en rejeu sérialisé :
`www.has-sante.fr` et `has-sante.fr` passent de `curl 60` à **HTTP 200**, et
**`ssd.jpl.nasa.gov`** aussi — un hôte que le dépôt tenait pour injoignable depuis le
01/10/2026. Échecs TLS : **8 → 5**.
⚠️ Le balayage initial, à huit requêtes en parallèle, avait annoncé **une régression**
(`science.nasa.gov`) **et un faux gain** (`studybuddhism.com`) : rejoués seuls, les deux
rendent 200 dans les deux configurations. C'étaient des **délais d'attente dus à la
concurrence** — l'incident du 12/10/2026 reproduit dans la mesure même qui préparait ce
correctif. **Un verdict réseau ne vaut que rejoué seul.**

📊 **Portée** : **57 documents citent `has-sante.fr`**, 5 citent `ssd.jpl.nasa.gov` — **62 au
total** voient au moins une page redevenir lisible. Ce n'est pas un gain gratuit : une page
qui passait de « non lue, rien n'est conclu » à **lisible** peut révéler qu'une citation n'y
est pas. Le verdict de ces documents peut donc changer, et dans le sens bloquant.

---

## Deuxième maillon — `cnsa.fr`, 26/10/2026

**Le 18/10 n'était pas un cas isolé, et le module n'était pas prêt pour le second.**

`balayer_adresses.py`, relancé le 26/10, a vu **quatre adresses `cnsa.fr` passer de `HTTP 200` à
`000 · curl 60`** en vingt-quatre heures, et une cinquième de `403` à `60` — **5 adresses,
38 documents** de la série SERAFIN-PH. Mesuré, séquentiellement, trois essais, **avec et sans**
le faisceau : `exit 60` constant dans les deux cas, donc le défaut n'était pas le nôtre.

**Le mécanisme est celui de la HAS, à l'identique :**

```
0 s:… CN=www.cnsa.fr
  i:C=ES, O=Sectigo (Europe) SL, CN=Sectigo Qualified Website Authentication CA R39
  v:NotBefore: Oct 14 00:00:00 2026 GMT; NotAfter: Apr 30 23:59:59 2027 GMT
Verify return code: 21 (unable to verify the first certificate)
  nb de certificats présentés : 1
```

Certificat **réémis le 14 octobre 2026**, valide, **chaîne intermédiaire absente**. Le serveur
n'envoie que sa feuille, et `curl`/`openssl`/`WebFetch` ne compensent pas.

⚠️ **MAIS L'ÉMETTEUR N'EST PAS LE MÊME QU'EN OCTOBRE.** La HAS passe par
`Sectigo Public Server Authentication CA OV R36` ; la CNSA, qui est une entité publique
(`businessCategory=Government Entity`), par **`Sectigo Qualified Website Authentication CA R39`** —
un certificat qualifié eIDAS, émis par la filiale espagnole `Sectigo (Europe) SL`. Le maillon
du 18/10 **ne pouvait donc pas servir**, et c'est mesuré : la feuille de la CNSA contre le
faisceau d'alors rend `error 20 at 0 depth lookup: unable to get local issuer certificate`.

### Le second intermédiaire

`sectigo-qualified-website-auth-ca-r39.pem` — `Sectigo Qualified Website Authentication CA R39`,
récupéré à l'adresse que l'**extension AIA de la feuille de la CNSA désigne elle-même** :
`http://crt.sectigo.com/SectigoQualifiedWebsiteAuthenticationCAR39.crt`
(HTTP 200 · 1 612 octets · `application/pkix-cert` · sha256 du DER
`ac8c7ef96eb4b535fbfb4e7521f130536198a60dff716312b22d4acc4afe9a7d`).
Valide du 18/09/2024 au 17/09/2039, `CA:TRUE, pathlen:0`.

🟢 **Et il remonte à une racine DÉJÀ approuvée — rien de neuf n'entre dans la confiance.** Son
émetteur est `Sectigo Public Server Authentication Root R46`, la même racine que le maillon du
18/10, présente dans le bundle de `brew` (vérifié par **extraction de chaque certificat et
lecture de son sujet**, jamais au `grep` : l'avertissement de la section précédente vaut
toujours). Les trois vérifications, dans l'ordre :

| Vérification | Commande | Résultat |
|---|---|---|
| L'intermédiaire seul remonte-t-il aux racines de brew ? | `openssl verify -CAfile <brew> r39.pem` | **OK** |
| La chaîne complète est-elle valide ? | `openssl verify -CAfile <brew> -untrusted r39.pem <feuille>` | **OK** |
| Et contre l'ancien faisceau du dépôt ? | `openssl verify -CAfile <faisceau 201> <feuille>` | `error 20` |

### 🔴 Ce que l'incident a révélé du module lui-même

`ca_bundle.py` portait **un chemin de fichier en dur** :

```python
INTER = os.path.join(RACINE, "outils", "scripts", "ca",
                     "sectigo-public-server-auth-ca-ov-r36.pem")
```

**Déposer un second `.pem` dans `ca/` n'aurait donc eu aucun effet, et rien ne l'aurait dit** —
ni une erreur, ni un avertissement : le faisceau se serait reconstruit sans lui, `curl` aurait
continué à rendre `60`, et les pages de la CNSA seraient restées « NON LUES », c'est-à-dire
**indiscernables d'une citation absente**. C'est le même angle mort qu'une source écartée sur un
`000`. Le module charge désormais **tous** les `.pem` du dossier, par `intermediaires()`.

### Le garde au harnais — bloc `0 octies`, tous les modes

`ca_bundle.py --autotest`, **6 bornes, aucun réseau, aucun tiers** : ① `chemin()` rend un fichier
existant · ② `ca/` porte au moins un intermédiaire · ③ **le compte du faisceau = brew + TOUS les
`.pem` de `ca/`** · ④ **chaque `.pem` est présent dans le faisceau, et la borne le NOMME** ·
⑤ seuls les `.pem` sont pris, et triés · ⑥ dossier absent → aucun intermédiaire, donc le repli
d'avant le faisceau est préservé. ⑤ et ⑥ exercent le **vrai** `intermediaires()` en déplaçant
`CA_DIR` vers une arborescence fabriquée en `tempfile` — pas une copie de sa logique.

⚠️ **Ces bornes ne peuvent pas périmer sur la panne d'un site**, contrairement aux témoins qui
ont bloqué le dépôt les 15, 22 et 23/10 : elles ne regardent que le dossier `ca/` et le fichier
en cache. Et `ATTENDU_CA=6` garde le lot contre sa propre amputation — un lot réduit
imprimerait un « N/N » plus petit et passerait au vert.

🧪 **Sabotage, et il mord** : remettre `inters[:1]` dans la concaténation — c'est-à-dire
reproduire le défaut d'avant le 26/10 — fait échouer ③ (`201 mesuré, 202 attendu`) **et** ④
(`absents : sectigo-qualified-website-auth-ca-r39.pem`), **exit 1**. Les deux bornes ne sont pas
redondantes : ③ compte, ④ **nomme**. `ca_bundle.py` restauré au sha256 identique.

### 🔴 Ce que le correctif NE répare PAS, et il faut le dire

**Les pages de la CNSA ne sont toujours pas lisibles.** Le TLS est réparé — `exit 60 → exit 0`,
et **`https://www.cnsa.fr/` rend désormais `HTTP 200`** — mais les pages de contenu rendent
**`HTTP 500`** :

```
HTTP/2 500 · content-type: text/html · x-varnish-cache: MISS
corps : 67 octets — « The website encountered an unexpected error. Try again later. »
```

Indépendant de l'agent (notre UA, un UA Chrome complet, aucun UA : `500` les trois fois), et
c'est le message d'erreur générique de Drupal derrière Varnish. **Cette panne était invisible
derrière l'échec TLS**, qui survient avant toute réponse HTTP — elle n'est donc pas causée par
le correctif, elle est **révélée** par lui. Second point de vue : l'Internet Archive avait
`www.cnsa.fr/actualites` à **200 le 17/10/2026**, neuf jours avant ; la panne est postérieure,
et cohérente avec la réémission du certificat du 14/10.

📊 **Ce que le correctif change donc vraiment** : les 5 adresses passent de `TLS` à `PANNE` dans
la classification du balayage. Ce n'est pas cosmétique — c'est la différence entre *« notre pile
ne sait pas valider, donc on ne sait rien »* et *« le serveur de la CNSA est en panne »*. Le
premier verdict fait écarter une source valide en silence ; le second est un fait sur lequel on
peut agir, attendre, ou déclarer une semaine creuse en le disant.
