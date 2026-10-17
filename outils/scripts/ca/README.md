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
