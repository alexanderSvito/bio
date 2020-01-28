from django.urls import path
from questions import views

urlpatterns = [
    path('start', views.start),
    path('<int:pk>', views.question)
]
