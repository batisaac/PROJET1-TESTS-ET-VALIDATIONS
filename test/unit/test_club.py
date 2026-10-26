"""Tests unitaires de la recherche d'un club."""

from club import find_by_email, find_by_name


def test_find_by_email_trouve_le_club():
    clubs = [{'email': 'a@club.com'}, {'email': 'b@club.com'}]

    assert find_by_email(clubs, 'b@club.com') == {'email': 'b@club.com'}


def test_find_by_email_inconnu_retourne_none():
    clubs = [{'email': 'a@club.com'}]

    assert find_by_email(clubs, 'inconnu@club.com') is None


def test_find_by_email_ignore_les_espaces_autour():
    clubs = [{'email': 'a@club.com'}]

    assert find_by_email(clubs, '  a@club.com  ') == {'email': 'a@club.com'}


def test_find_by_email_vide_retourne_none():
    clubs = [{'email': 'a@club.com'}]

    assert find_by_email(clubs, '') is None


def test_find_by_name_trouve_le_club():
    clubs = [{'name': 'Simply Lift'}, {'name': 'Iron Temple'}]

    assert find_by_name(clubs, 'Iron Temple') == {'name': 'Iron Temple'}


def test_find_by_name_inconnu_retourne_none():
    clubs = [{'name': 'Simply Lift'}]

    assert find_by_name(clubs, 'Fake') is None


def test_find_by_email_ignore_les_tabulations():
    clubs = [{'email': 'a@club.com'}]

    assert find_by_email(clubs, '\ta@club.com\n') == {'email': 'a@club.com'}


def test_find_by_email_none_retourne_none():
    clubs = [{'email': 'a@club.com'}]

    assert find_by_email(clubs, None) is None


def test_find_by_email_espaces_seuls_retourne_none():
    clubs = [{'email': 'a@club.com'}]

    assert find_by_email(clubs, '   ') is None


def test_find_by_email_est_sensible_a_la_casse():
    clubs = [{'email': 'a@club.com'}]

    assert find_by_email(clubs, 'A@CLUB.COM') is None


def test_find_by_name_vide_retourne_none():
    clubs = [{'name': 'Simply Lift'}]

    assert find_by_name(clubs, '') is None
