"""Reproduction des bogues de la phase 1 - Etat initial
A exécuter AVANT toute correction.
Usage : python reproduction_bugs.py
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from server import app

client = app.test_client()

def log(nom, resp, attendu=200):
    ok = resp.status_code == attendu
    print(f"{'OK ' if ok else 'BUG'} | {nom:<58} | recu={resp.status_code} | attendu={attendu}")

print("="*70)
print("REPRODUCTION DES BUGS - ETAT INITIAL")
print("="*70)

print("\n[1] CONNEXION")
log("B1 - Email inconnu", client.post("/showSummary", data={"email": "inconnu@club.com"}))
log("B2 - Champ email absent", client.post("/showSummary", data={}))
log("B2b - Email vide", client.post("/showSummary", data={"email": ""}))

print("\n[2] RESERVATION VIA URL")
log("B3 - Club inconnu dans l'URL", client.get("/book/Spring Festival/Fake"))
log("B4 - Competition inconnue dans l'URL", client.get("/book/Fake/Simply Lift"))
log("B5 - Les deux inconnus", client.get("/book/Fake/Fake"))

print("\n[3] ACHAT DE PLACES - FORMULAIRE")
log("B6 - Competition inconnue dans le formulaire", client.post("/purchasePlaces", data={"club": "Simply Lift", "competition": "Fake", "places": "1"}))
log("B7 - Club inconnu dans le formulaire", client.post("/purchasePlaces", data={"club": "Fake", "competition": "Spring Festival", "places": "1"}))
log("B8 - Champ 'places' manquant", client.post("/purchasePlaces", data={"club": "Simply Lift", "competition": "Spring Festival"}))
log("B9 - 'places' non entier 'abc'", client.post("/purchasePlaces", data={"club": "Simply Lift", "competition": "Spring Festival", "places": "abc"}))

print("\n[4] REGLES METIER")
r = client.post("/purchasePlaces", data={"club": "Simply Lift", "competition": "Fall Classic", "places": "999"})
print(f"BUG | B13 - 999 places alors que Fall Classic n'en a que 13 | status={r.status_code}")

r = client.post("/purchasePlaces", data={"club": "Simply Lift", "competition": "Spring Festival", "places": "20"})
print(f"BUG | B12 - 20 places (> 12 autorises)                    | status={r.status_code}")

r = client.post("/purchasePlaces", data={"club": "Simply Lift", "competition": "Spring Festival", "places": "-5"})
print(f"BUG | B16 - Places negatives                             | status={r.status_code}")

r = client.post("/purchasePlaces", data={"club": "Iron Temple", "competition": "Spring Festival", "places": "5"})
print(f"BUG | B11 - 5 places pour Iron Temple (4 points)         | status={r.status_code}")

print("\n" + "="*70)
print("FIN - Copie TOUTE cette sortie dans ton rapport de test")
print("="*70)