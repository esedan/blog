from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('post/', views.post,name='post'),
    path('editPost/<str:ref>/', views.editPost,name='edit'),
    path('delete/<str:ref>/', views.delete,name='delete'),

]

