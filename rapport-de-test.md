# Rapport de test — GUDLFT

> Version 1.1 — 2026-10-26
> Auteur : Isaac Batoua (`batisaac`)
> Dépôt : <https://github.com/batisaac/PROJET1-TESTS-ET-VALIDATIONS>
> Branche courante : `bug/email-inconnu` (créée depuis `main` @ `4ea6d0c`)

**État d'avancement : phase 1 en cours — 1 groupe d'anomalies corrigé sur 10.**
Les sections marquées *(à compléter)* le seront au fur et à mesure ; ce document ne
contient aucun résultat non mesuré.

---

## 1. Objectif

Documenter la démarche de test du projet **GUDLFT**, application Flask permettant aux
secrétaires de clubs d'inscrire des athlètes à des compétitions avec des points.

Le rapport couvre : la reproduction des anomalies, leur inventaire et criticité, la
stratégie de test, les tests réellement écrits et leurs résultats, les corrections
apportées, la couverture de code, la conformité Flake8 et la phase 2.

---

## 2. Périmètre

### 2.1 Dans le périmètre

| Fonctionnalité | Exigence (spécifications fonctionnelles) |
|---|---|
| Connexion par email | « Les secrétaires des clubs pourront utiliser leur adresse électronique pour se connecter » |
| Liste des compétitions à venir | « consulter la liste des compétitions à venir » |
| Achat de places | « utiliser leurs points pour acheter des places » (1 point = 1 place) |
| Déduction des points | « Les points utilisés doivent être déduits du total précédent » |
| Message de confirmation | « voir un message confirmant le nombre de places achetées » |
| Refus si concours complet | « ou un message indiquant que le concours est complet » |
| Limite des places disponibles | « ne doivent pas pouvoir réserver plus de places que celles disponibles » |
| Limite de 12 places | « ou plus de 12 places dans une compétition » |
| Déconnexion | « Les secrétaires des clubs pourront se déconnecter » |
| Tableau public des points (phase 2) | « tableau public, en lecture seule, des totaux de points… Il ne devrait pas être nécessaire de se connecter » |
| Performance (phase 2) | « pas plus de 5 secondes pour récupérer une liste de compétitions, et pas plus de 2 secondes pour mettre à jour le total de points » |

### 2.2 Hors périmètre

- Création de comptes, mots de passe, récupération d'identifiants.
- Administration des compétitions et attribution des points.
- Internationalisation, accessibilité avancée.

### 2.3 Composants testés

| Élément | Rôle |
|---|---|
| `server.py` | Routes : `/`, `/showSummary`, `/book/<competition>/<club>`, `/purchasePlaces`, `/logout` |
| `templates/index.html` | Formulaire de connexion |
| `templates/welcome.html` | Tableau de bord du club |
| `templates/booking.html` | Formulaire d'achat |
| `clubs.json` | Clubs (`name`, `email`, `points`) |
| `competitions.json` | Compétitions (`name`, `date`, `numberOfPlaces`) |

Le projet utilise des fichiers JSON à la place d'un SGBD (choix imposé pour ce POC).

---

## 3. Environnement de test

| Élément | Valeur |
|---|---|
| Système | Microsoft Windows 11 Famille Unilingue — 10.0.26100 — 64 bits |
| Interpréteur | Python 3.14.2 |
| Environnement virtuel | `.venv` (non versionné) |
| Flask | 3.1.3 |
| Werkzeug | 3.1.9 |
| Jinja2 / MarkupSafe | 3.1.6 / 3.0.4 |
| pytest | 9.1.1 |
| pytest-cov / coverage | 7.1.0 / 7.16.2 |
| flake8 | 7.4.1 |
| Locust | 2.47.0 (installé, non encore utilisé) |

Installation et lancement :

```cmd
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m flask --app server run
```

> L'application doit être lancée **depuis la racine du projet** (chemins relatifs, voir **B18**).

---

## 4. Stratégie de test

### 4.1 Démarche TDD

Cycle **Rouge → Vert → Refactor** : écrire le test (il échoue), corriger le code pour le
faire passer, nettoyer sans casser les tests.

