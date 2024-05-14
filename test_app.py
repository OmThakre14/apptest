import pytest
from app import app as flask_app, todos

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(app, client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_todo(client):
    initial_todo_count = len(todos)
    response = client.post('/add', data={'todo': 'Test Todo'}, follow_redirects=True)
    assert response.status_code == 200
    assert len(todos) == initial_todo_count + 1
    assert 'Test Todo' in todos.values()

def test_delete_todo(client):
    # First, add a todo item
    initial_todo_count = len(todos)
    response = client.post('/add', data={'todo': 'Delete Me'}, follow_redirects=True)
    assert response.status_code == 200
    assert len(todos) == initial_todo_count + 1

    # Get the ID of the added todo item dynamically
    todo_id = next(iter(todos))
    response = client.get('/delete/{}'.format(todo_id), follow_redirects=True)
    assert response.status_code == 200
    assert todo_id not in todos
