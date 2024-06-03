import json
from unittest.mock import patch, mock_open
from BookingLight.models import loadClubs, loadCompetitions, writeClubs, writeCompetitions


def test_loadClubs(app_with_db):
    _, _, mock_clubs = app_with_db
    with patch('BookingLight.models.open',
               mock_open(read_data=json.dumps({'clubs': mock_clubs})),
               create=True
               ):
        clubs = loadClubs()
        assert clubs == mock_clubs


def test_loadCompetitions(app_with_db):
    _, mock_competitions, _ = app_with_db
    with patch('BookingLight.models.open',
               mock_open(read_data=json.dumps(
                   {'competitions': mock_competitions})),
               create=True
               ):
        competitions = loadCompetitions()
        assert competitions == mock_competitions


def test_writeClubs(app_with_db):
    _, _, mock_clubs = app_with_db
    expected_json_dump = json.dumps(
        {'clubs': mock_clubs}, indent=4)
    mock_file = mock_open()
    with patch('BookingLight.models.open', mock_file, create=True):
        writeClubs(mock_clubs)
        handle = mock_file()
        written_data = ''.join(call.args[0]
                               for call in handle.write.call_args_list)
        assert written_data == expected_json_dump


def test_writeCompetitions(app_with_db):
    _, mock_competitions, _ = app_with_db
    expected_json_dump = json.dumps(
        {'competitions': mock_competitions}, indent=4)
    mock_file = mock_open()
    with patch('BookingLight.models.open', mock_file, create=True):
        writeCompetitions(mock_competitions)
        handle = mock_file()
        written_data = ''.join(call.args[0]
                               for call in handle.write.call_args_list)
        assert written_data == expected_json_dump