### 4.2 Niveaux de test

```text
test/
├── unit/           # règles métier isolées
├── integration/    # routes Flask + JSON + templates
└── fonctionnel/    # parcours utilisateur complet
```

| Niveau | Périmètre | Outil |
|---|---|---|
| Unitaire | Règles métier pures (limite de 12, solde, places disponibles, lecture JSON) | pytest |
| Intégration | Code HTTP, message affiché, redirection, contenu rendu | `app.test_client()` |
| Fonctionnel | Parcours complet : connexion → réservation → vérification → déconnexion | `app.test_client()` + fixtures |

Objectifs du guide : **couverture ≥ 60 %**, environ **2× plus de tests unitaires** que
d'intégration/fonctionnels.

### 4.3 Happy / sad paths

Chaque fonctionnalité est testée sur son cas nominal **et** sur ses cas d'erreur
(email inconnu, champ manquant, valeur non numérique, quantité négative, solde insuffisant,
quota dépassé, concours complet, identifiant inconnu).

### 4.4 Isolation des tests

L'état est porté par `clubs.json` / `competitions.json`, chargés en mémoire au démarrage
(**B22**). La fixture `donnees_reinitialisees` (`test/conftest.py`, `autouse=True`) recharge
les deux fichiers avant chaque test : sans elle, un achat d'un test modifierait les suivants.

```python
@pytest.fixture(autouse=True)
def donnees_reinitialisees():
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
    yield
```

### 4.5 Branches Git

`<type>/<nom-descriptif>`, une branche par anomalie. `main` reste la source de vérité ;
la branche `QA` sera créée depuis `main` en fin de projet et **ne sera jamais fusionnée dans `main`**.

---

## 5. Traçabilité exigences → tests

| Exigence | Test | Statut |
|---|---|---|
| Connexion email valide | T-I01 | **écrit, VERT** |
| Connexion email inconnu | T-I02 | **écrit, VERT** |
| Champ email absent | T-I03 | **écrit, VERT** |
| Email vide | T-I04 | **écrit, VERT** |
| Accès page de réservation valide | T-I05 | à écrire |
| Club inconnu dans l'URL | T-I06 | à écrire |
| Compétition inconnue dans l'URL | T-I07 | à écrire |
| Achat valide + confirmation | T-I08 | à écrire |
| Compétition inconnue (formulaire) | T-I09 | à écrire |
| Club inconnu (formulaire) | T-I10 | à écrire |
| Champ `places` absent | T-I11 | à écrire |
| `places` non numérique | T-I12 | à écrire |
| `places` ≤ 0 | T-I13 | à écrire |
| Plus de 12 places | T-I14 | à écrire |
| Plus de places disponibles | T-I15 | à écrire |
| Solde de points insuffisant | T-I16 | à écrire |
| Déduction des points | T-I17 | à écrire |
| Concours complet | T-I18 | à écrire |
| Message avec le nombre de places | T-I19 | à écrire |
| Persistance JSON | T-I20 | à écrire |
| Déconnexion effective | T-I21 | à écrire |
| Tableau public sans connexion (phase 2) | T-I22 | à écrire |
| Contenu du tableau public (phase 2) | T-I23 | à écrire |

---

## 6. Reproduction des anomalies — état initial

### 6.1 Méthode

1. **Manuellement** dans le navigateur, sur l'application lancée en local.
2. **Automatiquement** avec `reproduction_bugs.py`, qui utilise le client de test Flask.

```cmd
python -m flask --app server run
python reproduction_bugs.py
```

### 6.2 Sortie de `reproduction_bugs.py` (avant toute correction)

