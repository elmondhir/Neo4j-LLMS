from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    # path("", views.home, name="home"),
    path('login/', views.login_view, name='login'),
    path('show_graph/<str:database_name>/', views.show_graph, name='show_graph'),
]
