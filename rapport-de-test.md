# Rapport de test — GUDLFT

> Version 1.10 — 2026-10-26
> Auteur : Isaac Batoua (`batisaac`)
> Dépôt : <https://github.com/batisaac/PROJET1-TESTS-ET-VALIDATIONS>
> Branche courante : `main` @ `1900cb6`

**État d'avancement : phases 1 et 2 terminées — 25 anomalies corrigées sur 26 (1 atténuée),
F1 et F2 livrées, 70 tests verts.**
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
| `templates/points.html` | Tableau public des points |
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
    server.clubs = load_clubs()
    server.competitions = load_competitions()
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
| Accès page de réservation valide | T-I05 | **écrit, VERT** |
| Club inconnu dans l'URL | T-I06 | **écrit, VERT** |
| Compétition inconnue dans l'URL | T-I07 | **écrit, VERT** |
| Club et compétition inconnus | T-I07b | **écrit, VERT** |
| Achat valide + confirmation | T-I08 | **écrit, VERT** |
| Compétition inconnue (formulaire) | T-I09 | **écrit, VERT** |
| Club inconnu (formulaire) | T-I10 | **écrit, VERT** |
| Champ `places` absent | T-I11 | **écrit, VERT** |
| `places` non numérique | T-I12 | **écrit, VERT** |
| `places` ≤ 0 | T-I13 | **écrit, VERT** |
| Plus de places disponibles | T-I14, T-I15 | **écrit, VERT** |
| Plus de 12 places | T-I16, T-I17 | **écrit, VERT** |
| Solde de points insuffisant | T-I18 | **écrit, VERT** |
| Déduction des points | T-I19 | **écrit, VERT** |
| Concours complet | T-I20 | **écrit, VERT** |
| Message avec le nombre de places | T-I21 | **écrit, VERT** |
| Persistance JSON | T-I22 | **écrit, VERT** |
| Réservation sans session | T-I23 | **écrit, VERT** |
| Achat sans session | T-I24 | **écrit, VERT** |
| Réservation pour un autre club | T-I25 | **écrit, VERT** |
| Achat pour un autre club | T-I26 | **écrit, VERT** |
| Déconnexion effective | T-I27 | **écrit, VERT** |
| Clé secrète non versionnée | T-I28, T-U27, T-U28 | **écrit, VERT** |
| Compétitions passées masquées | T-I29, T-U29, T-U30 | **écrit, VERT** |
| HTML valide (réservation, accueil) | T-I30, T-I31 | **écrit, VERT** |
| Tableau public sans connexion (phase 2) | T-I32 | **écrit, VERT** |
| Contenu du tableau public (phase 2) | T-I33 | **écrit, VERT** |
| Parcours complet (phase 2) | T-F01 à T-F03 | **écrit, VERT** |
| Performance (phase 2) | Locust, `rapport-de-performances.md` | **mesuré** |

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
| **B3** | `server.py:35` | Club inconnu dans l'URL → 500 | `[...][0]` | auto | **corrigé** |
| **B4** | `server.py:36` | Compétition inconnue dans l'URL → 500 | `[...][0]` | auto | **corrigé** |
| **B5** | `server.py:35` | Club et compétition inconnus → 500 | B3 se déclenche avant B4 | auto | **corrigé** |
| **B5bis** | `server.py:41` | Branche `else` de `book()` inatteignable : passe une **chaîne** au template (`club['email']` → `TypeError`) | conception erronée | audit | **corrigé** |
| **B6** | `server.py:46` | Compétition inconnue (formulaire) → 500 | `[...][0]` | auto | **corrigé** |
| **B7** | `server.py:47` | Club inconnu (formulaire) → 500 | `[...][0]` | auto | **corrigé** |
| **B8** | `server.py:47` | Champ manquant → 400 | `request.form[...]` | auto | **corrigé** |
| **B9** | `server.py:48` | `places = abc` → 500 | `int('abc')` → `ValueError` | auto | **corrigé** |

### 7.3 Règles métier (majeur)

| ID | Emplacement | Exigence violée | Comportement observé | Repro | État |
|---|---|---|---|---|---|
| **B10** | `server.py:49` | Points déduits du total | Points jamais débités | manuel | **corrigé** |
| **B11** | `server.py:45-51` | Refus si points insuffisants | Aucun contrôle (Iron Temple : 4 points, 5 places) | auto | **corrigé** |
| **B12** | `server.py:45-51` | 12 places maximum | Aucun contrôle (20 places acceptées) | auto | **corrigé** |
| **B13** | `server.py:49` | Pas plus que les places disponibles | Compteur négatif (13 → −986) | auto + manuel | **corrigé** |
| **B14** | `server.py:50` | Message « concours complet » | Toujours `Great-booking complete!` | manuel | **corrigé** |
| **B15** | `server.py:50` | Message avec le nombre de places | Message générique | manuel | **corrigé** |
| **B16** | `server.py:48-49` | Quantité entière ≥ 1 | `-5` accepté (le stock augmente), `0` accepté | auto | **corrigé** |

