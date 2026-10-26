"""Tests unitaires du chargement des fichiers JSON."""

from repository import load_clubs, load_competitions


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
