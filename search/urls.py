from django.urls import path
from .views import create_search, update_search,get_search

urlpatterns = [
    path('create-search/', create_search, name='create_search'),
    path('update-search/', update_search, name='update_search'),
    path('get_search/<int:user_id>/', get_search, name='get_search'),

]
