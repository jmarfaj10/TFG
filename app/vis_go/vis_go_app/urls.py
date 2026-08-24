from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('singup/', views.singup_view, name='singup'),
    path('logout/', views.logout_view, name='logout'),
    path('controlPanel/', views.controlPanel_view, name='controlPanel'),
    path('logs/', views.logs_view, name='logs'),
    path('logs/<int:log_id>/', views.log_view, name='log'),
    path('logs/delete', views.logs_remove, name='log_delete')
]
