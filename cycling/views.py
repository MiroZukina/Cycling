from django.shortcuts import get_object_or_404, render, redirect
import requests
from .models import Profile, Post, Comment, City
from django.contrib import messages
from django import forms
from .forms import PostForm, CommentForm, CityForm, SignUpForm, ProfilePicForm
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your Post Has Been Posted")
            return redirect('home')
    else:
        form = PostForm()

    posts = Post.objects.all().order_by("-created_at")
    comments = Comment.objects.all().order_by("-created_at")
    comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = posts[0]  # Set the post field (you need to adjust this)
            new_comment.save()
            messages.success(request, "Your Comment Has Been Posted")
            return redirect('home')

    return render(request, 'home.html', {"posts": posts, "form": form, "comments": comments, "comment_form": comment_form})




def profile_list(request):
    if request.user.is_authenticated:
       profiles = Profile.objects.exclude(user=request.user)
       return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request,("You Must Be Logged In To Viwe This Page...") )
        return redirect('home')
    

    

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        posts = Post.objects.filter(user_id=pk).order_by("-created_at")
        comment_form = CommentForm()

        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST.get('follow')

            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()

            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = request.user
                new_comment.post = posts[0]  
                new_comment.save()
                messages.success(request, "Your Comment Has Been Posted")
                return redirect('profile', pk=pk)

        return render(request, "profile.html", {"profile": profile, "posts": posts, "comment_form": comment_form})
    else:
        messages.success(request, "You Must Be Logged In To View This Page...")
        return redirect('home')
    
    

    
def unfollow(request, pk):
    if request.user.is_authenticated:
        #get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        #Unfollow the user
        request.user.profile.follows.remove(profile)
        #save our profile
        request.user.profile.save()
        messages.success(request,(f"You Have Successfully Unfollowd {profile.user.username}") )
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request,("You Must Be Logged In To Viwe This Page...") )
        return redirect('home')
    

def follow(request, pk):
    if request.user.is_authenticated:
        #get the profile to follow
        profile = Profile.objects.get(user_id=pk)
        #follow the user
        request.user.profile.follows.add(profile)
        #save our profile
        request.user.profile.save()
        messages.success(request,(f"You Have Successfully Followd {profile.user.username}") )
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request,("You Must Be Logged In To Viwe This Page...") )
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST["password"]
        user= authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You Have Been Logged In On This Page...") )
            return redirect('home')
        else:
            messages.success(request,("There was an error logging in. Please Try Again...") )
            return redirect('login')

    else:
        return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request,("You Have Been Logged Out...") )
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
           form.save()
           username = form.cleaned_data['username']
           password = form.cleaned_data['password1']
           user = authenticate(username=username, password=password )
           login(request, user)
           messages.success(request,("You Have Been successfully registred! Welcom!") )
           return redirect('home')
        

    return render(request, "register.html", {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user_id=request.user.id)
        user_form = SignUpForm(request.POST or  None, request.FILES or None, instance=current_user ) 
        profile_form = ProfilePicForm(request.POST or  None, request.FILES or None, instance=profile_user ) 
        user_form.fields['username'].required = False

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, f'Your Profile Has Been Updated!')
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form,'profile_form':profile_form})
    else:
        messages.success(request, f'You Must Be logged In To View That Page...')
        return redirect('home')




    

def post_like(request, pk):
    if request.user.is_authenticated:
       post = get_object_or_404(Post, id=pk)
       if post.likes.filter(id=request.user.id):
          post.likes.remove(request.user)
       else:
          post.likes.add(request.user)

       
       return redirect(request.META.get("HTTP_REFERER"))


    else:
       messages.success(request, f'You Must Be logged In To View That Page...')
       return redirect('home')
    
def post_show(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post:
       return render(request, "post_show.html", {'post': post})

    else:
       messages.success(request, f'That Post Does Not Exist')
       return redirect('home')
    
def delete_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        #chacke to see if you own the post
        if request.user.username == post.user.username:
             #delete post
             post.delete()
             messages.success(request, "THe Post Has Been Deleted!")
             return redirect(request.META.get("HTTP_REFERER"))
        else:
             messages.success(request, "You Don't Own That post")
             return redirect('home')

    else:
         messages.success(request, f'PLease Log In To Continue..')
         return redirect(request.META.get("HTTP_REFERER"))



def edit_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user.username == post.user.username:
            form = PostForm(request.POST or None, instance=post)
            if request.method == "POST":
                if form.is_valid():
                   post = form.save(commit=False)
                   post.user = request.user
                   post.save()
                   messages.success(request,("You Post Hass Been Updated!") )
                   return redirect ('home')
            else:
               return render(request, "edit_post.html", {"form":form ,'post': post})
        else:
             messages.success(request, "You Don't Own That post")
             return redirect('home')
    else:
         messages.success(request, f'PLease Log In To Continue..')
         return redirect('home')


def weather(request):
    form = CityForm()  

    if request.method == 'POST':
        if 'add_city' in request.POST:
            form = CityForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
        elif 'clear_all' in request.POST:
            City.objects.all().delete()
            return redirect('home')

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&appid=1e9fb49a4a98c713dbcc8f10f30c9329'
        city_weather = requests.get(url).json()

        # Convert temperature to Celsius
        temperature_celsius = round(city_weather['main']['temp'] - 273.15, 2)

        # Convert wind speed to km/h
        wind_speed_kmh = round(city_weather['wind']['speed'] * 3.6, 2)

        # Format sunrise and sunset times
        sunrise_time = datetime.utcfromtimestamp(city_weather['sys']['sunrise']).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(city_weather['sys']['sunset']).strftime('%H:%M:%S')

        weather = {
            'city': city.name,
            'temperature': temperature_celsius,
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'humidity': city_weather['main']['humidity'],
            'pressure': city_weather['main']['pressure'],
            'windspeed': wind_speed_kmh,
            'sunrise': sunrise_time,
            'sunset': sunset_time
        }

        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather.html', context)
