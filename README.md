✅ START THE PROJECT:


cd into project folder

we confirm we have python with python --version

once confirmed, we run the virtual env with: py -m venv venv

then we can go to VS code F1 + "Select interpeter" + select venv env
(in case it doesnt activate we can run ".\venv\Scripts\activate" in the terminal to force it)

run pip install django

check if it installed with: django-admin --version

if ok then run: django-admin startproject <PROJECT NAME> .
(. is to create the folder inside our main folder)

then "python manage.py runserver" to start the server

Ctrl+C to quit

run python manage.py startapp <APPNAME> to create an APP

go to main folder in this case djangocrud/settings.py and seek for INSTALED_APPS to include the new APP, adding it to the ARRAY:

'APPNAME',

✅ IN ORDER TO ADD URLS:


in djangocrud/urls.py import include lib

and add to urlpatterns the path for the new app urls
path('', include('myapp.urls')),

in app add the new url folder with the proper includes and urlpatterns:

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index)
]

✅ IN ORDER TO ADD VIEWS/TEMPLATES:


create a new folder "template" (django will detect this is the main folder for views/templates)

then in view.py file use render function to include the template into the new function

render(request ,"index.html")

✅ IN ORDER TO WORK WITH MIGRATIONS

run python manage.py makemigrations

to create the migrations, then

python manage.py migrate 

to create the tables

if you want to add new tables you just need to go to Models and create a Class for every new table you need (remember every new class need to heritage from models.Model)

to create relationships between models you just need to add the class name to the attribute in the class u need calling object models like this:

attribute = models.ForeignKey(CLASS_NAME, on_delete=models.CASCADE)

✅ IN ORDER TO HANDLE CPANEL

to create a super user to access cpanel we need to run

python manage.py createsuperuser

an follow the instructions

to add and handle new tables we need to go to myapp/admin and import/register the model for the new table, example:

from .models import CLASS_NAME
#
#
admin.site.register(CLASS_NAME)