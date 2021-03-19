from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from .models import WishListUser, Wishlist, Link, WishlistItem
from .serializers import WishListUserSerializer
from json import loads as json_loads
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db.models import Model


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

    def test_login(self):
        WishListUserSerializer().create(self.test_credentials.copy())
        response = self.client.post('/api/login/', self.test_credentials, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_loads(response.content), {'detail': 'Success'})

    def test_login_fail(self):
        test_incorrect_credentials = {'username': 'wrong', 'password': 'incorrect'}
        response = self.client.post('/api/login/', test_incorrect_credentials, format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_loads(response.content), {'detail': 'Invalid credentials'})

    def test_logout(self):
        WishListUserSerializer().create(self.test_credentials.copy())
        self.client.login(**self.test_credentials)
        response = self.client.post('/api/logout/', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_loads(response.content), {'detail': 'Success'})

    def test_logout_fail(self):
        WishListUserSerializer().create(self.test_credentials.copy())
        response = self.client.post('/api/logout/', format='json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json_loads(response.content), {'detail': 'Not logged in'})

    def test_create_personal_wishlist(self):
        user = WishListUserSerializer().create(self.test_credentials.copy())
        try:
            Wishlist.objects.get(wishlistUser=user)
        except Model.DoesNotExist as e:
            self.fail(e.message)


class WishlistTests(APITestCase):

    def setUp(self):
        self.user = WishListUserSerializer().create({'username': 'Lars', 'password': 'n4p573r5uk5'})
        self.wishlist_properties = {'wishlistUser': self.user}

    def test_create_wishlist_instance(self):
        wishlist = Wishlist(**self.wishlist_properties)
        try:
            wishlist.save()
        except ValidationError as e:
            self.fail(e.message)


class LinkTests(APITestCase):

    def setUp(self):
        self.link_properties = {
            'url': 'https://www.bkstr.com/csumontereybaystore/product/clothing-accessories/men/t-shirts-tanks-men/calif'
                   'ornia-state-university-monterey-bay-short-sleeve-t-shirt-213389-1'
        }

    def test_create_link_instance(self):
        link = Link(**self.link_properties)
        try:
            link.save()
        except ValidationError as e:
            self.fail(e.message)

    def test_link_url_unique(self):
        link = Link(**self.link_properties)
        link.save()
        duplicate = Link(**self.link_properties)
        self.assertRaises(IntegrityError, duplicate.save)


class WishlistItemTests(APITestCase):

    def setUp(self):
        self.user = WishListUserSerializer().create({'username': 'Kirk', 'password': 'w4hw4h'})
        self.wishlist = Wishlist(wishlistUser=self.user)
        self.wishlist.save()
        self.link = Link(url='https://lazerhawk.bandcamp.com/merch/2x-lazerhawk-logo-t-shirt-sale')
        self.link.save()
        self.item_properties = {
            'wishlist': self.wishlist,
            'link': self.link,
            'name': 'Lazerhawk T-Shirt',
            'description': 'An awesome T-Shirt.',
            'image_url': 'https://f4.bcbits.com/img/0003534389_10.jpg',
            'priority': 10,
            'index': 0
        }

    def test_create_wishlist_item_instance(self):
        item = WishlistItem(**self.item_properties)
        try:
            item.save()
        except ValidationError as e:
            self.fail(e.message)

    def test_wishlist_and_index_unique(self):
        item = WishlistItem(**self.item_properties)
        item.save()
        item_duplicate_index = WishlistItem(**self.item_properties)
        item_duplicate_index.name = 'Lazerhawk T-Shirt 2'
        self.assertRaises(IntegrityError, item_duplicate_index.save)
