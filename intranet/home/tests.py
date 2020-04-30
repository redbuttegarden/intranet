import pytest

from pytest_django.asserts import assertContains, assertNotContains


@pytest.mark.django_db
def test_search_view_summary(client):
    # Search based on summary should return two posts
    response = client.get('/search/', {'query': 'normal'})
    assert response.status_code == 200
    assertContains(response, 'One')
    assertContains(response, 'Two')


@pytest.mark.django_db
def test_search_view_body(client):
    # Search based on body should return just the one post
    response = client.get('/search/', {'query': 'Unrelated'})
    assert response.status_code == 200
    assertContains(response, 'Two')
    assertNotContains(response, 'One')


@pytest.mark.django_db
def test_search_view_staff(client, admin_client):
    """
    Test to ensure private posts aren't visible to users who aren't in staff group
    """
    # Only Public Post should be visible to client even when authenticated
    unauthenticated_response = client.get('/search/', {'query': 'summary text'})
    assert unauthenticated_response.status_code == 200
    assertContains(unauthenticated_response, 'Public Post')
    assertNotContains(unauthenticated_response, 'Private Post')

    client.login(username='user', password='pass')
    authenticated_response = client.get('/search/', {'query': 'summary text'})
    assert authenticated_response.status_code == 200
    assertContains(authenticated_response, 'Public Post')
    assertNotContains(authenticated_response, 'Private Post')

    # Public AND Private Post should be visible to admin which is in staff group
    # admin_client is already considered logged in
    authenticated_response = admin_client.get('/search/', {'query': 'summary text'})
    assert authenticated_response.status_code == 200
    assertContains(authenticated_response, 'Public Post')
    assertContains(authenticated_response, 'Private Post')
