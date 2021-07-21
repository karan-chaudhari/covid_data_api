from .views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('fetch/', fetch_data, name='fetch_data'),
    path('api/signup/', SignupAPI.as_view(), name='signup'),
    path('send_mail/', send_mail, name='send_mail'),
]