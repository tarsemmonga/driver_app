
from django.urls import path

from . import views
from two_factor.urls import urlpatterns as tf_urls
from django.conf.urls import include


app_name = 'map'
# urls to each of the app's views, as needed
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('book/<int:user_id>/', views.book, name='book'),
    path('complete/', views.complete, name='complete'),
    path('update/', views.update_coords, name='update_coords'),

]
