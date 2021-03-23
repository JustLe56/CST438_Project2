from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from .models import WishListUser, Wishlist, Link, WishlistItem
from .serializers import WishListUserSerializer, WishlistItemSerializer
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
        self.user_credentials = {'username': 'Kirk', 'password': 'w4hw4h'}
        self.user = WishListUserSerializer().create(self.user_credentials.copy())
        self.wishlist = Wishlist.objects.get(wishlistUser=self.user)
        self.wishlist.save()
        self.link = Link(url='https://lazerhawk.bandcamp.com/merch/2x-lazerhawk-logo-t-shirt-sale')
        self.link.save()
        self.serializer = WishlistItemSerializer()
        base_item_properties = {
            'name': 'Lazerhawk T-Shirt',
            'description': 'An awesome T-Shirt.',
            'image_url': 'https://f4.bcbits.com/img/0003534389_10.jpg',
            'priority': 10,
            'index': 0
        }
        self.item_properties = base_item_properties.copy()
        self.item_properties.update({'wishlist': self.wishlist, 'link': self.link})
        self.serialized_item = base_item_properties.copy()
        self.serialized_item.update({'wishlist': self.wishlist.id, 'link_url': self.link.url})
        self.client.login(**self.user_credentials)

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

    def test_create_wishlist_item(self):
        self.serialized_item.pop('wishlist')
        response = self.client.post('/api/item/', self.serialized_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WishlistItem.objects.count(), 1)
        self.assertEqual(WishlistItem.objects.get().name, self.item_properties['name'])

    def test_retrieve(self):
        WishlistItem.objects.create(**self.item_properties)
        response = self.client.get(f'/api/item/{self.item_properties["index"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_duplicate_indexes(self):
        WishlistItem.objects.create(**self.item_properties)
        # create second user (and thus a second wishlist)
        user2 = WishListUserSerializer().create({'username': 'James', 'password': 'Seattle89'})
        self.item_properties['wishlist'] = Wishlist.objects.get(wishlistUser=user2)
        # create second item w/same index
        WishlistItem.objects.create(**self.item_properties)
        # retrieve first item
        response = self.client.get(f'/api/item/{self.item_properties["index"]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        item = WishlistItem.objects.create(**self.item_properties)
        self.serialized_item.update({'image_url': 'https://f4.bcbits.com/img/0003534387_10.jpg', 'priority': 5})
        response = self.client.put(f'/api/item/{self.item_properties["index"]}', self.serialized_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reserialized = WishlistItemSerializer(instance=WishlistItem.objects.get(id=item.id)).data
        self.assertEqual(reserialized, self.serialized_item)

    def test_destroy(self):
        WishlistItem.objects.create(**self.item_properties)
        self.item_properties['index'] += 1
        WishlistItem.objects.create(**self.item_properties)
        response1 = self.client.delete(f'/api/item/{self.item_properties["index"] - 1}')
        response2 = self.client.get(f'/api/item/{self.item_properties["index"] - 1}')
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_list_wishlist_items(self):
        item1 = WishlistItem.objects.create(**self.item_properties)
        self.item_properties['index'] += 1
        item2 = WishlistItem.objects.create(**self.item_properties)
        response = self.client.get('/api/listitems/')
        correct_response = [WishlistItemSerializer(instance=item).data for item in (item1, item2)]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_loads(response.content), correct_response)

    def test_update_index(self):
        WishlistItem.objects.create(**self.item_properties)
        self.item_properties['index'] += 1
        WishlistItem.objects.create(**self.item_properties)
        updated_serialized_item = self.serialized_item.copy()
        updated_serialized_item['index'] += 1
        response = self.client.put(f'/api/item/{self.serialized_item["index"]}', updated_serialized_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
