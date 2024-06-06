def test_index(flask_app):
    """test if the index route redirect to the good page with the good code

    Keyword arguments:
    flask_app -- the test app

    Return: passed if all assert pass, else it's will return failed
    """

    response = flask_app.get(
        '/', follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>GUDLFT Registration</title>' in response.data
