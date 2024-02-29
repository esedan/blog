from django.urls import path
from . import views

urlpatterns=[
    path('register/' , views.register , name= 'Register'),
    path('login/' , views.logInUser , name= 'login'),
    path('logout/' , views.logOut , name='logout'),
    path('forgotpassword/' , views.forgotPassword, name='forgotpassword'),
    path('forgotpassword/code/<str:ref>/' , views.code, name='code'),
    path('newpassword/<str:ref>/' , views.newPassword, name='newpassword'),
    path('profileform/' , views.profile, name='profile'),
    path('subscribe/' , views.subscribe, name='subscribe'),
    path('newsletter/' , views.sendNewsLetter, name='newsletter'),

]