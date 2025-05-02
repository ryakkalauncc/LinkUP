# linkup/urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from linkup import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('mypage/', views.mypage, name='mypage'),
    
    # URL for owned events
    path('owned-events/', views.owned_events, name='owned_events'),

    path('create/', views.create_event, name='create_event'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/events/', views.calendar_events, name='calendar_events'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('suggestions/', views.suggest_free_times, name='suggest_free_times'),



]
