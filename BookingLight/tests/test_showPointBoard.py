from unittest.mock import patch


@patch('BookingLight.views.loadClubs')
def test_pointBoard(mock_loadClubs, app_with_db):

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_loadClubs.return_value = mock_clubs

    response = flask_app.get('/showPointBoard', follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>GUDLFT Point Board</title>' in response.data
    assert b'<td>Test Club</td>' in response.data
    assert b'<td>15</td>' in response.data
