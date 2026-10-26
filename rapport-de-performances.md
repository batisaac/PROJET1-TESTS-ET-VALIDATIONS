# Rapport de performances — GUDLFT (phase 2)

> Version 1.0 — 2026-10-26
> Auteur : Isaac Batoua (`batisaac`)
> Dépôt : <https://github.com/batisaac/PROJET1-TESTS-ET-VALIDATIONS>
> Outil : Locust 2.47.0

## 1. Objectif

Vérifier les deux exigences de performance de la phase 2 :

| Exigence | Seuil |
|---|---|
| Récupérer la liste des compétitions | **< 5 s** |
| Mettre à jour le total de points (achat) | **< 2 s** |

## 2. Environnement de mesure

| Élément | Valeur |
|---|---|
| Machine | poste de développement Windows |
| Serveur | Flask 3.1.3, serveur de développement (`flask run`), port 5011 |
| Client | Locust 2.47.0, même machine (boucle locale) |
| Utilisateurs simulés | **6** (montée en charge 6 utilisateurs/s) |
| Durée | **30 secondes** |
| Données | `clubs.json` / `competitions.json` restaurés avant la mesure |

## 3. Scénario (`locustfile.py`)

Chaque utilisateur se connecte (`POST /showSummary` avec `john@simplylift.co`) puis exécute
aléatoirement, avec un temps d'attente de 1 à 2 s :

| Tâche | Poids | Requête |
|---|---|---|
| Lister les compétitions | 3 | `POST /showSummary` |
| Ouvrir la réservation | 2 | `GET /book/Spring Festival/Simply Lift` |
| Consulter le tableau public | 2 | `GET /points` |
| Acheter une place | 1 | `POST /purchasePlaces` |

## 4. Commande

```cmd
python -m flask --app server run --port 5011
locust -f locustfile.py --headless -u 6 -r 6 -t 30s --host http://127.0.0.1:5011
```

La tâche d'achat écrit dans `clubs.json` et `competitions.json`. Après la mesure :

```cmd
git checkout -- clubs.json competitions.json
```

## 5. Résultats mesurés

```text
Type     Name                    # reqs   # fails |    Avg     Min     Max    Med
GET      GET /book                   23   0(0.00%) |     29      20      62     25
GET      GET /points                 22   0(0.00%) |     36      21     100     26
POST     POST /purchasePlaces        11   0(0.00%) |     57      50      82     54
POST     POST /showSummary           37   0(0.00%) |     93      26     467     33
-------------------------------------------------------------------------------
         Aggregated                  93   0(0.00%) |     59      20     467     28
```

| Requête | Requêtes | Échecs | Moyenne | Médiane | 95 % | Max |
|---|---|---|---|---|---|---|
| `GET /book` | 23 | 0 | 29 ms | 25 ms | 48 ms | 62 ms |
| `GET /points` | 22 | 0 | 36 ms | 26 ms | 98 ms | 100 ms |
| `POST /purchasePlaces` | 11 | 0 | 57 ms | 54 ms | 83 ms | **82 ms** |
| `POST /showSummary` | 37 | 0 | 93 ms | 33 ms | 370 ms | **467 ms** |
| **Agrégé** | **93** | **0** | 59 ms | 28 ms | 330 ms | 467 ms |

Débit moyen : **4,10 requêtes/s**, **0 % d'échec**.

Une première mesure de 20 s (même scénario, port 5010) donnait 45 requêtes, 0 échec,
maximum 450 ms (`/showSummary`) et 62 ms (`/purchasePlaces`) : résultats cohérents.

## 6. Comparaison aux seuils

| Exigence | Mesure | Seuil | Marge | Verdict |
|---|---|---|---|---|
| Liste des compétitions (`POST /showSummary`) | max **467 ms** | 5 000 ms | × 10,7 | **conforme** |
| Mise à jour des points (`POST /purchasePlaces`) | max **82 ms** | 2 000 ms | × 24,4 | **conforme** |

Aucune requête n'a dépassé les seuils, y compris au 100e centile de l'échantillon.

## 7. Analyse

- Les pages en lecture (`/book`, `/points`) répondent en quelques dizaines de millisecondes.
- `POST /showSummary` est la route la plus lente (médiane 33 ms, 95e centile 370 ms) : elle
  rend le tableau de bord et filtre les compétitions à chaque appel. Le maximum isolé
  (467 ms) reste très en dessous du seuil de 5 s.
- `POST /purchasePlaces` écrit deux fichiers JSON (écriture atomique via fichier `.tmp` puis
  remplacement) et reste sous 100 ms, très loin du seuil de 2 s.
- Les 0 % d'échec confirment qu'aucune requête n'a produit d'erreur HTTP pendant la mesure.

## 8. Limites

| # | Limite | Impact |
|---|---|---|
| 1 | Serveur de développement Flask (mono-processus, `threaded`) | Le débit absolu serait plus élevé avec un serveur de production (gunicorn/waitress) |
| 2 | Client et serveur sur la même machine (boucle locale) | Pas de latence réseau ; les temps sont optimistes |
| 3 | Mesure de 30 s et 6 utilisateurs | Échantillon volontairement conforme au guide ; ce n'est pas un test de charge longue durée |
| 4 | Tâche d'achat qui épuise les points/places | Après quelques achats, les requêtes suivantes sont refusées (HTTP 200) ; le temps de réponse reste mesuré |
| 5 | Données réelles modifiées par les achats | Restauration obligatoire (`git checkout -- clubs.json competitions.json`) |

## 9. Conclusion

Les deux exigences de performance de la phase 2 sont **respectées avec une large marge** :
maximum 467 ms pour la liste des compétitions (seuil 5 s) et 82 ms pour la mise à jour des
points (seuil 2 s), sans aucun échec sur 93 requêtes.
