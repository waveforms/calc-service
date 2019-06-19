import os
import tempfile

import pytest

import components


@pytest.fixture
def client():
    components.common.app.config['SQLALCHEMY_DATABASE_URI'] = components.common.app.config['SQLALCHEMY_DATABASE_URI_TEST']
    components.common.app.config['TESTING'] = True
    client = components.common.app.test_client()

    with components.common.app.app_context():
        components.common.db.create_all()

    yield client

    
    
def test_top_level(client):
    """Start with anon user"""
    rv = client.get('/')
    assert b'Redirecting' in rv.data
    
def test_index(client):
    rv = client.get('/index')
    assert b'Redirecting' in rv.data
    
def test_login(client):
    rv = client.get('/login')
    assert b'Sign In - CalcService' in rv.data

def test_logout(client):
    rv = client.get('/logout')
    assert b'Redirecting' in rv.data
    
def test_register(client):
    rv = client.get('/register')
    assert b'Register - CalcService' in rv.data