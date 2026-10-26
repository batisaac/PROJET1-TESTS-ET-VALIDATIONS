"""Tests unitaires du chargement des fichiers JSON."""

import json

import pytest

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


def test_load_clubs_fichier_absent(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_clubs(tmp_path / 'absent.json')


def test_load_competitions_fichier_absent(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_competitions(tmp_path / 'absent.json')


@pytest.mark.parametrize('charger, nom', [
    (load_clubs, 'clubs.json'),
    (load_competitions, 'competitions.json'),
])
def test_load_json_corrompu(tmp_path, charger, nom):
    chemin = tmp_path / nom
    chemin.write_text('{ pas du json', encoding='utf-8')

    with pytest.raises(json.JSONDecodeError):
        charger(chemin)


@pytest.mark.parametrize('charger, nom', [
    (load_clubs, 'clubs.json'),
    (load_competitions, 'competitions.json'),
])
def test_load_json_sans_cle_attendue(tmp_path, charger, nom):
    chemin = tmp_path / nom
    chemin.write_text('{"autre": []}', encoding='utf-8')

    with pytest.raises(KeyError):
        charger(chemin)


def test_save_clubs_conserve_les_accents(tmp_path):
    chemin = tmp_path / 'clubs.json'
    clubs = [{'name': 'Équipe Café', 'email': 'test@club.com', 'points': '7'}]

    save_clubs(clubs, chemin)

    assert load_clubs(chemin) == clubs


def test_save_competitions_conserve_tous_les_champs(tmp_path):
    chemin = tmp_path / 'competitions.json'
    competitions = [
        {
            'name': 'Coupe Été',
            'date': '2999-01-01 10:00:00',
            'numberOfPlaces': '5',
        },
    ]

    save_competitions(competitions, chemin)

    assert load_competitions(chemin) == competitions


def test_save_ne_laisse_pas_de_fichier_temporaire(tmp_path):
    chemin = tmp_path / 'clubs.json'

    save_clubs([], chemin)

    assert not (tmp_path / 'clubs.json.tmp').exists()


def test_save_liste_vide_puis_relecture(tmp_path):
    chemin = tmp_path / 'competitions.json'

    save_competitions([], chemin)

    assert load_competitions(chemin) == []


def test_save_remplace_le_contenu_existant(tmp_path):
    chemin = tmp_path / 'clubs.json'
    save_clubs([{'name': 'Ancien'}], chemin)

    save_clubs([{'name': 'Nouveau'}], chemin)

    assert load_clubs(chemin) == [{'name': 'Nouveau'}]
