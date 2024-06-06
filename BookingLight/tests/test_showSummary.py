from unittest.mock import patch


@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_showSummary(mock_loadClubs, mock_loadCompetitions, app_with_db):
    """test if the showSummary route redirect to the good page with the good code in multiple condition

    Keyword arguments:
    mock_loadClubs -- the mock for the loadClubs
    mock_loadCompetitions -- the mock for the loadCompetitions
    app_with_db -- the testDB containing the test app and our false data

    Return: passed if all assert pass, else it's will return failed
    """

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    for test_number in range(1, 3):
        if test_number == 1:  # test result if email not in Json data
            response = flask_app.post(
                '/showSummary', data={'email': 'notAnEmail'}, follow_redirects=True)

            assert response.status_code == 200
            assert b'<title>GUDLFT Registration</title>' in response.data
            assert b'<li>Sorry, that email wasn&#39;t found.</li>' in response.data

        if test_number == 2:  # test result if email is in Json data
            response = flask_app.post(
                '/showSummary', data={'email':  'test@club.com'}, follow_redirects=True)

            assert response.status_code == 200
            assert b'<title>Summary | GUDLFT Registration</title>' in response.data