### 7.4 Robustesse, sécurité, testabilité

| ID | Emplacement | Problème | Gravité | Repro | État |
|---|---|---|---|---|---|
| **B17** | `server.py:20-21,49` | Aucune persistance : les JSON ne sont jamais réécrits, tout est perdu au redémarrage | Majeur | manuel | **corrigé** |
| **B18** | `repository.py` (ex-`server.py:6,13`) | Chemins relatifs au répertoire courant | Mineur | audit | **corrigé** |
| **B19** | `server.py:18` | `secret_key` en dur et versionnée | Mineur (sécurité) | audit | **corrigé** |
| **B20** | `server.py:33-51` | Aucune authentification : réservation possible pour n'importe quel club | Majeur (sécurité) | audit | **corrigé** |
| **B21** | `server.py:57-59` | `/logout` sans effet (aucune session) | Mineur | audit | **corrigé** |
| **B22** | `server.py:20-21` | Données chargées une fois au démarrage (état global non réinitialisable) | Mineur (testabilité) | audit | atténué par la fixture `donnees_reinitialisees` |

### 7.5 Interface et fonctionnalités manquantes

| ID | Emplacement | Problème | Gravité | État |
|---|---|---|---|---|
| **B23** | `templates/welcome.html` | Compétitions **passées** affichées (exigence : à venir) | Majeur | **corrigé** |
| **B24** | `templates/*.html` | HTML invalide : `id=""`, `label for` non associé, `</br>`, `input number` sans `min`/`max` | Mineur | **corrigé** |
| **F1** | `server.py` | Phase 2 : tableau public des points | Fonctionnalité | **fait** |
| **F2** | — | Phase 2 : performance (< 5 s / < 2 s) | Exigence | **fait** |

### 7.6 Bilan

| Catégorie | Nombre | Corrigées |
|---|---|---|
| Crashs / entrées invalides | 11 | 11 (B1 à B9, B5bis) |
| Règles métier | 7 | 7 (B10 à B16) |
| Robustesse / sécurité / testabilité | 6 | 5 (B17 à B21) |
| Interface / fonctionnalités | 2 | 2 (B23, B24) |
| **Total** | **26** | **25** |

Reproduction : 14 anomalies via script + 4 via navigateur = **18 constatées** ; 8 identifiées par audit.

---

## 8. Tests réalisés

Trois dossiers de tests sont actifs à ce stade :

- `test/integration/test_login.py` (4 tests, T-I01 à T-I04) ;
- `test/integration/test_booking_url.py` (4 tests, T-I05 à T-I07b) ;
- `test/integration/test_purchase.py` (16 cas, T-I08 à T-I22) ;
- `test/integration/test_securite.py` (6 tests, T-I23 à T-I28) ;
- `test/integration/test_interface.py` (3 tests, T-I29 à T-I31) ;
- `test/integration/test_points_public.py` (2 tests, T-I32 et T-I33) ;
- `test/unit/` : `test_club.py`, `test_competition.py`, `test_config.py`,
  `test_repository.py` et `test_booking.py` (32 tests, T-U01 à T-U30) ;
- `test/fonctionnel/test_parcours_complet.py` (3 parcours, T-F01 à T-F03).

### 8.1 Exécution

```cmd
python -m pytest -v
```

**Résultat actuel :**

```text
test/integration/test_booking_url.py ....
test/integration/test_interface.py ...
test/integration/test_login.py ....
test/integration/test_points_public.py ..
test/integration/test_purchase.py ................
test/integration/test_securite.py ......
test/unit/test_booking.py ...............
test/unit/test_club.py ......
test/unit/test_competition.py ....
test/unit/test_config.py ..
test/unit/test_repository.py .....
test/fonctionnel/test_parcours_complet.py ...
============================ 70 passed in 4.40s ==============================
```

**Preuve TDD (test de connexion, avant correction) :**

```text
test/integration/test_login.py::test_connexion_email_valide PASSED              [ 25%]
test/integration/test_login.py::test_connexion_email_inconnu_ne_provoque_pas_d_erreur_serveur FAILED [ 50%]
test/integration/test_login.py::test_connexion_champ_email_absent_ne_provoque_pas_d_erreur_serveur FAILED [ 75%]
test/integration/test_login.py::test_connexion_email_vide_ne_provoque_pas_d_erreur_serveur FAILED [100%]

E   IndexError: list index out of range
server.py:29: IndexError
========================= 3 failed, 1 passed in 2.03s =========================
```

Les tests unitaires ont également été écrits **avant** les modules `repository.py` et `club.py` :
pytest échouait au chargement avec `ModuleNotFoundError: No module named 'repository'`.

### 8.2 Détail des tests

