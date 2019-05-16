from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import Movie
from bs4 import BeautifulSoup
import threading
import urllib
import os
import re

# View inside the website
# define to get youTube link by the movie name.
def get_youtube_link(movie):
    # Create query using urllib function with movie name.
    query = urllib.quote_plus(movie.Name)

    # Create f variable that uses urllib to open YouTube URL plus the query name.
    f = urllib.urlopen('https://www.youtube.com/results?search_query='+query+'+trailer').read()
    
    # Using BeautifulSoup to extract data from the URL using lxml parser. 
    soup=BeautifulSoup(f,'lxml')

    # Find all the matches data and print them.
    item = soup.find_all('ol',{'class':'item-section'})
    for itm in item:
        a = item[0].find_all('a',{'class':'yt-uix-sessionlink'})[0]    
    a = re.findall('=(.*)',a.get('href'))
    print (a)

    # Send the movie trailer in its database and save it.
    link= 'http://www.youtube.com/embed/'+a[0]
    movie.trailer=link
    movie.save()

# define index which return request.
def index(request):

    # if the user try to store or retrieve data,
    # get all objects in Movie database and return main.html.
    if 'user' in request.session:
        movies=Movie.objects.all()
        return render(request,'main.html',{'movies':movies})    
    return render(request,'login.html')

# define log in which return request.
def logged_in(request):

    # When the user login and their data is authenticate get all movie objects
    # and return to the main.html page.
    if 'user' in request.session and request.user.is_authenticated:
        movies=Movie.objects.all()
        return render(request,'main.html',{'movies':movies})

    # Get the user username and password.    
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        # If user isn't exist show error message.
        if not User.objects.filter(username=username).exists():
            return render(request,'login.html',{'error_message':'Please Register First'})
        
        # If the user login, and their data correct, get the all movie objects and get the user to the main.html,
        # or else show error message.    
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                request.session['user']=username
                movies=Movie.objects.all()
                return render(request, 'main.html', {'movies':movies})
            else:
                return render(request,'login.html',{'error_message':'Your Account Has Been Suspended'})

        # return to the login page if the user's data is not right.        
        return render(request,'login.html',{'error_message':'Wrong Credentials'})
    return render(request,'login.html')

# define ability to register for the user
def register(request):

    # get username, password, repetition password, and email from the user.
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        rep_password=request.POST['rep_password']
        e_mail=request.POST['email']

        # if user"s email, username, and password exist show error message or else
        # set the user data and save it to the system.
        if User.objects.filter(email=e_mail).exists():
            return render(request,'register.html',{'error_message':'E-mail already registered'})
        elif User.objects.filter(username=username).exists():
            return render(request,'register.html',{'error_message':'Username not available'})
        elif(password!=rep_password):
            return render(request,'register.html',{'error_message':'Passwords Dont match'})
        else:
            user=User(username=username,email=e_mail)
            user.set_password(password)
            user.save()
            user=authenticate(username=username,password=password)
            login(request,user)
            request.session['user']=username
            movies=Movie.objects.all()
            return render(request,'main.html',{'movies':movies})
    return render(request,'register.html')

# define ability to log out for the user
def log_out(request):

    # request logout function and redirect to the login page.
    if 'user' in request.session:
        del request.session['user']
        logout(request)
        return redirect('logged_in')

# define detail movie.
def Detail_movie(request,movie_id):

    # if the user isn't authenticated direct the user to the login page
    if not request.user.is_authenticated:
        return redirect('logged_in')

    # Create a thread that print the get_youtube_link method.     
    threadobj= threading.Thread(target=get_youtube_link,args=[])
    movie=get_object_or_404(Movie,id=movie_id)
    print (movie.trailer)
    if not movie.trailer:
        try:
            get_youtube_link(movie)
        except:
            pass
    return render(request,'details.html', {'movie':movie})

# define search movie.
def search_movie(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if not request.POST['search']:
                return redirect('logged_in')
            # Get all matches movie from the search input from the user    
            if '-w' in request.POST['search']:
                Q=re.findall('(.*)\s+-w',request.POST['search'])

                # if not match, filter by the unwatched movie else
                # get the name, year, and genre of the movie. 
                if not Q:
                    movies=Movie.objects.filter(Watched=False)
                    return render(request,'main.html',{'movies':movies})
                else:
                    Q=Q[0]
                    list1=Movie.objects.filter(Name__contains=Q,Watched=False)
                    list2=Movie.objects.filter(Year__contains=Q,Watched=False)
                    list3=Movie.objects.filter(Genre__contains=Q,Watched=False)

            # if movie found get the name, year, and genre.
            else:
                Q=request.POST['search']
                list1=Movie.objects.filter(Name__contains=Q)
                list2=Movie.objects.filter(Year__contains=Q)
                list3=Movie.objects.filter(Genre__contains=Q)

            # Set context with the list objects.
            res=list(set(list1)^set(list2)^set(list3))
            context={
                'movies':res,
            }
            return render(request,'main.html',context)
    return redirect('logged_in')

# define play movie return request and movie_id
def Play_movie(request,movie_id):

    # If requested from user is authenticated get the movie by movie id
    if request.user.is_authenticated:
        movie=get_object_or_404(Movie,id=movie_id)
        os.system('xdg-open '+'"'+movie.Path+'"')
        return render(request,'details.html',{'movie':movie})
    return redirect('logged_in')

# define favorite movies
def Favorite(request,movie_id):

    # if it's the favorite movie to watch then false else true
    if request.user.is_authenticated:
        movie=get_object_or_404(Movie,id=movie_id)
        if movie.Watched:
            movie.Watched=False
        else:
            movie.Watched=True
        movie.save()
    return redirect('logged_in')

# define marked watched and unwatched movie
def Watched(request,movie_id):

    # if the movie watched then marked as false else true
    if request.user.is_authenticated:
        movie=get_object_or_404(Movie,id=movie_id)
        if movie.Watched:
            movie.Watched=False
        else:
            movie.Watched=True
        movie.save()
        return render(request,'details.html',{'movie':movie})
    return redirect('logged_in')
