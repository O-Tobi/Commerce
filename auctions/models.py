from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category_name}"

class Bid(models.Model):
    bid = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_bid")

    def __str__(self):
        return f"{self.bid}"
 
class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    active = models.BooleanField(default=True)
    starting_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, blank=True, related_name="user_bidding")
    image_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, related_name="user_watchlist")

    def __str__(self):
        return f"Title: {self.title}, Description: {self.description}, Active: {self.active}, Starting Bid: {self.starting_bid}, Image URL: {self.image_url}, Owner: {self.owner}, Category: {self.category}"

#The Comment model saves all the comments made by the user
class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    get_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment")
    user_comment = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.writer} comment on{self.get_listing}"

