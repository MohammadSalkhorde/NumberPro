from django.urls import path,include
from .views import *

app_name='numbers'
urlpatterns = [
    path("", services_page, name="services_list"),
    path("get-numbers/", get_numbers, name="get_numbers"),
    path("buy/", buy_number, name="buy_number"),
    path('get-code/<int:number_id>/', get_code, name='get_code'),
    path("cancel/ajax/<str:number_id>/", cancel_number_ajax, name="cancel_number_ajax"),
    path("cancel/wait/<int:number_id>/", cancel_wait, name="cancel_wait"),
]