| ID | Nom du test | Type | Vérifie | Résultat |
|---|---|---|---|---|
| T-I01 | `test_connexion_email_valide` | Intégration (happy) | HTTP 200 + `Welcome, john@simplylift.co` | VERT |
| T-I02 | `test_connexion_email_inconnu_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | HTTP 200 + message `not registered` | VERT |
| T-I03 | `test_connexion_champ_email_absent_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | HTTP 200 + message `not registered` | VERT |
| T-I04 | `test_connexion_email_vide_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | HTTP 200 + message `not registered` | VERT |
| T-I05 | `test_acces_page_reservation_valide` | Intégration (happy) | HTTP 200 + `Places available: 25` | VERT |
| T-I06 | `test_club_inconnu_dans_l_url_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | 200 (après redirection) + `does not exist` (B3) | VERT |
| T-I07 | `test_competition_inconnue_dans_l_url_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | 200 + `does not exist` (B4) | VERT |
| T-I07b | `test_club_et_competition_inconnus_ne_provoquent_pas_d_erreur_serveur` | Intégration (sad) | 200 + `does not exist` (B5) | VERT |
| T-I08 | `test_achat_valide_debute_le_stock` | Intégration (happy) | 200 + stock 25 → 24 | VERT |
| T-I09 | `test_competition_inconnue_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | 200 + `does not exist` (B6) | VERT |
| T-I10 | `test_club_inconnu_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | 200 + `does not exist` (B7) | VERT |
| T-I11 | `test_champ_places_absent_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | 200 + `invalid` (B8) | VERT |
| T-I12 | `test_places_non_numerique_ne_provoque_pas_d_erreur_serveur` | Intégration (sad) | 200 + `invalid` (B9) | VERT |
| T-I13 | `test_places_non_positives_refusees` (0 et -5) | Intégration (sad) | message + stock inchangé (B16) | VERT |
| T-I14 | `test_demande_superieure_au_stock_refusee` | Intégration (sad) | 200 + message + stock inchangé (B13) | VERT |
| T-I15 | `test_demande_egale_au_stock_acceptee` | Intégration (happy) | 200 + stock 0 (limite B13) | VERT |
| T-I16 | `test_demande_superieure_a_12_places_refusee` | Intégration (sad) | message + stock inchangé (B12) | VERT |
| T-I17 | `test_demande_de_12_places_acceptee` | Intégration (happy) | 200 + stock 13 (limite B12) | VERT |
| T-I18 | `test_solde_de_points_insuffisant_refuse` | Intégration (sad) | message + stock et points inchangés (B11) | VERT |
| T-I19 | `test_achat_debute_les_points_et_confirme_le_nombre` | Intégration (happy) | points 4 → 3 + « 1 place » (B10, B15) | VERT |
| T-I20 | `test_concours_complet_refuse` | Intégration (sad) | message « competition is full » (B14) | VERT |
| T-I21 | `test_achat_de_deux_places_debute_deux_points` | Intégration (happy) | points 13 → 11 + « 2 places » (B10, B15) | VERT |
| T-I22 | `test_achat_persiste_les_points_et_le_stock` | Intégration | disque : 12 points, 24 places (B17) | VERT |
| T-I23 | `test_reservation_refusee_sans_session` | Intégration (sad) | 302 vers `/` (B20) | VERT |
| T-I24 | `test_achat_refuse_sans_session` | Intégration (sad) | 302 + stock inchangé (B20) | VERT |
| T-I25 | `test_reservation_pour_un_autre_club_refusee` | Intégration (sad) | 302 si club ≠ session (B20) | VERT |
| T-I26 | `test_achat_pour_un_autre_club_refuse` | Intégration (sad) | 302 + stock inchangé (B20) | VERT |
| T-I27 | `test_deconnexion_ferme_la_session` | Intégration | `/book` 200 avant, 302 après `/logout` (B21) | VERT |
| T-I28 | `test_cle_secrete_n_est_plus_en_dur` | Intégration | clé ≠ `something_special`, longueur ≥ 32 (B19) | VERT |
| T-I29 | `test_welcome_affiche_seulement_les_competitions_a_venir` | Intégration | future affichée, passée masquée (B23) | VERT |
| T-I30 | `test_page_reservation_contient_les_contraintes_html` | Intégration | `id="places"`, `min="1"`, `max="12"` (B24) | VERT |
| T-I31 | `test_page_accueil_associe_le_label_et_le_champ` | Intégration | `id="email"` (B24) | VERT |
| T-I32 | `test_tableau_public_accessible_sans_connexion` | Intégration (happy) | `GET /points` → 200 sans session (F1) | VERT |
| T-I33 | `test_tableau_public_affiche_tous_les_clubs_et_leurs_points` | Intégration (happy) | 3 clubs + points, aucun email exposé (F1) | VERT |
| T-U01 | `test_load_clubs_lit_les_trois_clubs` | Unitaire | 3 clubs, premier = Simply Lift | VERT |
| T-U02 | `test_load_competitions_lit_les_deux_competitions` | Unitaire | 2 compétitions, première = Spring Festival | VERT |
| T-U03 | `test_load_clubs_fonctionne_depuis_un_autre_repertoire` | Unitaire | chargement indépendant du répertoire courant (B18) | VERT |
| T-U04 | `test_find_by_email_trouve_le_club` | Unitaire | retourne le club correspondant | VERT |
| T-U05 | `test_find_by_email_inconnu_retourne_none` | Unitaire | `None` si email inconnu (B1) | VERT |
| T-U06 | `test_find_by_email_ignore_les_espaces_autour` | Unitaire | `"  a@club.com  "` reconnu | VERT |
| T-U07 | `test_find_by_email_vide_retourne_none` | Unitaire | `""` → `None` (B2b) | VERT |
| T-U08 | `test_find_by_name_trouve_le_club` | Unitaire | retourne le club correspondant | VERT |
| T-U09 | `test_find_by_name_inconnu_retourne_none` | Unitaire | `None` si nom inconnu (B3) | VERT |
| T-U10 | `test_find_by_name_trouve_la_competition` | Unitaire | retourne la compétition correspondante | VERT |
| T-U11 | `test_find_by_name_inconnu_retourne_none` | Unitaire | `None` si nom inconnu (B4) | VERT |
| T-U12 | `test_parse_places_entier_valide` | Unitaire | `'3'` → `3` | VERT |
| T-U13 | `test_parse_places_accepte_les_espaces` | Unitaire | `' 3 '` → `3` | VERT |
| T-U14 | `test_parse_places_texte_retourne_none` | Unitaire | `'abc'` → `None` (B9) | VERT |
| T-U15 | `test_parse_places_absent_retourne_none` | Unitaire | `None` → `None` (B8) | VERT |
| T-U16 | `test_validate_refuse_quantite_non_positive` (0, -5) | Unitaire | message « at least one place » (B16) | VERT |
| T-U17 | `test_validate_accepte_quantite_positive` | Unitaire | `1` → `None` (aucune erreur) | VERT |
| T-U18 | `test_validate_refuse_demande_superieure_au_stock` | Unitaire | stock 3, demande 4 → message (B13) | VERT |
| T-U19 | `test_validate_accepte_demande_egale_au_stock` | Unitaire | stock 3, demande 3 → `None` (limite B13) | VERT |
| T-U20 | `test_validate_accepte_douze_places` | Unitaire | 12 places → `None` (limite B12) | VERT |
| T-U21 | `test_validate_refuse_plus_de_douze_places` | Unitaire | 13 places → message (B12) | VERT |
| T-U22 | `test_validate_refuse_solde_de_points_insuffisant` | Unitaire | 4 points, 5 places → message (B11) | VERT |
| T-U23 | `test_validate_refuse_concours_complet` | Unitaire | stock 0 → « competition is full » (B14) | VERT |
| T-U24 | `test_confirmation_message_indique_le_nombre_de_places` (1 et 2) | Unitaire | « 1 place » / « 2 places » (B15) | VERT |
| T-U25 | `test_save_clubs_ecrit_un_json_relisible` | Unitaire | écriture puis relecture (B17) | VERT |
| T-U26 | `test_save_competitions_ecrit_un_json_relisible` | Unitaire | écriture puis relecture (B17) | VERT |
| T-U27 | `test_secret_key_utilise_la_variable_d_environnement` | Unitaire | `SECRET_KEY` prioritaire (B19) | VERT |
| T-U28 | `test_secret_key_generee_si_variable_absente` | Unitaire | 64 caractères aléatoires (B19) | VERT |
| T-U29 | `test_upcoming_ne_garde_que_les_competitions_a_venir` | Unitaire | passée exclue, future gardée (B23) | VERT |
| T-U30 | `test_upcoming_garde_une_date_invalide` | Unitaire | date illisible conservée (B23) | VERT |
| T-F01 | `test_parcours_connexion_achat_et_consultation_publique` | Fonctionnel | connexion → réservation → achat → déconnexion → `/points` à jour | VERT |
| T-F02 | `test_parcours_limite_de_douze_places_par_achat` | Fonctionnel | 13 refusé, 12 accepté, puis 1 accepté jusqu'à 0 point | VERT |
| T-F03 | `test_parcours_stock_epuise_puis_refus` | Fonctionnel | dernier place achetée puis « competition is full » | VERT |

