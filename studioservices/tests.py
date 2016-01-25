from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

def create_user(t, userpass):
    url = reverse('api-register-list')
    data = {'username': userpass, 'password':userpass, 'password2':userpass}
    response = t.client.post(url, data, format='json')
    return response

class RegisterTests(APITestCase):
    def test_create_account(self):
        url = reverse('api-register-list')
        data = {'username': 'test1', 'password':'test1', 'password2':'test1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_existing_account(self):
        url = reverse('api-register-list')
        data = {'username': 'test2', 'password':'test2', 'password2':'test2'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bad_password(self):
        url = reverse('api-register-list')
        data = {'username': 'test1', 'password':'test1', 'password2':'test2'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #def test_register_logged_user(self):

class LoginTest(APITestCase):
    def test_good_login(self):
        create_user(self, 'test_login1')
        self.client.logout()
        url = reverse('api-login-list')
        data = {'username': 'test_login1', 'password':'test_login1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bad_login(self):
        create_user(self, 'test_login2')
        self.client.logout()
        url = reverse('api-login-list')
        data = {'username': 'test_login2', 'password':'test_wrong'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UsersTest(APITestCase):
    #                mixins.RetrieveModelMixin,
    #               mixins.UpdateModelMixin,
    #               mixins.DestroyModelMixin,
    #               mixins.ListModelMixin)
    #               try create also
    pass


