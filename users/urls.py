from django.urls import path
from .views import SignUpView, LoginView, UpdateProfileView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),

]
