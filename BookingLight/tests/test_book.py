from unittest.mock import patch


@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_book(mock_loadClubs, mock_loadCompetitions, app_with_db):
    """test if the book route redirect to the good page with the good code in multiple condition

    Keyword arguments:
    mock_loadClubs -- the mock for the loadClubs
    mock_loadCompetitions -- the mock for the loadCompetitions
    app_with_db -- the testDB containing the test app and our false data

    Return: passed if all assert pass, else it's will return failed
    """

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_competitions[0]['date'] = '2022-06-15 13:30:00'

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    for test_number in range(1, 5):
        if test_number == 1:  # test result if competition date is in the past
            response = flask_app.get(
                f'/book/{mock_competitions[0]['name']}/{mock_clubs[0]['name']}', follow_redirects=True)

            assert response.status_code == 200
            assert b'<title>Summary | GUDLFT Registration</title>' in response.data
            assert b'<li>Error, this competitions has already ended.</li>' in response.data

        if test_number == 2:  # test result if the competition date is still in the futur
            mock_competitions[0]['date'] = '2050-06-15 13:30:00'
            response = flask_app.get(
                f'/book/{mock_competitions[0]['name']}/{mock_clubs[0]['name']}', follow_redirects=True)

            assert response.status_code == 200
            assert b'<title>Booking for Test Competition || GUDLFT</title>' in response.data
            assert b'<li>This competitions is still available</li>' in response.data

        if test_number == 3:  # test result if competition is invalid
            response = flask_app.get(
                f'/book/"not existing"/{mock_clubs[0]['name']}', follow_redirects=True)

            assert response.status_code == 200
            assert b'<title>Summary | GUDLFT Registration</title>' in response.data
            assert b'<li>Something went wrong-please try again</li>' in response.data

        if test_number == 4:  # test result if club is invalid
            response = flask_app.get(
                f'/book/{mock_competitions[0]['name']}/"not existing"', follow_redirects=True)

            assert response.status_code == 200
            assert b'<title>Summary | GUDLFT Registration</title>' in response.data
            assert b'<li>Something went wrong-please try again</li>' in response.data
