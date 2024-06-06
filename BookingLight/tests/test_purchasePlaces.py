from unittest.mock import patch


@patch('BookingLight.views.writeCompetitions')
@patch('BookingLight.views.writeClubs')
@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_purchasePlaces(mock_loadClubs, mock_loadCompetitions, mock_writeClubs, mock_writeCompetitions, app_with_db):
    """test if the purchasePlaces route redirect to the good page with the good code in multiple condition

    Keyword arguments:
    mock_loadClubs -- the mock for the loadClubs
    mock_loadCompetitions -- the mock for the loadCompetitions
    mock_writeClubs -- the mock for the writeClubs
    mock_writeCompetitions -- the mock for the writeCompetitions
    app_with_db -- the testDB containing the test app and our false data

    Return: passed if all assert pass, else it's will return failed
    """
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
    """test if the purchasePlaces route redirect to the good page with the good code if not enough point

    Keyword arguments:
    mock_loadClubs -- the mock for the loadClubs
    mock_loadCompetitions -- the mock for the loadCompetitions
    mock_writeClubs -- the mock for the writeClubs
    mock_writeCompetitions -- the mock for the writeCompetitions
    app_with_db -- the testDB containing the test app and our false data

    Return: passed if all assert pass, else it's will return failed
    """

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
    """test if the purchasePlaces route redirect to the good page
    with the good code if try to purchase more than 12 points

    Keyword arguments:
    mock_loadClubs -- the mock for the loadClubs
    mock_loadCompetitions -- the mock for the loadCompetitions
    mock_writeClubs -- the mock for the writeClubs
    mock_writeCompetitions -- the mock for the writeCompetitions
    app_with_db -- the testDB containing the test app and our false data

    Return: passed if all assert pass, else it's will return failed
    """

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


@patch('BookingLight.views.writeCompetitions')
@patch('BookingLight.views.writeClubs')
@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_purchasePlaces_wrong_club(mock_loadClubs,
                                   mock_loadCompetitions,
                                   mock_writeClubs,
                                   mock_writeCompetitions,
                                   app_with_db
                                   ):
    """test if the purchasePlaces route redirect to the good page
    with the good code if not the right club

    Keyword arguments:
    mock_loadClubs -- the mock for the loadClubs
    mock_loadCompetitions -- the mock for the loadCompetitions
    mock_writeClubs -- the mock for the writeClubs
    mock_writeCompetitions -- the mock for the writeCompetitions
    app_with_db -- the testDB containing the test app and our false data

    Return: passed if all assert pass, else it's will return failed
    """

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_competitions[0]['numberOfPlaces'] = '25'
    mock_clubs[0]['points'] = '15'

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    response = flask_app.post('/purchasePlaces', data={
        'club': 'not existing',
        'competition': 'Test Competition',
        'places': '10'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>GUDLFT Registration</title>' in response.data
    assert b'<li>Something went wrong</li>' in response.data

    updated_club = mock_clubs[0]
    updated_competition = mock_competitions[0]
    assert updated_club['points'] == '15'
    assert updated_competition['numberOfPlaces'] == '25'


@patch('BookingLight.views.writeCompetitions')
@patch('BookingLight.views.writeClubs')
@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_purchasePlaces_wrong_competition(mock_loadClubs,
                                          mock_loadCompetitions,
                                          mock_writeClubs,
                                          mock_writeCompetitions,
                                          app_with_db
                                          ):
    """test if the purchasePlaces route redirect to the good page
    with the good code if wrong competition

    Keyword arguments:
    mock_loadClubs -- the mock for the loadClubs
    mock_loadCompetitions -- the mock for the loadCompetitions
    mock_writeClubs -- the mock for the writeClubs
    mock_writeCompetitions -- the mock for the writeCompetitions
    app_with_db -- the testDB containing the test app and our false data

    Return: passed if all assert pass, else it's will return failed
    """

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_competitions[0]['numberOfPlaces'] = '25'
    mock_clubs[0]['points'] = '15'

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    response = flask_app.post('/purchasePlaces', data={
        'club': 'Test Club',
        'competition': 'not existing',
        'places': '10'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>GUDLFT Registration</title>' in response.data
    assert b'<li>Something went wrong</li>' in response.data

    updated_club = mock_clubs[0]
    updated_competition = mock_competitions[0]
    assert updated_club['points'] == '15'
    assert updated_competition['numberOfPlaces'] == '25'