Répartition : **32 unitaires / 35 intégration / 3 fonctionnels**.

---

## 9. Backlog de tests (non écrits)

| Fichier | Tests prévus |
|---|---|
| `test/unit/test_repository.py` | fichier absent, JSON corrompu |
| Tous les autres fichiers | — (couvert) |

Le test de charge est réalisé (`locustfile.py`, 6 utilisateurs) ; il reste hors de pytest
car il nécessite un serveur en fonctionnement. Voir `rapport-de-performances.md`.

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

### 10.2 Branche `refactor/logique-metier` — B18

Objectif : sortir la logique de `server.py` **sans modifier le comportement** (les 4 tests
d'intégration restent verts), et rendre les chemins JSON indépendants du répertoire courant.

| Fichier créé | Contenu |
|---|---|
| `repository.py` | `load_clubs()`, `load_competitions()` ; chemins calculés depuis `Path(__file__).resolve().parent` |
| `club.py` | `MAX_PLACES = 12`, `find_by_email(clubs, email)` |

`server.py` se contente désormais d'appeler ces fonctions. `test/conftest.py` utilise
`repository.load_clubs()` / `load_competitions()` pour la réinitialisation entre tests.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B18 | chemins relatifs au répertoire courant | T-U03 |

### 10.3 Branche `bug/book-url-invalide` — B3, B4, B5, B5bis

```python
# AVANT
foundClub = [c for c in clubs if c['name'] == club][0]
foundCompetition = [c for c in competitions if c['name'] == competition][0]
if foundClub and foundCompetition:          # toujours vrai, sinon crash avant

# APRES
foundClub = find_club_by_name(clubs, club)
foundCompetition = find_competition_by_name(competitions, competition)
if foundClub is None or foundCompetition is None:
    flash("Sorry, this club or competition does not exist.")
    return redirect(url_for('index'))
```

`competition.py` est créé (`find_by_name`) et `club.py` reçoit `find_by_name`.
La branche `else` erronée (B5bis), qui passait une chaîne au template, est supprimée.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B3 | `IndexError` club inconnu | T-I06, T-U09 |
| B4 | `IndexError` compétition inconnue | T-I07, T-U11 |
| B5 | crash quand les deux sont inconnus | T-I07b |
| B5bis | branche `else` incorrecte | T-I06/T-I07 (plus de template avec une chaîne) |

Choix : message + redirection vers la page de connexion (HTTP 200 après redirection),
plutôt qu'une erreur 404 brute.

### 10.4 Branche `bug/purchase-form-invalide` — B6, B7, B8, B9

```python
# AVANT
competition = [c for c in competitions if c['name'] == request.form['competition']][0]
club = [c for c in clubs if c['name'] == request.form['club']][0]
placesRequired = int(request.form['places'])

# APRES
placesRequired = parse_places(request.form.get('places'))
foundCompetition = find_competition_by_name(competitions, request.form.get('competition'))
foundClub = find_club_by_name(clubs, request.form.get('club'))
if placesRequired is None: ...            # B8, B9
if foundClub is None or foundCompetition is None: ...   # B6, B7
```

`booking.py` est créé avec `parse_places()` : conversion protégée en entier, `None` si la
saisie est absente ou non numérique. `request.form.get()` remplace `request.form[...]`.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B6 | `IndexError` compétition inconnue | T-I09 |
| B7 | `IndexError` club inconnu | T-I10 |
| B8 | `BadRequestKeyError` champ absent | T-I11, T-U15 |
| B9 | `ValueError` sur `abc` | T-I12, T-U14 |

### 10.5 Branche `bug/places-invalides` — B16

`booking.validate_purchase(club, competition, places)` centralise les règles d'achat et
renvoie un message d'erreur (ou `None` si l'achat est valide) :

