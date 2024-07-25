from django.urls import path
from . import views

urlpatterns = [
    path('create_user/', views.create_user),
    path('create_shift/', views.create_shift),
    path('view_roster/', views.view_roster),
    path('view_shifts/', views.view_shifts),
    path('mark_attendance/', views.mark_attendance),
    path('view_attendance/', views.view_attendance),
    path('set_weekly_off/', views.set_weekly_off),
    path('update_user/<int:user_id>/', views.update_user),
    path('request_shift_change/', views.request_shift_change),
    path('approve_shift_change/', views.approve_shift_change),
]
