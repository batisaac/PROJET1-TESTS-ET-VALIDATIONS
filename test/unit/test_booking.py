"""Tests unitaires des regles d'achat de places."""

import pytest

from booking import confirmation_message, parse_places, validate_purchase

CLUB = {'points': '13'}
COMPETITION = {'numberOfPlaces': '25'}
COMPETITION_PETITE = {'numberOfPlaces': '3'}
CLUB_RICHE = {'points': '100'}
COMPETITION_GRANDE = {'numberOfPlaces': '100'}
CLUB_PAUVRE = {'points': '4'}
COMPETITION_COMPLETE = {'numberOfPlaces': '0'}
CLUB_ZERO = {'points': '0'}
CLUB_ONZE = {'points': '11'}
CLUB_DOUZE = {'points': '12'}
COMPETITION_UNE = {'numberOfPlaces': '1'}
COMPETITION_QUATRE = {'numberOfPlaces': '4'}
COMPETITION_DOUZE = {'numberOfPlaces': '12'}


def test_parse_places_entier_valide():
    assert parse_places('3') == 3


def test_parse_places_accepte_les_espaces():
    assert parse_places(' 3 ') == 3


def test_parse_places_texte_retourne_none():
    assert parse_places('abc') is None


def test_parse_places_absent_retourne_none():
    assert parse_places(None) is None


@pytest.mark.parametrize('places', [0, -5])
def test_validate_refuse_quantite_non_positive(places):
    message = validate_purchase(CLUB, COMPETITION, places)

    assert 'at least one place' in message


def test_validate_accepte_quantite_positive():
    assert validate_purchase(CLUB, COMPETITION, 1) is None


def test_validate_refuse_demande_superieure_au_stock():
    message = validate_purchase(CLUB, COMPETITION_PETITE, 4)

    assert 'not enough places' in message


def test_validate_accepte_demande_egale_au_stock():
    assert validate_purchase(CLUB, COMPETITION_PETITE, 3) is None


def test_validate_accepte_douze_places():
    assert validate_purchase(CLUB_RICHE, COMPETITION_GRANDE, 12) is None


def test_validate_refuse_plus_de_douze_places():
    message = validate_purchase(CLUB_RICHE, COMPETITION_GRANDE, 13)

    assert 'more than 12 places' in message


def test_validate_refuse_solde_de_points_insuffisant():
    message = validate_purchase(CLUB_PAUVRE, COMPETITION, 5)

    assert 'do not have enough points' in message


def test_validate_refuse_concours_complet():
    message = validate_purchase(CLUB, COMPETITION_COMPLETE, 1)

    assert 'competition is full' in message


@pytest.mark.parametrize('places, attendu', [
    (1, 'You have booked 1 place.'),
    (2, 'You have booked 2 places.'),
])
def test_confirmation_message_indique_le_nombre_de_places(places, attendu):
    assert attendu in confirmation_message(places)


@pytest.mark.parametrize('saisie, attendu', [
    ('+3', 3),
    ('0', 0),
    ('-5', -5),
    ('', None),
    ('   ', None),
    ('3.0', None),
    ('3 places', None),
    ('12\n', 12),
])
def test_parse_places_cas_limites(saisie, attendu):
    assert parse_places(saisie) == attendu


@pytest.mark.parametrize('club, competition, places, attendu', [
    (CLUB_PAUVRE, COMPETITION_COMPLETE, 0, 'at least one place'),
    (CLUB_PAUVRE, COMPETITION_COMPLETE, 13, 'competition is full'),
    (CLUB_PAUVRE, COMPETITION_PETITE, 13, 'not enough places'),
    (CLUB_PAUVRE, COMPETITION_GRANDE, 13, 'more than 12 places'),
    (CLUB_PAUVRE, COMPETITION_GRANDE, 5, 'do not have enough points'),
    (CLUB_PAUVRE, COMPETITION_GRANDE, 4, None),
])
def test_validate_respecte_l_ordre_des_regles(club, competition, places,
                                              attendu):
    message = validate_purchase(club, competition, places)

    if attendu is None:
        assert message is None
    else:
        assert attendu in message


@pytest.mark.parametrize('club, competition, places', [
    (CLUB_RICHE, COMPETITION_UNE, 1),
    (CLUB_DOUZE, COMPETITION_DOUZE, 12),
    (CLUB_PAUVRE, COMPETITION_QUATRE, 4),
])
def test_validate_accepte_les_bornes(club, competition, places):
    assert validate_purchase(club, competition, places) is None


def test_validate_refuse_un_point_de_moins():
    message = validate_purchase(CLUB_ONZE, COMPETITION, 12)

    assert 'do not have enough points' in message


def test_validate_refuse_un_club_sans_point():
    message = validate_purchase(CLUB_ZERO, COMPETITION, 1)

    assert 'do not have enough points' in message


@pytest.mark.parametrize('places, attendu', [
    (1, 'Great-booking complete! You have booked 1 place.'),
    (12, 'Great-booking complete! You have booked 12 places.'),
])
def test_confirmation_message_est_exact(places, attendu):
    assert confirmation_message(places) == attendu