```python
def validate_purchase(club, competition, places):
    if places < 1:
        return 'Sorry, you must book at least one place.'
    return None
```

En cas d'erreur, `purchasePlaces` réaffiche le tableau de bord avec le message, **sans**
modifier le stock. Les règles suivantes seront ajoutées à cette même fonction.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B16 | aucune validation de la quantité | T-I13, T-U16, T-U17 |

### 10.6 Branche `bug/sur-reservation` — B13

```python
if places > int(competition['numberOfPlaces']):
    return 'Sorry, there are not enough places available.'
```

`int(...)` convertit la chaîne JSON (`"13"`) avant comparaison. En cas de refus, la route
réaffiche le tableau de bord et le stock reste inchangé.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B13 | stock non vérifié (stock négatif possible) | T-I14, T-I15, T-U18, T-U19 |

### 10.7 Branche `bug/limite-12-places` — B12

`MAX_PLACES` (déjà défini dans `club.py`) est enfin utilisé ; le message est construit à
partir de la constante :

```python
from club import MAX_PLACES

if places > MAX_PLACES:
    return (
        f'Sorry, you cannot book more than {MAX_PLACES} places '
        'per competition.'
    )
```

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B12 | quota de 12 places non appliqué | T-I16, T-I17, T-U20, T-U21 |

### 10.8 Branche `bug/points-et-messages` — B10, B11, B14, B15

Deux règles et un message s'ajoutent à `validate_purchase` :

```python
available = int(competition['numberOfPlaces'])
if available == 0:
    return 'Sorry, this competition is full.'
...
if places > int(club['points']):
    return 'Sorry, you do not have enough points.'
```

Le débit est appliqué par la route, **après** validation, et la confirmation indique le
nombre de places :

```python
foundClub['points'] = int(foundClub['points'])-placesRequired
flash(confirmation_message(placesRequired))
```

```python
def confirmation_message(places):
    suffix = 's' if places > 1 else ''
    return f'Great-booking complete! You have booked {places} place{suffix}.'
```

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B10 | points jamais débités | T-I19, T-I21 |
| B11 | solde de points non vérifié | T-I18, T-U22 |
| B14 | message de concours complet absent | T-I20, T-U23 |
| B15 | confirmation sans le nombre de places | T-I19, T-I21, T-U24 |

