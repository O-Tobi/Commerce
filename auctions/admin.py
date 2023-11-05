from django.contrib import admin
from .models import User, Listing, Category, Comment, Bid

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "description","category", "starting_bid", "image_url",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("bid", "user")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("writer", "get_listing", "user_comment")


# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
