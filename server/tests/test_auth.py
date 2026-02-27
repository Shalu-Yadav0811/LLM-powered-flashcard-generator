def test_register(client, db):
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['user']['username'] == 'newuser'
    assert 'access_token' in data
    assert 'refresh_token' in data


def test_register_duplicate_email(client, db):
    client.post('/api/auth/register', json={
        'username': 'user1',
        'email': 'dup@example.com',
        'password': 'password123',
    })
    response = client.post('/api/auth/register', json={
        'username': 'user2',
        'email': 'dup@example.com',
        'password': 'password123',
    })
    assert response.status_code == 409


def test_login(client, db):
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'password123',
    })
    response = client.post('/api/auth/login', json={
        'email': 'login@example.com',
        'password': 'password123',
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data


def test_login_wrong_password(client, db):
    client.post('/api/auth/register', json={
        'username': 'wrongpass',
        'email': 'wrong@example.com',
        'password': 'password123',
    })
    response = client.post('/api/auth/login', json={
        'email': 'wrong@example.com',
        'password': 'wrongpassword',
    })
    assert response.status_code == 401


def test_get_profile(client, auth_headers):
    response = client.get('/api/auth/me', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['username'] == 'testuser'


def test_protected_route_no_token(client, db):
    response = client.get('/api/auth/me')
    assert response.status_code == 401
