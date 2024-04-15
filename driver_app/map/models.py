
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# https://stackoverflow.com/questions/34239877/django-save-user-uploads-in-seperate-folders
# define the directory path for each file upload by user
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# model to provide extra information for auth User model
class UserInfo(models.Model):
    # refers to only one user per UserInfo
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # image for the User's profile picture
    image = models.FileField(upload_to=user_directory_path, blank=True)
    # biography for the user's profile page
    bio = models.CharField(max_length=1000, default='')
    # boolean for if the created user is a driver or not
    is_driver = models.BooleanField()
    # stores the latitude and longitude of user when they book to be picked up or are a driver
    cur_lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    cur_long = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    # used for tracking the driver that a user wants to be picked up by
    driver_id = models.IntegerField(default=0)

    def __str__(self):
        return self.bio


# model for the reviews that each driver may have on their profile
class Review(models.Model):
    # each user may have multiple reviews
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # the username of the other user that writes the review
    author = models.CharField(max_length=50)
    # a 1 - 5 rating of the driver
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    # text for what the user thought of the driver
    review_text = models.CharField(max_length=500)

    def __str__(self):
        return self.review_text
