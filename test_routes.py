from flask_login import LoginManager, login_user
import pytest
from application import create_app, db
from application.database.users import User
from flask import Flask 

app = Flask(__name__)
login_manager = LoginManager(app)

@pytest.fixture
def form_test():
    return {
        'Neighborhood': 'OldTown',
        'Overall_Cond': 5,
        'Overall_Qual': 6,
        'Kitchen_Qual': "Ex",
        'Exter_Qual': "Ex",
        'Garage_Cars': 2,
        'Misc_Val': 4000,
        'MS_SubClass': "1-STORY 1946 & NEWER ALL STYLES",
        'surface_total': 1500,
        'BsmtFin_SF_first': 200
    }
    
@pytest.fixture
def app():
    return create_app(test=True)

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()
        
def test_home(client):
    response = client.get('/')
    print(response.data)
    assert response.status_code == 200
    assert "Welcome" in str(response.data)
    
def test_auth(client):
    @login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(email='ayoub1@gmail.com').first()

    response = client.post('/login', json={'email': 'ayoub1@gmail.com', 'password': '1234'}, follow_redirects=True)
    assert response.status_code == 200
    
def test_add_user(client):
    user_data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john@example.com',
        'password': '1234',
    }
    @login_manager.request_loader
    def load_user_from_request(request):
        user = User.query.filter_by(email=user_data['email']).first()
        return user 
    response = client.post('/add_user', data=user_data, follow_redirects=True)
    print(response.__dict__)
    assert response.status_code == 200
    user = User.query.filter_by(email=user_data['email']).first()
    assert user is not None
    assert user.firstname == user_data['firstname']

def test_login( client):
    response = client.get('/login')
    assert response.status_code == 200    
    @login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(email=user_data['email']).first()
    user_data = {
        'email': 'john@example.com',
        'password': '1234',
    }
    response = client.post('/login', data=user_data, follow_redirects=True)
    print(response.__dict__)
    print(response.data)
    print(response.status_code)
    assert response.status_code == 200 
    
    

def test_index(client):
    response = client.get('/prediction/', follow_redirects=True)
    assert response.status_code == 200
    assert "Prediction" in str(response.data)
    
# def test_prediction(form_test: dict, client):
#     response = client.post('/prediction/predict', data=form_test, follow_redirects=True)
#     print(response.__dict__)
#     print(response.data)
#     assert response.status_code == 200

def test_predict_route_with_authenticated_user(client, form_test: dict):
    
    # Créer un utilisateur de test
    user_data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john@example.com',
        'password': '1234',
    }
    user = User(firstname=user_data['firstname'],lastname=user_data['lastname'], email=user_data['email'], password_hash=user_data['password']).save_to_db()
    @login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(email=user_data['email']).first()
    # Simuler l'authentification de l'utilisateur
    # Effectuer la requête sur la route protégée
    response = client.get('/prediction/predict', data=form_test, follow_redirects=True)
    assert response.status_code == 200
    assert 'Prediction' in str(response.data)
        
        
        
# import pytest
# from flask import Flask
# from flask_login import current_user
# from application import create_app, db
# from application.database.users import User

# @pytest.fixture(scope='module')
# def test_client():
#     flask_app = create_app()
#     testing_client = flask_app.test_client()

#     # Set up the testing environment
#     with flask_app.app_context():
#         db.create_all()
#         User.query.delete()
#         User(firstname='Test', lastname='User', email='test@example.com', password_hash='testpassword').save_to_db()

#     yield testing_client

#     # Clean up the testing environment
#     with flask_app.app_context():
#         db.drop_all()

# def test_login(test_client):
#     response = test_client.get('/login', follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Login' in response.data

#     response = test_client.post('/login', data={'email': 'test@example.com', 'password': 'testpassword'}, follow_redirects=True)
#     assert response.status_code == 200
#     assert response.request.url == 'http://localhost/login'

#     # Ensure the user is logged in
#     with test_client.session_transaction() as session:
#         assert session['_user_id'] == 1
#         assert current_user.is_authenticated

# def test_add_user(test_client):
#     response = test_client.get('/add_user')
#     assert response.status_code == 200
#     assert b'Nouvel utilisateur' in response.data

#     response = test_client.post('/add_user', data={'firstname': 'John', 'lastname': 'Doe', 'email': 'john@example.com', 'password_hash': 'password', 'password_hash2': 'password'}, follow_redirects=True)
#     assert response.status_code == 200
#     print('----------------------------------------------------------------')
#     print(response.data)
#     assert response.request.url == 'http://localhost/add_user'

#     # Check if the user was added to the database
#     with test_client.session_transaction() as session:
#         user = User.query.filter_by(email='john@example.com').first()
#         assert user is not None
#         assert user.firstname == 'John'
#         assert user.lastname == 'Doe'
#         assert user.email == 'john@example.com'
#         assert user.password_hash != 'password'

# def test_predict(test_client):
#     # Login as the test user
#     response = test_client.post('/login', data={'email': 'test@example.com', 'password': 'testpassword'}, follow_redirects=True)
#     assert response.status_code == 200
#     assert response.request.url == 'http://localhost/login'

#     # Access the prediction route
#     response = test_client.get('/prediction', follow_redirects=True)
#     assert response.status_code == 200
#     print('----------------------------------------------------------------')
#     print('----------------------------------------------------------------')
#     assert response.request.url == 'http://localhost/prediction/'

#     # Submit the prediction form
#     response = test_client.post('/prediction/predict', data={
#         'Neighborhood': 'NAmes',
#         'Overall_Cond': 5,
#         'Overall_Qual': 5,
#         'Kitchen_Qual': 'TA',
#         'Exter_Qual': 'TA',
#         'Garage_Cars': 0,
#         'BsmtFin_SF_first': 0,
#         'Misc_Val': 0,
#         'MS_SubClass': '1-STORY 1946 & NEWER ALL STYLES',
#         'surface_total': 150,
#         'submit': True
#     }, follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Prediction Result' in response.data
#     assert b'$' in response.data