### 10.9 Branche `bug/persistance-json` — B17

`repository.py` gagne l'écriture, symétrique de la lecture, avec un chemin injectable pour
les tests et une écriture atomique :

```python
def save_clubs(clubs, path=None):
    _write({'clubs': clubs}, path or CLUBS_FILE)


def _write(data, path):
    path = Path(path)
    temporaire = path.with_name(path.name + '.tmp')
    with open(temporaire, 'w', encoding='utf-8') as fichier:
        json.dump(data, fichier, indent=4, ensure_ascii=False)
    temporaire.replace(path)
```

`purchasePlaces` enregistre les deux fichiers après avoir appliqué les changements. La
fixture `donnees_reinitialisees` sauvegarde et restaure les JSON réels autour de chaque
test, pour qu'un test de persistance ne pollue pas les suivants.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B17 | JSON jamais réécrits | T-I22, T-U25, T-U26 |

### 10.10 Branche `bug/robustesse-securite` — B19, B20, B21

`config.py` isole la clé de signature : variable d'environnement si elle existe, sinon une
valeur aléatoire (jamais versionnée). `showSummary` ouvre une session ; `book` et
`purchasePlaces` vérifient que la session existe **et** que le club demandé est celui de la
session ; `logout` ferme la session.

```python
# config.py
def secret_key():
    return os.environ.get('SECRET_KEY') or secrets.token_hex(32)

# showSummary
session['email'] = club['email']

# book / purchasePlaces
clubSession = club_de_session()
if clubSession is None:
    return refuser_sans_session()
...
if foundClub['name'] != clubSession['name']:
    flash("Sorry, you cannot book for another club.")
    return redirect(url_for('index'))

# logout
session.pop('email', None)
return redirect(url_for('index'))
```

Les 20 tests existants appelaient les routes sans session : la fixture `connecte(email)` a
été ajoutée et chaque test se connecte avec le club concerné.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B19 | `secret_key` en dur | T-I28, T-U27, T-U28 |
| B20 | aucune authentification, club non lié à la session | T-I23 à T-I26 |
| B21 | `/logout` sans effet | T-I27 |

B22 reste **atténué** (la fixture recharge les données), pas corrigé : les listes globales
demeurent un choix de conception du POC.

### 10.11 Branche `bug/interface` — B23, B24

Le filtrage est fait en Python, pas dans le template, pour être testable sans navigateur :

```python
def upcoming(competitions, maintenant=None):
    maintenant = maintenant or datetime.now()
    resultat = []
    for competition in competitions:
        try:
            date = datetime.strptime(competition['date'], DATE_FORMAT)
        except (KeyError, ValueError):
            resultat.append(competition)
            continue
        if date >= maintenant:
            resultat.append(competition)
    return resultat
```

Le tableau de bord utilise `upcoming(competitions)` (y compris après un achat, corrigé dans
la branche Flake8). HTML : `id="email"`, `id="places"`, `min="1"`, `max="12"` (constante
`MAX_PLACES` passée au template), `</br>` remplacé par `<br />`.

| Anomalie | Cause traitée | Tests |
|---|---|---|
| B23 | compétitions passées affichées | T-I29, T-U29, T-U30 |
| B24 | attributs HTML manquants ou invalides | T-I30, T-I31 |

### 10.12 Branche `chore/qualite-flake8`

`setup.cfg` fixe `max-line-length = 99` et exclut `.venv`, `.git`, `__pycache__` (sans quoi
`flake8 .` analyse les dépendances). Les lignes trop longues de `server.py`, `config.py`,
des tests et de `reproduction_bugs.py` ont été repliées ; les espaces manquants après
virgule et les lignes vides autour des fonctions ont été corrigés.

| Mesure | Avant | Après |
|---|---|---|
| `flake8 .` | 23 erreurs (limite 79) | **0 erreur** |

### 10.13 Branche `feature/tableau-points-public` — F1

La route publique ne dépend d'aucune session et ne rend que le nom et les points :

```python
@app.route('/points')
def points():
    return render_template('points.html', clubs=clubs)
```

`templates/points.html` contient un tableau en lecture seule ; `index.html` ajoute le lien
« View club points ». Les emails ne sont pas affichés (vérifié par T-I33).

| Élément | Tests |
|---|---|
| Accès sans connexion | T-I32 |
| Contenu des 3 clubs, sans email | T-I33 |

### 10.14 Branche `test/fonctionnels`

Trois parcours de bout en bout, via le client Flask, enchaînent les routes comme un
utilisateur :

| Test | Parcours |
|---|---|
| T-F01 | connexion → tableau de bord → réservation → achat de 2 places → déconnexion → `/points` |
| T-F02 | 13 places refusées, 12 acceptées, puis 1 place acceptée (points 13 → 1 → 0) |
| T-F03 | stock 1 → achat → stock 0 → refus « competition is full » |

### 10.15 Branche `perf/locust` — F2

