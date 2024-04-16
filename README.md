# Driver App

Inspired by Uber, this is a web app that lets users view Google maps and request rides from nearby drivers to bring them to some destination. Users can create an
account as either a driver or a non-driver to experience the app in 2 different ways. Non-driver users can see all drivers on the map around
them and they can click on any one of them to go to their profile. From the driver's profile, users can request a pickup, write a review for the driver,
 and view the driver's information. Once a pickup is complete, the user can then press "complete pickup" on the driver's profile to confirm that
 they've arrived at their destination.
 
Driver users on the other hand won't see any other users on the map until a non-driver user presses "request a pickup" on their profile. When that happens,
 every user that has requested a pickup by the driver will be shown on the map and the driver can decide at their own discretion on which user
 that they want to drive to and pickup. When the user presses "complete pickup" on their profile, they're no longer seen on the driver's map.
 
Map updates for tracking each user's position is done through saving user coordinates into the database and reloading the page every so often.
 
Users can also go on their own profiles to update their information and upload a profile picture.

**This project works best on mobile devices or other systems with geolocation services.**


   
## Project Responsibilities



* Created project and configured the project settings.py
* Configured the project urls
* Wrote the SignUp form in forms.py
* Wrote every view in views.py and ensured they worked correctly with urls and templates
* Configured two-factor authentication to work with the login page
* Configured the app urls
* Wrote the register and profile templates and the javascript in the profile template
* Wrote the logic in the index template to allow for actual user coordinates to be shown on the map depending on whether driver or non-driver
* Wrote the models.py for the UserInfo and Review models
* Wrote tests for the models
* Wrote the css for the project in style.css
* Created yaml heat template and environment to download needed packages and deploy the project automatically, as well as to download and install jenkins on 2 different servers
* Configuring project on Openstack through yaml files and sshing into server instances
* Made so project is accessible through ngrok in deploy server
* Attempted configuring Jenkins to build and deploy project to deploy server through webhook
* Ensured comments were written on all parts of project
* Writing of this readme markdown file
* Configured the Google Maps API on the index template using javascript
* Wrote logic for randomly placing users from database onto the map
* Wrote tests for the views
* Helped with the two-factor authentication

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to install the app, you'll need Python3, pip3, and Django. (This may be optionally done inside an environment.)[https://virtualenvwrapper.readthedocs.io/en/latest/]

Installing these using Ubuntu command line:

```
sudo apt install python3 -y
sudo apt install python3-pip -y
pip3 install Django
```

### Installing

In order to get a running development envionment, follow these steps.

1\. Download the project files or clone the project to a directory, cd to project directory:

```
git  <destination-directory>
cd <destination-directory>/driver_app
```

2\. Install requirements with included requirements file:

```
pip3 install -r requirements.txt
```

3\. Migrate the database:

```
python3 manage.py makemigrations map
python3 manage.py migrate
```

4\. Add validation service to yubikey plugin:

```
python3 manage.py shell
>>> from otp_yubikey.models import ValidationService
>>> ValidationService.objects.create(name='default', use_ssl=True, param_sl='', param_timeout='')
>>> exit()
```

5\. Run the test server and open localhost:8000 using a browser:

```
python3 manage.py runserver
```


In order to manage data in the app:

1\. Create a superuser:

```
python3 manage.py createsuperuser
```

2\. Run server then visit admin page and login with new admin account at "localhost:8000/admin":

```
python3 manage.py runserver
```

### Installing Through Heat Template

Included with this project are yaml heat templates located in the "projectyaml" directory. Follow these steps to install the project on Openstack:

1\. Open the files in a new stack on Openstack

2\. Go into the deploy server's console and run the server along with ngrok

```
cd /code/driver_app
python3 manage.py runserver &
ngrok http 8000
```

## Running the tests

In order to test the project, cd to the project directory and run the tests

```
python3 manage.py test
```

These test for database violations and ensure views work correctly.

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Google Maps](https://developers.google.com/maps/documentation/) - Map API used to display data in app
* [Django Two-Factor Authentication](https://django-two-factor-auth.readthedocs.io/en/stable/) - Built in Two-Factor authentication framework

* [ngrok](https://ngrok.com/docs) - Localhost tunnel to expose app to the Internet

## Authors

* **Brandon Verigin**
* **Griffin Jarvis**
* **Tarsem Monga**

## Acknowledgments

* Django (for their documentation)
* Louis Barranqueiro (for code on uploading to user directories)