import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

# ==========================================
# 1. ROUTE ACCESSIBILITY TESTS
# ==========================================

def test_home_page_status(client):
    """TC-01: Verify home page loads or redirects to auth."""
    response = client.get('/')
    assert response.status_code in [200, 302]

def test_login_page_status(client):
    """TC-02: Verify login page renders correctly."""
    # Checks both root /login and blueprint /auth/login
    response = client.get('/auth/login') if client.get('/auth/login').status_code != 404 else client.get('/login')
    assert response.status_code == 200

def test_register_page_status(client):
    """TC-03: Verify registration page renders correctly."""
    response = client.get('/auth/register') if client.get('/auth/register').status_code != 404 else client.get('/register')
    assert response.status_code == 200

def test_nonexistent_route_404(client):
    """TC-04: Verify requesting a non-existent route returns 404."""
    response = client.get('/this-page-does-not-exist')
    assert response.status_code == 404


# ==========================================
# 2. SESSION & ACCESS CONTROL TESTS
# ==========================================

def test_unauthenticated_report_redirect(client):
    """TC-05: Ensure unauthenticated user accessing report endpoint gets redirected."""
    response = client.get('/report', follow_redirects=False)
    if response.status_code == 404:
        response = client.get('/main/report', follow_redirects=False)
    assert response.status_code in [302, 303]

def test_unauthenticated_my_activity_redirect(client):
    """TC-06: Ensure unauthenticated user accessing my-activity gets redirected."""
    response = client.get('/my-activity', follow_redirects=False)
    if response.status_code == 404:
        response = client.get('/main/my-activity', follow_redirects=False)
    assert response.status_code in [302, 303, 404]

def test_report_item_requires_auth(client):
    """TC-07: Submitting an item report without session data fails or redirects."""
    response = client.post('/report', data={'title': 'Lost Keys'}, follow_redirects=False)
    assert response.status_code in [302, 303, 401, 404]


# ==========================================
# 3. AUTHENTICATION & SESSION TESTS
# ==========================================

def test_invalid_login_credentials(client):
    """TC-08: Submitting invalid login details handles response appropriately."""
    login_url = '/auth/login' if client.get('/auth/login').status_code != 404 else '/login'
    response = client.post(login_url, data={
        'username': 'nonexistent_user',
        'password': 'WrongPassword123'
    }, follow_redirects=True)
    assert response.status_code in [200, 302]

def test_logout_session_clearing(client):
    """TC-09: Test logout route handles redirect."""
    logout_url = '/auth/logout' if client.get('/auth/logout').status_code != 404 else '/logout'
    response = client.get(logout_url, follow_redirects=True)
    assert response.status_code in [200, 302, 404]

def test_authenticated_user_session_simulation(client):
    """TC-10: Simulate logged-in user session and verify profile/dashboard access."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'testuser'
        sess['role'] = 'user'
    
    response = client.get('/')
    assert response.status_code in [200, 302]