"""Test de charge GUDLFT (Locust).

6 utilisateurs simulent des secretaires de club : consultation du tableau de
bord, de la page de reservation, du tableau public des points et achat d'une
place.

Attention : la tache d'achat ecrit dans clubs.json et competitions.json.
Restaurer les donnees apres la mesure :
    git checkout -- clubs.json competitions.json
"""

from locust import HttpUser, between, task

EMAIL = 'john@simplylift.co'


class SecretaireClub(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.post(
            '/showSummary',
            data={'email': EMAIL},
            name='POST /showSummary',
        )

    @task(3)
    def lister_les_competitions(self):
        self.client.post(
            '/showSummary',
            data={'email': EMAIL},
            name='POST /showSummary',
        )

    @task(2)
    def ouvrir_la_reservation(self):
        self.client.get(
            '/book/Spring Festival/Simply Lift',
            name='GET /book',
        )

    @task(2)
    def consulter_les_points(self):
        self.client.get('/points', name='GET /points')

    @task(1)
    def acheter_une_place(self):
        self.client.post(
            '/purchasePlaces',
            data={
                'club': 'Simply Lift',
                'competition': 'Spring Festival',
                'places': '1',
            },
            name='POST /purchasePlaces',
        )
