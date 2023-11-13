from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('pos/', views.terminal, name='pos'),
    path('editpos/', views.editPos, name='editpos'),
    path('deletepos/', views.deletePos, name='deletepos'),
    path('posstaff/<str:pk>/', views.staffPosView, name='posstaff'),
    path('possale/<str:pk>/', views.posSaleView, name='possale'),
]