`locustfile.py` simule 6 secrétaires (connexion, tableau de bord, réservation, points,
achat). Mesure de 30 s : **93 requêtes, 0 échec**, maximum **467 ms** pour la liste des
compétitions (seuil 5 s) et **82 ms** pour l'achat (seuil 2 s). Détail et limites dans
`rapport-de-performances.md`.

### 10.16 Reste à faire

| Élément | Statut |
|---|---|
| B22 | atténué par la fixture, non corrigé (limite §14) |
| Tests « fichier JSON absent / corrompu » | non écrits (backlog §9) |
| Protection CSRF | non prévue (limite §14) |

---

## 11. Couverture de code

**Commande (code applicatif uniquement) :**

```cmd
python -m pytest --cov=server --cov=repository --cov=club --cov=competition --cov=config --cov=booking --cov-report=term-missing -q
```

**Résultat mesuré (2026-10-26) :**

```text
Name             Stmts   Miss  Cover   Missing
----------------------------------------------
booking.py          22      0   100%
club.py              6      0   100%
competition.py      16      0   100%
config.py            4      0   100%
repository.py       21      0   100%
server.py           80      0   100%
----------------------------------------------
TOTAL              149      0   100%
70 passed in 4.40s
```

| Fichier | % | Lignes non couvertes |
|---|---|---|
| `booking.py` | 100 % | — |
| `club.py` | 100 % | — |
| `competition.py` | 100 % | — |
| `config.py` | 100 % | — |
| `repository.py` | 100 % | — |
| `server.py` | 100 % | — |
| **Total** | **100 %** | objectif ≥ 60 % largement atteint |

**Analyse** : l'ancienne ligne non couverte (`/logout`) l'est désormais (T-I27). Attention :
ces 100 % mesurent l'**exécution**, pas le respect des règles métier ni la sécurité
(voir les limites §14).

---

## 12. Flake8

**Commande :**

```cmd
python -m flake8 .
```

**Configuration** (`setup.cfg`) :

```ini
[flake8]
max-line-length = 99
exclude = .git,.venv,__pycache__,build,dist
```

**Résultat mesuré : 0 erreur** (aucune sortie).

Historique de la branche `chore/qualite-flake8` :

| Étape | Erreurs |
|---|---|
| Avant (hors `.venv`, limite 79) | 35 (dont 19 dans `reproduction_bugs.py`) |
| Après `setup.cfg` (limite 99) | 17 |
| Après repli des lignes et espaces | **0** |

| Fichier | Avant | Après |
|---|---|---|
| `server.py` | 18 (12 E231, 2 E302, 4 E501) | 0 |
| `reproduction_bugs.py` | 19 (E402, E302, E305, E501, W292) | 0 |
| `config.py` | 1 (E501) | 0 |
| tests | 4 (E501, W391) | 0 |
| `repository.py`, `club.py`, `competition.py`, `booking.py` | 0 | 0 |

La section 6 « Flake8 Report » du `README.md` indique la commande et le résultat (0 erreur).

---

## 13. Phase 2 — tableau public des points

**Terminée.**

| Élément | Attendu | État |
|---|---|---|
| Route `GET /points` | accessible sans connexion | **fait** (T-I32) |
| Template `templates/points.html` | tableau club / points, lecture seule | **fait** (T-I33) |
| Lien depuis `index.html` | navigation publique | **fait** |
| T-I32, T-I33 | 200 sans session + contenu exact | **écrit, VERT** |
| Parcours fonctionnels | 3 scénarios de bout en bout | **écrit, VERT** (T-F01 à T-F03) |
| Performance < 5 s / < 2 s | mesure Locust, 6 utilisateurs | **conforme** (467 ms / 82 ms, 0 échec) |

Détail des mesures : `rapport-de-performances.md`.

---

## 14. Écarts et limites

