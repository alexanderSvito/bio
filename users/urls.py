from django.urls import path
from users import views

urlpatterns = [
    path('verify/email', views.verify_email),
    path('login', views.get_access_token),
    path('logout', views.logout_view),
    path('me', views.me),
    path('verify-email', views.verify_view)
]
