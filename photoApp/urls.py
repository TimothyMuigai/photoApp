from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path('view_photo/<str:pk>/', views.view_photo, name='view_photo'),
    path("register/", views.register, name="register"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="logout"),
    path('profile/',views.profile, name='profile'),
    path('update_password/', views.update_password, name='update_password'),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("filter/<str:tag_name>/", views.filter_photos, name="filter_photos"),
    path("like_photo/<int:photo_id>/", views.like_photo, name="like_photo"),
]   