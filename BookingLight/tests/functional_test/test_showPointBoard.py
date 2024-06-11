from unittest.mock import patch


@patch('BookingLight.views.loadClubs')
def test_pointBoard(mock_loadClubs, app_with_db):
    """test if the pointBoard route redirect to the good page with the good code

    Keyword arguments:
    mock_loadClubs -- the mock for the loadClubs
    app_with_db -- the testDB containing the test app and our false data

    Return: passed if all assert pass, else it's will return failed
    """

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_loadClubs.return_value = mock_clubs

    response = flask_app.get('/showPointBoard', follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>GUDLFT Point Board</title>' in response.data
    assert b'<td>Test Club</td>' in response.data
    assert b'<td>15</td>' in response.data
