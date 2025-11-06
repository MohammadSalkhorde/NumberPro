from django.urls import path,include
from django.contrib.auth import views as auth_views
from .views import *

app_name='main'
urlpatterns = [
    path('',index,name='index'),
    path('about-us/', about_us, name='about-us'),
    path('contact/', contact, name='contact'),
    path('test-payment/', test_payment_view, name='test_payment'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

