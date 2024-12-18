from django.urls import path
from .views import add_category, view_categories, delete_category

urlpatterns = [
    path('add/', add_category, name='add_category'),
    path('view/', view_categories, name='view_categories'),
    path('<int:category_id>/delete/', delete_category, name='delete_category'),
]
