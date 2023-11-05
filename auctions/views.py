from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Comment, Bid


def index(request):
    active_listing = Listing.objects.filter(active=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "all_listing": active_listing,
        "categories": all_categories
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


#The listing function takes the entry from the user and displays it on the index page
def listing(request):
    #Take the entries from the user (from the new_auction page)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('user_bid')
        image_url = request.POST.get('image_url')
        current_user = request.user
        category = request.POST.get('category')
        

        category = Category.objects.get(category_name=category)
        bid = Bid(
            bid=starting_bid,
            user=current_user
        )
        bid.save()
        #save the entry in the model
        new_listing = Listing(
            title = title,
            description = description,
            starting_bid = bid,
            image_url = image_url,
            owner = current_user,
            category = category
        )

        new_listing.save()
        #display all the active listings in the model 
        all_listing = Listing.objects.filter(active=True)

        return render(request, "auctions/index.html",{
            "all_listing" : all_listing
        })
    else:
        all_categories = Category.objects.all()
        return render(request, "auctions/new_auction.html",{
            "categories": all_categories
        })

#The about_listing function displays all information about the selected listing including comments and bids made by users 
def about_listing(request, listing_id):
    active_listing = Listing.objects.get(id=listing_id)
    listing_in_watchlist = request.user in active_listing.watchlist.all()
    all_comment = Comment.objects.filter(get_listing=active_listing)
    owner_bid = request.user.username == active_listing.owner.username
    
    return render(request, "auctions/about.html", {
        "all_listing" : active_listing,
        "listing_in_watchlist" : listing_in_watchlist,
        "all_comments": all_comment,
        "owner_bid" : owner_bid
    })



def about_category(request):
    if request.method == "POST":
        category_data = request.POST.get('category')
        category = Category.objects.get(category_name=category_data)
        active_listing = Listing.objects.filter(active=True, category=category)
        all_categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "all_listing": active_listing,
            "categories": all_categories
        })
        


def add_to_watchlist(request, listing_id):
    listing_data = Listing.objects.get(id=listing_id)
    current_user = request.user
    listing_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("about_listing", args=(listing_id, )))

def remove_from_watchlist(request, listing_id):
    listing_data = Listing.objects.get(id=listing_id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("about_listing", args=(listing_id, )))

def view_watchlist(request):
    current_user = request.user
    auction_list = current_user.user_watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "user_watchlist": auction_list 
    })


def new_comment(request, listing_id):
    current_user = request.user
    listing_data = Listing.objects.get(id=listing_id)
    message = request.POST.get('comment_texts')
    
    save_comment = Comment(
        writer = current_user,
        get_listing = listing_data,
        user_comment = message
    )

    save_comment.save()
    
    return HttpResponseRedirect(reverse("about_listing", args=(listing_id, )))


#i think the new auction form is not rendering what i saved in the form to the database. also, the database is not taking new entry if i should use the make a bid form
def new_bid(request, listing_id):
    bid_data = request.POST.get('user_bid')
    listing_data = Listing.objects.get(id=listing_id)
    listing_in_watchlist = request.user in listing_data.watchlist.all()
    all_comment = Comment.objects.filter(get_listing=listing_data)
    owner_bid = request.user.username == listing_data.owner.username
    print("fine 1")

    if int(bid_data) > int(listing_data.starting_bid.bid):
        update_bid = Bid(
            user=request.user, 
            bid=int(bid_data)
            )
        update_bid.save()
        print("fine 2")
        listing_data.starting_bid = update_bid
        listing_data.save()
        print("fine 3")
        return render(request, "auctions/about.html", {
            "all_listing": listing_data,
            "success": True,
            "message": "Successful",
            "listing_in_watchlist" : listing_in_watchlist,
            "all_comments": all_comment,
            "owner_bid" : owner_bid
        })

    else:
        return render(request, "auctions/about.html", {
            "all_listing": listing_data,
            "success": False,
            "message": "Bid Failed, Try again.",
            "listing_in_watchlist" : listing_in_watchlist,
            "all_comments": all_comment,
            "owner_bid" : owner_bid, 
        })

def close_auction(request, listing_id):
    listing_data = Listing.objects.get(id=listing_id)
    listing_data.active=False
    listing_data.save()
    print("fine 1")
    owner_bid = request.user.username == listing_data.owner.username
    print("fine 2")
    listing_in_watchlist = request.user in listing_data.watchlist.all()
    print("fine 3")
    all_comment = Comment.objects.filter(get_listing=listing_data)
    print("fine 4")

    return render(request, "auctions/about.html", {
        "all_listing" : listing_data,
        "listing_in_watchlist" : listing_in_watchlist,
        "all_comments": all_comment,
        "owner_bid" : owner_bid,
        "success": True,
        "message": "Congratulations on your auction."
    })


 