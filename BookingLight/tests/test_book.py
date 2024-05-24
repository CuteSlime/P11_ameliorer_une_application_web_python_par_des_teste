from unittest.mock import patch


@patch('BookingLight.views.loadCompetitions')
@patch('BookingLight.views.loadClubs')
def test_book(mock_loadClubs, mock_loadCompetitions, app_with_db):

    flask_app, mock_competitions, mock_clubs = app_with_db

    mock_competitions[0]['date'] = '2022-06-15 13:30:00'

    mock_loadClubs.return_value = mock_clubs
    mock_loadCompetitions.return_value = mock_competitions

    for test_number in range(1, 3):
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
