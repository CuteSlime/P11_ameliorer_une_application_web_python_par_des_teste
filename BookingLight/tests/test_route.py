from unittest.mock import patch


@patch('BookingLight.views.writeCompetitions')
@patch('BookingLight.views.writeClubs')
@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_purchasePlaces(mock_loadClubs, mock_loadCompetitions, mock_writeClubs, mock_writeCompetitions, app_with_db):
    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    response = flask_app.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '5'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>Summary | GUDLFT Registration</title>' in response.data
    updated_club = mock_clubs[0]
    updated_competition = mock_competitions[0]
    assert updated_club['points'] == '10'
    assert updated_competition['numberOfPlaces'] == '5'
    mock_writeClubs.assert_called_once_with(mock_clubs)
    mock_writeCompetitions.assert_called_once_with(mock_competitions)
