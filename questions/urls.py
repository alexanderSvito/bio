from django.urls import path
from questions import views

urlpatterns = [
    path('start', views.start),
    path('continue', views.continue_view),
    path('questions', views.questions_view),
    path('<int:pk>', views.question),
]
