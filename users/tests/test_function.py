import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_user_registration(client):
    url=reverse('user-register')
    data = {
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "SecurePassword123!",
        "role": "buyer",
        "nationality": "American"
    }
    
    response=client.post(url,data,format='json')
    
    assert response.status_code== status.HTTP_201_CREATED
    
    assert response.data['username']=='testuser'
    assert response.data['email']== 'testuser@example.com'
    
    assert 'password' not in response.data
    
@pytest.mark.django_db
def test_user_login(client,create_user):
    url=reverse('user-login')
    
    create_user(email='testuser@example.com',password='SecurePassword123!')
    
    data={
        "email":"testuser@example.com",
        "password":"securePassword124!"
    }
    
    response=client.post(url,data,format='json')
    
    assert response.status_code== status.HTTP_200_OK
    
    assert response.data['email']=='testuser@example.com'
    
    
    
    