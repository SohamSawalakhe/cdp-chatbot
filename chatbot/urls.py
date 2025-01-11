from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Show the chatbot interface
    path('ask/', views.ask_question, name='ask_question'),
     path('', views.ask_question, name='ask_question'),  # Handle user questions
]