```text
======================================================================
REPRODUCTION DES BUGS - ETAT INITIAL
======================================================================

[1] CONNEXION
ERROR in app: Exception on /showSummary [POST]
  File "...\server.py", line 29, in showSummary
    club = [club for club in clubs if club['email'] == request.form['email']][0]
IndexError: list index out of range
BUG | B1 - Email inconnu                                         | recu=500 | attendu=200
BUG | B2 - Champ email absent                                    | recu=400 | attendu=200
ERROR in app: Exception on /showSummary [POST]
IndexError: list index out of range
BUG | B2b - Email vide                                           | recu=500 | attendu=200

[2] RESERVATION VIA URL
ERROR in app: Exception on /book/Spring Festival/Fake [GET]
  File "...\server.py", line 35, in book
IndexError: list index out of range
BUG | B3 - Club inconnu dans l'URL                               | recu=500 | attendu=200
ERROR in app: Exception on /book/Fake/Simply Lift [GET]
  File "...\server.py", line 36, in book
IndexError: list index out of range
BUG | B4 - Competition inconnue dans l'URL                       | recu=500 | attendu=200
ERROR in app: Exception on /book/Fake/Fake [GET]
  File "...\server.py", line 35, in book
IndexError: list index out of range
BUG | B5 - Les deux inconnus                                     | recu=500 | attendu=200

[3] ACHAT DE PLACES - FORMULAIRE
ERROR in app: Exception on /purchasePlaces [POST]
  File "...\server.py", line 46, in purchasePlaces
IndexError: list index out of range
BUG | B6 - Competition inconnue dans le formulaire               | recu=500 | attendu=200
ERROR in app: Exception on /purchasePlaces [POST]
  File "...\server.py", line 47, in purchasePlaces
IndexError: list index out of range
BUG | B7 - Club inconnu dans le formulaire                       | recu=500 | attendu=200
BUG | B8 - Champ 'places' manquant                               | recu=400 | attendu=200
ERROR in app: Exception on /purchasePlaces [POST]
  File "...\server.py", line 48, in purchasePlaces
ValueError: invalid literal for int() with base 10: 'abc'
BUG | B9 - 'places' non entier 'abc'                             | recu=500 | attendu=200

[4] REGLES METIER
BUG | B13 - 999 places alors que Fall Classic n'en a que 13 | status=200
BUG | B12 - 20 places (> 12 autorises)                    | status=200
BUG | B16 - Places negatives                             | status=200
BUG | B11 - 5 places pour Iron Temple (4 points)         | status=200

======================================================================
FIN
======================================================================
```

Les numéros de ligne cités (`server.py:29/35/36/46/47/48`) sont ceux du code d'origine.

### 6.3 Observations manuelles (navigateur, avant correction)

| # | Action | Observation | Anomalie |
|---|---|---|---|
| 1 | `GET /` | Page affichée | OK |
| 2 | Connexion `john@simplylift.co` | Tableau de bord, 13 points, 2 compétitions | OK |
| 3 | Connexion `inconnu@club.com` | `500 Internal Server Error` | B1 |
| 4 | `GET /book/Spring Festival/Simply Lift` | Formulaire affiché | OK |
| 5 | `GET /book/Spring Festival/Fake` | `500 Internal Server Error` | B3 |
| 6 | Achat d'1 place (Spring Festival) | `Great-booking complete!`, places 25 → 24, **points toujours 13** | B10, B15 |
| 7 | Achats répétés (Fall Classic) | Places 13 → −986 → −1006… **compteur négatif** | B13 |
| 8 | Achat de 20 places | Accepté, points toujours 13 | B11, B12, B14 |
| 9 | Achat avec `places = -5` | Accepté | B16 |
| 10 | Achat avec `places = abc` | Bloqué par le navigateur (`number`), **mais le serveur n'a aucune validation** | B9 |
| 11 | Redémarrage après achats | Données revenues à l'état initial : aucune persistance | B17 |

---

## 7. Inventaire des anomalies

> **Réserve importante** — La section « Issues » du dépôt d'origine est **vide**
> (0 issue sur `Sedrickgael/Python_Testing_2627` et sur `teamWorkbyG/Python_Testing_2627`),
> alors que le mail du commanditaire annonçait des bogues listés dans les issues.
> L'inventaire a donc été **établi par audit du code + confrontation aux spécifications**,
> puis confirmé par reproduction. Il peut différer d'une liste officielle non publiée (voir §14).

### 7.1 Gravité

