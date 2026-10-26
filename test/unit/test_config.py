"""Tests unitaires de la configuration."""

from config import secret_key


def test_secret_key_utilise_la_variable_d_environnement(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'cle-de-test')

    assert secret_key() == 'cle-de-test'


def test_secret_key_generee_si_variable_absente(monkeypatch):
    monkeypatch.delenv('SECRET_KEY', raising=False)

    assert len(secret_key()) == 64


def test_secret_key_generee_si_variable_vide(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', '')

    assert len(secret_key()) == 64


def test_secret_key_generee_est_hexadecimale(monkeypatch):
    monkeypatch.delenv('SECRET_KEY', raising=False)
    cle = secret_key()

    assert all(caractere in '0123456789abcdef' for caractere in cle)


def test_secret_key_generee_change_a_chaque_appel(monkeypatch):
    monkeypatch.delenv('SECRET_KEY', raising=False)

    assert secret_key() != secret_key()
