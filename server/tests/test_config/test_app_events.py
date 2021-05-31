from unittest import mock
from unittest.mock import Mock

from starlette.testclient import TestClient

from src.main import app


@mock.patch("src.main.init_database")
def test_app_events(mock_init_db: Mock):
    """Tests app startup & shutdown events."""
    with TestClient(app):
        mock_init_db.assert_called_once()
