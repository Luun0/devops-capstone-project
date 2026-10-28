"""Verify database environment configuration without making a connection."""
import importlib
import os
from unittest import TestCase
from unittest.mock import patch
from service import config


class TestConfig(TestCase):
    """Environment configuration tests."""

    def test_database_components(self):
        """It should build a database URI from individual environment values."""
        with patch.dict(os.environ, {
            "DATABASE_URI": "", "DATABASE_USER": "demo", "DATABASE_PASSWORD": "test",
            "DATABASE_HOST": "db", "DATABASE_NAME": "accounts"
        }):
            importlib.reload(config)
            self.assertEqual(config.SQLALCHEMY_DATABASE_URI,
                             "postgresql://demo:test@db:5432/accounts")
        importlib.reload(config)
