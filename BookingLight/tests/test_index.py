def test_index(flask_app):
    response = flask_app.get(
        '/', follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>GUDLFT Registration</title>' in response.data
