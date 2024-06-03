def test_logout(flask_app):
    response = flask_app.get(
        '/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'<title>GUDLFT Registration</title>' in response.data
