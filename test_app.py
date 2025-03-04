import pytest
from app import app, db, User

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_users(client):
    user = User(username="testuser")
    db.session.add(user)
    db.session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    assert "testuser" in response.get_data(as_text=True)

def test_external_api(client):
    response = client.get('/external-api')
    assert response.status_code == 200
    assert len(response.json()) > 0
