from django.urls import path
from . import views 
urlpatterns = [
    path('api/home',views.HomeView.as_view(),name= 'home'),
    
]
