from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_bim/', views.generate_bim, name='generate_bim'),
]
