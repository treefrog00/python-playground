from flask_thingy import main
import pytest


@pytest.fixture
def client():
    main.app.config['TESTING'] = True

    with main.app.test_client() as client:
        yield client
