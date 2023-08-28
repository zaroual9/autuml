from django.urls import path
from .views import CustomLoginView, CustomLogoutView, CustomSignupView, generate_uml

urlpatterns = [
    path('', generate_uml, name='generate_uml'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('signup/', CustomSignupView.as_view(), name='signup'),
]

