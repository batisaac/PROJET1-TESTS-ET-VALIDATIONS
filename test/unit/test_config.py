"""Tests unitaires de la configuration."""

from config import secret_key


def test_secret_key_utilise_la_variable_d_environnement(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'cle-de-test')

    assert secret_key() == 'cle-de-test'


def test_secret_key_generee_si_variable_absente(monkeypatch):
    monkeypatch.delenv('SECRET_KEY', raising=False)

    assert len(secret_key()) == 64
