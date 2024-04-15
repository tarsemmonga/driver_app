
from django.test import TestCase
from django.urls import reverse
from django.test import Client

from .models import *
from django.contrib.auth.models import User


# simple tests to see if views work on request
class ViewTests(TestCase):

    client = Client()

    def setUp(self):
        # enter a user into the database
        user = User.objects.create(email='example@example.com', username='test', first_name='john', last_name='smith', password='password')
        user.save()

    def login_successful(self):
        bool = self.client.login(username='test', password='password')
        self.assertIs(bool, True)

    def test_profile_with_existing_user(self):
        response = self.client.get('/1/')
        self.assertEqual(response.status_code, 200)

    def test_profile_with_nonexistent_user(self):
        response = self.client.get('/4/')
        self.assertEqual(response.status_code, 404)

    def test_register(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get('')
        self.failUnlessEqual(response.status_code, 302)


# review model tests
class ReviewModelTests(TestCase):

    def __init__(self):
        # need user
        self.user = User.objects.create(email='example@example.com', username='test', first_name='john', last_name='smith', password='password')

    # create some reviews in the database
    def setUp(self):
        rev1 = Review.objects.create(user=self.user, author='testman', rating=3, review_text='This is a test!')
        rev2 = Review.objects.create(user=self.user, author='testwoman', rating=1, review_text='This is a test! This is test!')
        rev1.save()
        rev2.save()
        self.user.save()

    # review cant be created without any values
    def review_created_with_no_values(self):
        review = Review()
        self.assertIs(review.id is null, True)

    # review created with max rating of 5
    def review_created_with_large_rating(self):
        review = Review(user=self.user, author='testman', rating=100, review_text='This is a test!')
        self.assertIs(review.rating <= 5, True)

    # review created with min rating of 0
    def review_created_with_small_rating(self):
        review = Review(user=self.user, author='testman', rating=-55, review_text='This is a test!')
        self.assertIs(review.rating >= 0, True)

    # review created can only have max review_text of 500
    def review_created_with_large_text(self):
        review = Review(user=self.user,author='testman', rating=3, review_text='This is a test!asssssllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssdsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')
        self.assertIs(len(review.review_text) <= 500, True)

    # review created can only have max author text of 50
    def review_created_with_large_author(self):
        review = Review(user=self.user, author='testmannnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn', rating=3, review_text='This is a test!')
        self.assertIs(len(review.author) <= 50, True)

    # reviews created cant have the same id/pk
    def reviews_with_different_ids(self):
        reviews = Review.objects.all()
        self.assertIs(reviews[0].id != reviews[1].id, True)



# userinfo model tests
class UserInfoModelTests(TestCase):

    def __init__(self):
        # need user
        self.user = User.objects.create(email='example@example.com', username='test', first_name='john', last_name='smith', password='password')

    # create some userinfos in the database
    def setUp(self):
        inf1.objects.create(user=self.user, bio='Hi I am a test! Good luck!!', is_driver=True, cur_lat=22.222, cur_long=11.1111)
        inf2.objects.create(user=self.user, bio='Hi I am a test! Good luck!!', is_driver=False, driver_id=1)
        inf1.save()
        inf2.save()
        self.user.save()

    # userinfo cant be created without any values
    def userinfo_created_with_no_values(self):
        userinfo = UserInfo()
        self.assertIs(userinfo.id is null, True)

    # userinfo can be created without image, cur_lat, cur_long, bio, and driver_id
    def userinfo_created_with_missing_values(self):
        userinfo = UserInfo(user=self.user, is_driver=True)
        self.assertIs(userinfo.id is null, False)

    # userinfo created cant have the same id/pk
    def reviews_with_different_ids(self):
        infos = UserInfo.objects.all()
        self.assertIs(infos[0].id != infos[1].id, True)

