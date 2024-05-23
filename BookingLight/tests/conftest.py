import pytest

from BookingLight import app


@pytest.fixture(scope="session")
def flask_app():
    app

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope="session")
def app_with_db(flask_app):

    club = {
        'name': 'Test Club',
        'email': 'test@club.com',
        'points': '15'
    }
    competition = {
        'name': 'Test Competition',
        'date': '2024-06-15 13:30:00',
        'numberOfPlaces': '10'
    }

    yield flask_app, [competition], [club]