| Niveau | Définition |
|---|---|
| **Bloquant** | HTTP 400/500, fonctionnalité inutilisable |
| **Majeur** | Règle métier non respectée (résultat faux) |
| **Mineur** | Robustesse, sécurité, qualité, cosmétique |

### 7.2 Entrées invalides et crashs (bloquant)

| ID | Emplacement | Symptôme | Cause racine | Repro | État |
|---|---|---|---|---|---|
| **B1** | `server.py:29` | Email inconnu → 500 | `[...][0]` sur liste vide | auto | **corrigé** |
| **B2** | `server.py:29` | Champ `email` absent → 400 | `request.form['email']` | auto | **corrigé** |
| **B2b** | `server.py:29` | Email vide → 500 | idem B1 | auto | **corrigé** |
| **B3** | `server.py:35` | Club inconnu dans l'URL → 500 | `[...][0]` | auto | à corriger |
| **B4** | `server.py:36` | Compétition inconnue dans l'URL → 500 | `[...][0]` | auto | à corriger |
| **B5** | `server.py:35` | Club et compétition inconnus → 500 | B3 se déclenche avant B4 | auto | à corriger |
| **B5bis** | `server.py:41` | Branche `else` de `book()` inatteignable : passe une **chaîne** au template (`club['email']` → `TypeError`) | conception erronée | audit | à corriger |
| **B6** | `server.py:46` | Compétition inconnue (formulaire) → 500 | `[...][0]` | auto | à corriger |
| **B7** | `server.py:47` | Club inconnu (formulaire) → 500 | `[...][0]` | auto | à corriger |
| **B8** | `server.py:47` | Champ manquant → 400 | `request.form[...]` | auto | à corriger |
| **B9** | `server.py:48` | `places = abc` → 500 | `int('abc')` → `ValueError` | auto | à corriger |

### 7.3 Règles métier (majeur)

| ID | Emplacement | Exigence violée | Comportement observé | Repro | État |
|---|---|---|---|---|---|
| **B10** | `server.py:49` | Points déduits du total | Points jamais débités | manuel | à corriger |
| **B11** | `server.py:45-51` | Refus si points insuffisants | Aucun contrôle (Iron Temple : 4 points, 5 places) | auto | à corriger |
| **B12** | `server.py:45-51` | 12 places maximum | Aucun contrôle (20 places acceptées) | auto | à corriger |
| **B13** | `server.py:49` | Pas plus que les places disponibles | Compteur négatif (13 → −986) | auto + manuel | à corriger |
| **B14** | `server.py:50` | Message « concours complet » | Toujours `Great-booking complete!` | manuel | à corriger |
| **B15** | `server.py:50` | Message avec le nombre de places | Message générique | manuel | à corriger |
| **B16** | `server.py:48-49` | Quantité entière ≥ 1 | `-5` accepté (le stock augmente), `0` accepté | auto | à corriger |

### 7.4 Robustesse, sécurité, testabilité

| ID | Emplacement | Problème | Gravité | Repro | État |
|---|---|---|---|---|---|
| **B17** | `server.py:20-21,49` | Aucune persistance : les JSON ne sont jamais réécrits, tout est perdu au redémarrage | Majeur | manuel | à corriger |
| **B18** | `server.py:6,13` | Chemins relatifs au répertoire courant | Mineur | audit | à corriger |
| **B19** | `server.py:18` | `secret_key` en dur et versionnée | Mineur (sécurité) | audit | à corriger |
| **B20** | `server.py:33-51` | Aucune authentification : réservation possible pour n'importe quel club | Majeur (sécurité) | audit | à corriger |
| **B21** | `server.py:57-59` | `/logout` sans effet (aucune session) | Mineur | audit | à corriger |
| **B22** | `server.py:20-21` | Données chargées une fois au démarrage (état global non réinitialisable) | Mineur (testabilité) | audit | atténué par la fixture `donnees_reinitialisees` |

### 7.5 Interface et fonctionnalités manquantes

