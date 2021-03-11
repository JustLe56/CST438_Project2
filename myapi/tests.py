from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from .models import WishListUser
from .serializers import WishListUserSerializer


class WishListUserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.test_credentials = {'username': 'James', 'password': 'h37f!3ld'}
        self.serializer = WishListUserSerializer()

    def test_create_user(self):
        response = self.client.post('/api/createAccount/', self.test_credentials)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishListUser.objects.count(), 1)
        self.assertEqual(WishListUser.objects.get().username, self.test_credentials['username'])

    def test_create_user_disallowed_methods(self):
        disallowed_methods = [
            self.client.get,
            self.client.head,
            self.client.put,
            self.client.delete,
            self.client.trace
        ]
        for method in disallowed_methods:
            response = method('/api/createAccount/')
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
