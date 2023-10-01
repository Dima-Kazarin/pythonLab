import pytest
from unittest.mock import MagicMock


@pytest.fixture(scope='session')
def cursor():
    return MagicMock()
