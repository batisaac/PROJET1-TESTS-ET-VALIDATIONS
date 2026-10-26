"""Tests unitaires du chargement des fichiers JSON."""

from repository import (
    load_clubs,
    load_competitions,
    save_clubs,
    save_competitions,
)


def test_load_clubs_lit_les_trois_clubs():
    clubs = load_clubs()

    assert len(clubs) == 3
    assert clubs[0]['name'] == 'Simply Lift'


def test_load_competitions_lit_les_deux_competitions():
    competitions = load_competitions()

    assert len(competitions) == 2
    assert competitions[0]['name'] == 'Spring Festival'


def test_load_clubs_fonctionne_depuis_un_autre_repertoire(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    clubs = load_clubs()

    assert len(clubs) == 3


def test_save_clubs_ecrit_un_json_relisible(tmp_path):
    chemin = tmp_path / 'clubs.json'
    clubs = [{'name': 'Test Club', 'email': 'test@club.com', 'points': '7'}]

    save_clubs(clubs, chemin)

    assert load_clubs(chemin) == clubs


def test_save_competitions_ecrit_un_json_relisible(tmp_path):
    chemin = tmp_path / 'competitions.json'
    competitions = [{'name': 'Test Cup', 'numberOfPlaces': '5'}]

    save_competitions(competitions, chemin)

    assert load_competitions(chemin) == competitions
