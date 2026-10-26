"""Reproduction des bogues de la phase 1 - Etat initial
A executer AVANT toute correction.
Usage : python reproduction_bugs.py

Ce script reflete l'etat du depot AVANT les corrections (commit initial) :
certaines routes ont depuis change de comportement.
"""

import sys

from server import app

sys.stdout.reconfigure(encoding="utf-8")

client = app.test_client()


def log(nom, resp, attendu=200):
    ok = resp.status_code == attendu
    statut = 'OK ' if ok else 'BUG'
    print(
        f"{statut} | {nom:<58} | recu={resp.status_code} "
        f"| attendu={attendu}"
    )


def acheter(club, competition, places=None):
    data = {"club": club, "competition": competition}
    if places is not None:
        data["places"] = places
    return client.post("/purchasePlaces", data=data)


print("=" * 70)
print("REPRODUCTION DES BUGS - ETAT INITIAL")
print("=" * 70)

print("\n[1] CONNEXION")
log("B1 - Email inconnu", client.post(
    "/showSummary", data={"email": "inconnu@club.com"}))
log("B2 - Champ email absent", client.post("/showSummary", data={}))
log("B2b - Email vide", client.post("/showSummary", data={"email": ""}))

print("\n[2] RESERVATION VIA URL")
log("B3 - Club inconnu dans l'URL", client.get(
    "/book/Spring Festival/Fake"))
log("B4 - Competition inconnue dans l'URL", client.get(
    "/book/Fake/Simply Lift"))
log("B5 - Les deux inconnus", client.get("/book/Fake/Fake"))

print("\n[3] ACHAT DE PLACES - FORMULAIRE")
log("B6 - Competition inconnue dans le formulaire",
    acheter("Simply Lift", "Fake", "1"))
log("B7 - Club inconnu dans le formulaire",
    acheter("Fake", "Spring Festival", "1"))
log("B8 - Champ 'places' manquant",
    acheter("Simply Lift", "Spring Festival"))
log("B9 - 'places' non entier 'abc'",
    acheter("Simply Lift", "Spring Festival", "abc"))

print("\n[4] REGLES METIER")
r = acheter("Simply Lift", "Fall Classic", "999")
print(
    "BUG | B13 - 999 places alors que Fall Classic n'en a que 13 "
    f"| status={r.status_code}")

r = acheter("Simply Lift", "Spring Festival", "20")
print(
    "BUG | B12 - 20 places (> 12 autorises)                    "
    f"| status={r.status_code}")

r = acheter("Simply Lift", "Spring Festival", "-5")
print(
    "BUG | B16 - Places negatives                             "
    f"| status={r.status_code}")

r = acheter("Iron Temple", "Spring Festival", "5")
print(
    "BUG | B11 - 5 places pour Iron Temple (4 points)         "
    f"| status={r.status_code}")

print("\n" + "=" * 70)
print("FIN - Copie TOUTE cette sortie dans ton rapport de test")
print("=" * 70)