| ID | Emplacement | Problème | Gravité | État |
|---|---|---|---|---|
| **B23** | `templates/welcome.html` | Compétitions **passées** affichées (exigence : à venir) | Majeur | à corriger |
| **B24** | `templates/*.html` | HTML invalide : `id=""`, `label for` non associé, `</br>`, `input number` sans `min`/`max` | Mineur | à corriger |
| **F1** | `server.py:54` | Phase 2 : tableau public des points (`# TODO`) | Fonctionnalité | à faire |
| **F2** | — | Phase 2 : performance (< 5 s / < 2 s) | Exigence | à faire |

### 7.6 Bilan

| Catégorie | Nombre | Corrigées |
|---|---|---|
| Crashs / entrées invalides | 11 | 3 (B1, B2, B2b) |
| Règles métier | 7 | 0 |
| Robustesse / sécurité / testabilité | 6 | 0 |
| Interface / fonctionnalités | 2 | 0 |
| **Total** | **26** | **3** |

Reproduction : 14 anomalies via script + 4 via navigateur = **18 constatées** ; 8 identifiées par audit.

---

## 8. Tests réalisés

Un seul fichier de test contient des tests à ce stade : `test/integration/test_login.py`.
Les autres fichiers de l'arborescence sont créés mais **vides** (backlog §9).

### 8.1 Exécution

```cmd
python -m pytest test/integration/test_login.py -v
```

**Avant correction :**

```text
test/integration/test_login.py::test_connexion_email_valide PASSED              [ 25%]
test/integration/test_login.py::test_connexion_email_inconnu_ne_provoque_pas_d_erreur_serveur FAILED [ 50%]
test/integration/test_login.py::test_connexion_champ_email_absent_ne_provoque_pas_d_erreur_serveur FAILED [ 75%]
test/integration/test_login.py::test_connexion_email_vide_ne_provoque_pas_d_erreur_serveur FAILED [100%]

E   IndexError: list index out of range
server.py:29: IndexError
========================= 3 failed, 1 passed in 2.03s =========================
```

**Après correction :**

```text
test/integration/test_login.py::test_connexion_email_valide PASSED              [ 25%]
test/integration/test_login.py::test_connexion_email_inconnu_ne_provoque_pas_d_erreur_serveur PASSED [ 50%]
test/integration/test_login.py::test_connexion_champ_email_absent_ne_provoque_pas_d_erreur_serveur PASSED [ 75%]
test/integration/test_login.py::test_connexion_email_vide_ne_provoque_pas_d_erreur_serveur PASSED [100%]
============================== 4 passed in 0.36s ==============================
```

### 8.2 Détail des tests

| ID | Nom du test | Type | Vérifie | Résultat |
|---|---|---|---|---|
| T-I01 | `test_connexion_email_valide` | Intégration (happy) | HTTP 200 + `Welcome, john@simplylift.co` | VERT |
| T-I02 | `test_connexion_email_inconnu_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | HTTP 200 + message `not registered` | VERT |
| T-I03 | `test_connexion_champ_email_absent_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | HTTP 200 + message `not registered` | VERT |
| T-I04 | `test_connexion_email_vide_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | HTTP 200 + message `not registered` | VERT |

Suite complète : `python -m pytest -q` → **4 passed in 0.44s**.

---

## 9. Backlog de tests (non écrits)

| Fichier | Tests prévus |
|---|---|
| `test/unit/test_club.py` | conversion des points, débit, solde suffisant, limite de 12 |
| `test/unit/test_competition.py` | places disponibles, concours complet, places suffisantes, date passée/future |
| `test/unit/test_repository.py` | lecture/écriture JSON, fichier absent, JSON corrompu |
| `test/integration/test_booking_url.py` | T-I05 à T-I07 |
| `test/integration/test_purchase.py` | T-I08 à T-I21 |
| `test/integration/test_points_public.py` | T-I22, T-I23 (phase 2) |
| `test/fonctionnel/test_parcours_complet.py` | parcours complet, limite de 12, stock épuisé, consultation publique |
| `locustfile.py` | charge 6 utilisateurs, seuils 5 s / 2 s |

> Les tests unitaires supposent l'extraction de la logique métier dans des modules dédiés
> (voir §11, branche `refactor/logique-metier`). Ils sont donc volontairement différés.

---

## 10. Corrections apportées

### 10.1 Branche `bug/email-inconnu` — B1, B2, B2b

**Diff conceptuel :**

```python
# AVANT
club = [club for club in clubs if club['email'] == request.form['email']][0]
return render_template('welcome.html', club=club, competitions=competitions)

