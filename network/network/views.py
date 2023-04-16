from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from .models import User, Post, Like, Follow
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from django.http import JsonResponse
from django.core.paginator import Paginator
import math
import json


def paginate(request, page: str, id: int = None):
    """ Pagination  """
    if page == 'index':
        posts = Post.objects.all().order_by('-time')
    elif page == 'followposts':
        posts = []
        # * Multiple IDs => Get id from every user the current user if following
        ids = [ID['user_id'] for ID in Follow.objects.filter(follower_id=id).values('user_id')]
        if len(ids):
            posts = []  
            for post in Post.objects.all().order_by('-time'):
                if post.user_id in ids:
                    posts.append(post)
    elif page == 'profile':
        posts = Post.objects.filter(user_id=id).order_by('-time')

    paginator = Paginator(posts, 10)
    
    pages = [i for i in range(1, math.ceil(len(posts)/10)+1)]
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return page_obj, pages


def index(request):
    """ 
        All Posts: The “All Posts” link in the navigation bar should take the user to a page where they can see all posts from all users, 
        with the most recent posts first.
        Each post should include 
            the username of the poster, 
            the post content itself, 
            the date and time at which the post was made, 
            and the number of “likes” the post has 
            (this will be 0 for all posts until you implement the ability to “like” a post later).
    """

    page_obj, pages = paginate(request, 'index')

    # If the user is not logged in, display all posts without the create new post form
    if not request.user.is_authenticated:
        return render(request, "network/index.html", {
            'posts': page_obj,
            'pages': pages,
        })

    user = User.objects.get(username=request.user.username)
    # Initial values: USER = current user(User instance)
    form = PostForm(request.POST or None, initial={'user': user})

    if request.method == 'POST':
        # If the form is valid, save it
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('index'))

    return render(request, "network/index.html", {
        'form': form,
        'posts': page_obj,
        'pages': pages,
    })


@login_required
def follow_posts(request, id: int):
    """  
        The “Following” link in the navigation bar should take the user to a page 
        where they see all posts made by users that the current user follows.

        This page should behave just as the “All Posts” page does, just with a more limited set of posts.
        This page should only be available to users who are signed in. 
    """
    user = User.objects.get(username=request.user.username)
    # Initial values: USER = current user(User instance)
    form = PostForm(request.POST or None, initial={'user': user})
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('follow_posts'), args=id)


    page_obj, pages = paginate(request, 'followposts', id=id)


    return render(request, "network/index.html", {
        'form': form,
        'posts': page_obj,
        'pages': pages,
    })

def profile_page(request, id: int):
    """ 
        Clicking on a username should load that user’s profile page. This page should:
        Display the number of followers the user has, as well as the number of people that the user follows.
        Display all of the posts for that user, in reverse chronological order.

        For any other user who is signed in, 
        this page should also display a “Follow” or “Unfollow” button that will let the current user toggle
        whether or not they are following this user’s posts.

        Note that this only applies to any “other” user: a user should not be able to follow themselves.
    """

    page_obj, pages = paginate(request, 'profile', id=id)
       
    if request.user.is_authenticated:
        followState = 'Follow' if not Follow.objects.filter(user_id=id, follower=request.user).exists() else 'Unfollow'
    else:
        followState = ''    

    return render(request, 'network/profile.html', {
        'posts': page_obj,
        'pages': pages,
        'profileUser': User.objects.get(id=id),
        'followState': followState,
    })


@login_required
@requires_csrf_token
def updateFollow(request, action: str, user_id: int,  follower_id: int):
    """ 
        Follow or Unfollow user,
        Like or unlike post

        If action = Like then follower_id ==  post_id
    """
    # Return status code indicating bad request
    if request.method != 'POST' and request.method != 'DELETE':
        return JsonResponse({'error': 'Invalid request, only DELETE and POST supported.'}, status=400)
    
    
    if action == 'follow':
        if request.method == 'DELETE':
            follow = Follow.objects.filter(
                user_id=user_id, follower_id=follower_id)
            follow.delete()
            message = 'User unfollowed'
            status = 200
        elif request.method == 'POST':
            follower = User.objects.get(id=follower_id)
            user = User.objects.get(id=user_id)
            if not Follow.objects.filter(user_id=user_id, follower_id=follower_id).exists():
                Follow.create(user, follower)
                message = 'Success'
                status = 201
            else:
                message = f"{follower.username} already follows {user.username}"
                status = 202

        # Get updated number of the followers
        followers = Follow.objects.filter(user_id=user_id).count()

        return JsonResponse({
            'message': message,
            'followers': followers,
        }, status=status)

    elif action == 'like':
        #  If action = Like then follower_id ==  post_id
        if request.method == 'DELETE':
            like = Like.objects.filter(user_id=user_id, post_id=follower_id)
            like.delete()
            message = 'Like removed'
            status = 200
        elif request.method == 'POST':
            post = Post.objects.get(id=follower_id)
            user = User.objects.get(id=user_id)
            if not Like.objects.filter(user_id=user_id, post_id=follower_id).exists():
                Like.create(user, post)
                message = 'Success'
                status = 201
            else:
                message = f"{user.username} has already liked this post"
                status = 202

        # Get the number of likes
        likes = Like.objects.filter(post_id=follower_id).count()

        return JsonResponse({
            'message': message,
            'likes': likes,
        }, status=status)

    


@login_required
@requires_csrf_token
def edit(request, action: str, id: int):
    """ 
        Edit post if user.UUID == post.user.UUID
        @param id => post_id 

        ID can be used as well, but UUID is more secure,
        given that the ID is just the sequence of numbers,
        and the UUID is 36-character alphanumeric string regardless of the user's ID
        
        Methods:
        POST
        
        actions: 
        get post
        save modified post
    """
 
    # Return status code indicating bad request
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method, only POST supported.'}, status=400)


    if action == 'edit':
        post = Post.objects.get(id=id)
        return JsonResponse({'content': post.content.encode("utf8").decode("unicode-escape")}, status=200, safe=False)
    else:
        content = str(request.body, 'utf8')
        mod_post = Post.objects.get(id=id)
        mod_post.content = content[1:-1]
        post = mod_post.content
        mod_post.save() 
        
        return JsonResponse({'content': post}, status=202, safe=False)

    



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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

