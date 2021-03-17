from django.contrib.auth.models import AbstractUser
from django.db import models


class WishListUser(AbstractUser):

	def __str__(self):
		return self.username


class Wishlist(models.Model):
	wishlistUser = models.ForeignKey(WishListUser, on_delete=models.CASCADE)


class Link(models.Model):
	url = models.URLField(unique=True)


class WishlistItem(models.Model):
	wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
	link = models.ForeignKey(Link, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	description = models.CharField(blank=True, max_length=1000)
	image_url = models.URLField(blank=True)
	priority = models.PositiveSmallIntegerField()
	index = models.PositiveSmallIntegerField()

	class Meta:
		unique_together = ['wishlist', 'index']
