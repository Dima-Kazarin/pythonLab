import pytest
from unittest.mock import MagicMock


@pytest.fixture
def cursor():
    return MagicMock()
