from django.urls import path
from django.views.generic import TemplateView

from welcome import views
from welcome.views import AboutView, LearnView

urlpatterns = [
    path('', views.main_view),
    path('learn',
         LearnView.as_view()
    ),
    path('about',
         AboutView.as_view()
    ),
]
