from unittest.mock import patch


@patch('BookingLight.views.writeCompetitions')
@patch('BookingLight.views.writeClubs')
@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_purchasePlaces(mock_loadClubs, mock_loadCompetitions, mock_writeClubs, mock_writeCompetitions, app_with_db):
    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_competitions[0]['numberOfPlaces'] = '10'
    mock_clubs[0]['points'] = '15'

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


@patch('BookingLight.views.writeCompetitions')
@patch('BookingLight.views.writeClubs')
@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_purchasePlaces_not_enough_point(mock_loadClubs,
                                         mock_loadCompetitions,
                                         mock_writeClubs,
                                         mock_writeCompetitions,
                                         app_with_db
                                         ):

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_competitions[0]['numberOfPlaces'] = '25'
    mock_clubs[0]['points'] = '9'

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    response = flask_app.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '10'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>Booking for Test Competition || GUDLFT</title>' in response.data
    assert b'<li>You didn&#39;t have enough points to redeems 10 places, you only have 9</li>' in response.data

    updated_club = mock_clubs[0]
    updated_competition = mock_competitions[0]
    assert updated_club['points'] == '9'
    assert updated_competition['numberOfPlaces'] == '25'


@patch('BookingLight.views.writeCompetitions')
@patch('BookingLight.views.writeClubs')
@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_purchasePlaces_more_than_12(mock_loadClubs,
                                     mock_loadCompetitions,
                                     mock_writeClubs,
                                     mock_writeCompetitions,
                                     app_with_db
                                     ):

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_competitions[0]['numberOfPlaces'] = '25'
    mock_clubs[0]['points'] = '15'

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    response = flask_app.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'Test Competition',
        'places': '14'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>Booking for Test Competition || GUDLFT</title>' in response.data
    assert b'<li>You can&#39;t book more than 12 places</li>' in response.data

    updated_club = mock_clubs[0]
    updated_competition = mock_competitions[0]
    assert updated_club['points'] == '15'
    assert updated_competition['numberOfPlaces'] == '25'


@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_book(mock_loadClubs, mock_loadCompetitions, app_with_db):

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_competitions[0]['date'] = '2022-06-15 13:30:00'

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    for test_number in range(1, 3):
        if test_number == 1:
            response = flask_app.get(
                f'/book/{mock_competitions[0]['name']}/{mock_clubs[0]['name']}', follow_redirects=True)

            assert response.status_code == 200
            assert b'<title>Summary | GUDLFT Registration</title>' in response.data
            assert b'<li>Error, this competitions has already ended.</li>' in response.data

        if test_number == 2:
            mock_competitions[0]['date'] = '2050-06-15 13:30:00'
            response = flask_app.get(
                f'/book/{mock_competitions[0]['name']}/{mock_clubs[0]['name']}', follow_redirects=True)

            assert response.status_code == 200
            assert b'<title>Booking for Test Competition || GUDLFT</title>' in response.data
            assert b'<li>This competitions is still available</li>' in response.data
