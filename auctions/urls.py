from django.urls import path
#from django.conf import settings
#from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing, name="listing"),
    path("about_category", views.about_category, name="about_category"),
    path("about_listing/<int:listing_id>", views.about_listing, name="about_listing"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("view_watchlist", views.view_watchlist, name="view_watchlist"),
    path("new_comment/<int:listing_id>", views.new_comment, name="new_comment"),
    path("new_bid/<int:listing_id>", views.new_bid, name="new_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction")
   
]
