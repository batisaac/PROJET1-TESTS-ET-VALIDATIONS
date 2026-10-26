"""Configuration de l'application."""

import os
import secrets


def secret_key():
    """Cle de signature des sessions : variable d'environnement ou aleatoire."""
    return os.environ.get('SECRET_KEY') or secrets.token_hex(32)
