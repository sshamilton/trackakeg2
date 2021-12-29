from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('pints', views.pints, name='pints'),
        ]
