from django.urls import path

from welcome import views

urlpatterns = [
    path('', views.main_view),
    path('about', views.about_view)
]
