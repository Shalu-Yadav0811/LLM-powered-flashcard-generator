def test_create_deck(client, auth_headers):
    response = client.post('/api/decks', json={
        'title': 'Test Deck',
        'description': 'A test deck',
        'subject': 'Science',
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['deck']['title'] == 'Test Deck'


def test_list_decks(client, auth_headers):
    client.post('/api/decks', json={'title': 'Deck 1'}, headers=auth_headers)
    client.post('/api/decks', json={'title': 'Deck 2'}, headers=auth_headers)

    response = client.get('/api/decks', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['decks']) == 2


def test_get_deck_with_cards(client, auth_headers):
    # Create deck
    resp = client.post('/api/decks', json={'title': 'My Deck'}, headers=auth_headers)
    deck_id = resp.get_json()['deck']['id']

    # Add a card
    client.post(f'/api/decks/{deck_id}/cards', json={
        'question': 'What is Python?',
        'answer': 'A programming language',
        'difficulty': 'Easy',
        'topic': 'Programming',
    }, headers=auth_headers)

    # Get deck
    response = client.get(f'/api/decks/{deck_id}', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['deck']['flashcards']) == 1
    assert data['deck']['flashcards'][0]['question'] == 'What is Python?'


def test_update_card(client, auth_headers):
    # Create deck and card
    resp = client.post('/api/decks', json={'title': 'Edit Deck'}, headers=auth_headers)
    deck_id = resp.get_json()['deck']['id']

    resp = client.post(f'/api/decks/{deck_id}/cards', json={
        'question': 'Old question',
        'answer': 'Old answer',
    }, headers=auth_headers)
    card_id = resp.get_json()['flashcard']['id']

    # Update card
    response = client.put(f'/api/cards/{card_id}', json={
        'question': 'New question',
        'answer': 'New answer',
        'difficulty': 'Hard',
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['flashcard']['question'] == 'New question'
    assert data['flashcard']['difficulty'] == 'Hard'


def test_delete_deck(client, auth_headers):
    resp = client.post('/api/decks', json={'title': 'Delete Me'}, headers=auth_headers)
    deck_id = resp.get_json()['deck']['id']

    response = client.delete(f'/api/decks/{deck_id}', headers=auth_headers)
    assert response.status_code == 200

    response = client.get(f'/api/decks/{deck_id}', headers=auth_headers)
    assert response.status_code == 404
