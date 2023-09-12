import pytest


@pytest.fixture(autouse=True)
def db_access(db):
    pass