# APRES
email = request.form.get('email', '').strip()
club = next((c for c in clubs if c['email'] == email), None)
if club is None:
    flash('Sorry, that email is not registered.')
    return render_template('index.html'), 200
return render_template('welcome.html', club=club, competitions=competitions)
```

`templates/index.html` affiche désormais les messages flash (`get_flashed_messages()`),
sans quoi le message d'erreur ne serait pas visible.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B1 | `IndexError` sur liste vide | T-I02 |
| B2 | `BadRequestKeyError` sur champ absent | T-I03 |
| B2b | `IndexError` sur email vide/espaces | T-I04 |

Choix : retour **HTTP 200** avec le formulaire et un message, plutôt qu'un 404 — l'utilisateur
reste sur la page de connexion et peut corriger sa saisie.

### 10.2 Autres branches

*(à compléter : aucune autre correction n'a encore été réalisée)*

| Anomalies | Branche prévue | État |
|---|---|---|
| B3, B4, B5, B5bis | `bug/book-url-invalide` | à faire |
| B6, B7, B8, B9 | `bug/purchase-form-invalide` | à faire |
| B16 | `bug/places-invalides` | à faire |
| B13 | `bug/sur-reservation` | à faire |
| B12 | `bug/limite-12-places` | à faire |
| B10, B11, B14, B15 | `bug/points-et-messages` | à faire |
| B17 | `bug/persistance-json` | à faire |
| B18 à B22 | `bug/robustesse-securite` | à faire |
| B23, B24 | `bug/interface` | à faire |
| — | `chore/qualite-flake8` | à faire |
| F1, F2 | `feature/tableau-points-public` | à faire |

---

## 11. Couverture de code

**Commande :**

```cmd
python -m pytest --cov=server --cov-report=term-missing -q
```

**Résultat mesuré (2026-10-26) :**

```text
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
server.py      44     14    68%   25, 39-45, 50-55, 63
-----------------------------------------
TOTAL          44     14    68%
4 passed in 0.92s
```

| Fichier | % | Lignes non couvertes |
|---|---|---|
| `server.py` | 68 % | 25 (`/`), 39-45 (`/book`), 50-55 (`/purchasePlaces`), 63 (`/logout`) |

**Analyse honnête** : les 68 % dépassent déjà l'objectif de 60 %, mais cette mesure est
**structurelle** : les décorateurs de routes sont exécutés à l'import du module, donc
comptés comme couverts. Elle ne prouve **pas** que les règles métier sont testées — les
routes d'achat (`50-55`) et de réservation (`39-45`) ne sont pas encore exercées.
La couverture utile sera réévaluée après les branches `bug/purchase-*` et `refactor/*`.

---

## 12. Flake8

**Commande :**

```cmd
python -m flake8 server.py test/ --statistics
```

**Résultat mesuré : 27 erreurs** (aucune configuration `setup.cfg` pour l'instant, donc
limite par défaut de 79 caractères).

```text
4     E111 indentation is not a multiple of 4
2     E117 over-indented
12    E231 missing whitespace after ','
2     E302 expected 2 blank lines, found 1
6     E501 line too long (> 79 characters)
1     W292 no newline at end of file
```

| Fichier | Erreurs |
|---|---|
| `server.py` | 26 |
| `test/integration/test_login.py` | 1 (E501 ligne 5 : appel `client.post` à 80 caractères) |

**État : non conforme.** Objectif : `flake8 .` sans erreur, via la branche
`chore/qualite-flake8` (formatage + `setup.cfg` avec `max-line-length = 99`).
La section 6 « Flake8 Report » du `README.md` sera remplie à ce moment-là.

---

## 13. Phase 2 — tableau public des points

**Non commencée.**

| Élément | Attendu | État |
|---|---|---|
| Route `GET /points` | accessible sans connexion | à faire |
| Template `templates/points.html` | tableau club / points, lecture seule | à faire |
| Lien depuis `index.html` | navigation publique | à faire |
| T-I22, T-I23 | 200 sans session + contenu exact | à écrire |
| Performance < 2 s | mesure Locust | à faire |

---

## 14. Écarts et limites

| # | Écart / limite | Impact |
|---|---|---|
| 1 | Section « Issues » du dépôt d'origine **vide** (0 issue) malgré l'annonce du commanditaire | Inventaire reconstruit par audit + reproduction ; exhaustivité non garantie |
| 2 | `requirements.txt` d'origine inutilisable (Flask 1.1.2 / MarkupSafe 1.1.1 / click 7.1.2 incompatibles Python 3.14) | Montée de version vers Flask 3.1.3 ; régressions couvertes par les tests au fur et à mesure |
| 3 | Compétitions de démonstration datées de 2020 (donc passées) alors que l'exigence porte sur les compétitions à venir | Tests à écrire avec des dates injectées par fixture |
| 4 | Couverture actuelle (68 %) **structurelle**, non représentative des règles métier | À réévaluer après les tests d'achat et le refactor |
| 5 | `coverage` mesure l'exécution, pas la qualité des assertions | Chaque fonctionnalité testée en happy + sad path |
| 6 | Locust mesurerait le serveur de développement Flask, pas un serveur de production | Résultats indicatifs ; seuils (5 s / 2 s) très larges |
| 7 | Le client de test Flask ne teste pas le JavaScript (ex. blocage de `abc` par `<input type="number">`) | D'où l'importance de la validation serveur (T-I12) |
| 8 | Les tests unitaires sont différés tant que la logique reste dans `server.py` | Prévu : branche `refactor/logique-metier` |

---

## 15. Conclusion

**État actuel** : 4 tests écrits, 4 verts. Les anomalies **B1, B2 et B2b** sont corrigées
et couvertes par des tests qui échouaient avant la correction (preuve TDD conservée §8.1).

**Reste à faire** en phase 1 : 21 anomalies (dont 8 crashs HTTP), puis Flake8.
**Phase 2** : non commencée.

Points d'attention confirmés par les mesures :
- l'objectif de couverture (60 %) est atteint « sur le papier » (68 %) mais **pas encore
  de façon significative** : les routes d'achat ne sont pas testées ;
- le code n'est **pas conforme Flake8** (27 erreurs) ;
- l'absence de persistance (**B17**) reste l'anomalie la plus structurante : sans elle,
  aucun test d'achat ne peut vérifier durablement l'état.

---

## Annexe A — Commandes

```cmd
.\.venv\Scripts\activate
python -m pip install -r requirements.txt

python -m flask --app server run
python reproduction_bugs.py

python -m pytest -v
python -m pytest test/unit -v
python -m pytest test/integration -v
python -m pytest test/fonctionnel -v

python -m pytest --cov=server --cov-report=term-missing --cov-report=html
python -m flake8 server.py test/ --statistics
```

## Annexe B — Arborescence

```text
test/
├── __init__.py
├── conftest.py
├── unit/
│   ├── __init__.py
│   ├── test_club.py            (vide)
│   ├── test_competition.py     (vide)
│   └── test_repository.py      (vide)
├── integration/
│   ├── __init__.py
│   ├── test_login.py           (4 tests — VERT)
│   ├── test_booking_url.py     (vide)
│   ├── test_purchase.py        (vide)
│   └── test_points_public.py   (vide)
└── fonctionnel/
    ├── __init__.py
    └── test_parcours_complet.py (vide)
```

## Annexe C — Glossaire

| Terme | Définition |
|---|---|
| Happy path | Scénario nominal |
| Sad path | Scénario d'erreur |
| Fixture | Préparation automatique exécutée par pytest avant un test |
| TDD | Écrire le test avant le code (rouge → vert → refactor) |
| Couverture | % de lignes exécutées par les tests |
| Régression | Bug réintroduit par une modification |