| # | Écart / limite | Impact |
|---|---|---|
| 1 | Section « Issues » du dépôt d'origine **vide** (0 issue) malgré l'annonce du commanditaire | Inventaire reconstruit par audit + reproduction ; exhaustivité non garantie |
| 2 | `requirements.txt` d'origine inutilisable (Flask 1.1.2 / MarkupSafe 1.1.1 / click 7.1.2 incompatibles Python 3.14) | Montée de version vers Flask 3.1.3 ; régressions couvertes par les tests au fur et à mesure |
| 3 | Compétitions de démonstration datées de 2020 (donc passées) alors que l'exigence porte sur les compétitions à venir | Le tableau de bord est vide avec les données d'origine ; les tests injectent une date future et le filtrage est vérifié (T-I29) |
| 4 | Couverture applicative de 100 % | Mesure d'exécution, pas de conformité métier |
| 5 | `coverage` mesure l'exécution, pas la qualité des assertions | Chaque fonctionnalité testée en happy + sad path |
| 6 | Locust mesure le serveur de développement Flask, sur la boucle locale, pendant 30 s | Résultats optimistes, mais très en dessous des seuils (5 s / 2 s) ; détails et limites dans `rapport-de-performances.md` |
| 7 | Le client de test Flask ne teste pas le JavaScript (ex. blocage de `abc` par `<input type="number">`) | D'où l'importance de la validation serveur (T-I12) |
| 8 | Les tests unitaires sont écrits au fil des branches, pas en bloc final | Répartition actuelle : 32 unitaires / 35 intégration / 3 fonctionnels |
| 9 | `clubs.json` et `competitions.json` sont écrits séparément (pas de transaction commune) | Un arrêt entre les deux écritures peut désynchroniser points et stock |
| 10 | Les tests de persistance écrivent dans les vrais fichiers JSON (restaurés par la fixture) | Ne pas lancer deux `pytest` en parallèle sur le même dossier |
| 11 | Aucune protection CSRF sur les formulaires | Un site tiers pourrait soumettre un achat à la place d'un utilisateur connecté |
| 12 | Sans `SECRET_KEY`, la clé est aléatoire par processus | Les sessions sont invalidées à chaque redémarrage (comportement attendu, à documenter en production) |
| 13 | Le filtrage des compétitions utilise l'heure locale du serveur | Un fuseau différent peut décaler la limite passé/futur |
| 14 | B22 non corrigé : listes globales chargées au démarrage | La fixture masque le problème dans les tests ; un rechargement à chaud n'est pas prévu |
| 15 | Test de charge de courte durée (30 s, 6 utilisateurs) sur données locales | Suffisant pour vérifier les seuils, pas pour dimensionner une production |

---

## 15. Conclusion

**État actuel** : **70 tests écrits, 70 verts** (32 unitaires, 35 intégration,
3 fonctionnels).
Anomalies corrigées : **25 sur 26** — connexion (B1, B2, B2b), chemins JSON (B18),
page de réservation (B3, B4, B5, B5bis), formulaire d'achat (B6, B7, B8, B9),
toutes les règles métier (B10 à B16), persistance (B17), sécurité (B19, B20, B21),
interface (B23, B24). B22 est atténué par la fixture, sans correction de conception.

**Phase 1** : terminée, `flake8 .` à 0 erreur.
**Phase 2** : terminée — tableau public (F1), 3 parcours fonctionnels et mesure de charge
Locust (F2) conforme aux seuils.

Points d'attention confirmés par les mesures :
- la couverture applicative est de **100 %**, mais elle mesure l'exécution, pas la qualité
  des assertions ;
- le code est **conforme Flake8** (0 erreur) ;
- les achats sont persistés, la session est obligatoire et liée au club, `/logout` ferme la
  session et les compétitions passées sont masquées ;
- le tableau public répond sans connexion et n'expose pas les emails ;
- performance mesurée : **467 ms** au maximum pour la liste des compétitions (seuil 5 s)
  et **82 ms** pour l'achat (seuil 2 s), 0 échec sur 93 requêtes ;
- aucune protection CSRF n'est en place et B22 reste une limite documentée (§14).

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

python -m pytest --cov=server --cov=repository --cov=club --cov=competition --cov=config --cov=booking --cov-report=term-missing --cov-report=html
python -m flake8 .

python -m flask --app server run --port 5011
locust -f locustfile.py --headless -u 6 -r 6 -t 30s --host http://127.0.0.1:5011
git checkout -- clubs.json competitions.json
```

## Annexe B — Arborescence

```text
.
├── server.py                   routes Flask
├── config.py                   clé de session (environnement ou aléatoire)
├── club.py                     MAX_PLACES, find_by_email, find_by_name
├── competition.py              find_by_name, upcoming
├── booking.py                  parse_places, validate_purchase
├── repository.py               load/save clubs et competitions (écriture atomique)
├── setup.cfg                   configuration Flake8
├── clubs.json
├── competitions.json
├── templates/
│   ├── index.html              connexion + messages flash + lien public
│   ├── welcome.html            tableau de bord (compétitions à venir)
│   ├── booking.html            formulaire d'achat (min/max)
│   └── points.html             tableau public des points
├── reproduction_bugs.py        reproduction des anomalies
├── locustfile.py               test de charge (6 utilisateurs)
├── rapport-de-test.md
├── rapport-de-performances.md
└── test/
    ├── __init__.py
    ├── conftest.py             fixtures client, connecte, réinitialisation
    ├── unit/
    │   ├── __init__.py
    │   ├── test_booking.py         (15 tests — VERT)
    │   ├── test_club.py            (6 tests — VERT)
    │   ├── test_competition.py     (4 tests — VERT)
    │   ├── test_config.py          (2 tests — VERT)
    │   └── test_repository.py      (5 tests — VERT)
    ├── integration/
    │   ├── __init__.py
    │   ├── test_login.py           (4 tests — VERT)
    │   ├── test_booking_url.py     (4 tests — VERT)
    │   ├── test_purchase.py        (16 tests — VERT)
    │   ├── test_securite.py        (6 tests — VERT)
    │   ├── test_interface.py       (3 tests — VERT)
    │   └── test_points_public.py   (2 tests — VERT)
    └── fonctionnel/
        ├── __init__.py
        └── test_parcours_complet.py (3 tests — VERT)
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
