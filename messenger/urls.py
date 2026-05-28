from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/messages/', views.messages, name='messages'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('conversations/', views.conversations, name='conversations'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
    path('conversations/admin/<int:user_a_id>/<int:user_b_id>/', views.admin_conversation, name='admin_conversation'),
    path('logout/', views.logout, name='logout'),
]

