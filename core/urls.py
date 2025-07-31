from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('video/<int:video_id>/', views.watch_video, name='watch_video'),
    path('upload/', views.upload_video, name='upload_video'),
    path('video/<int:video_id>/edit/', views.edit_video, name='edit_video'),
    path('video/<int:video_id>/delete/', views.delete_video, name='delete_video'),
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),
    path('video/<int:video_id>/comment/', views.add_comment, name='add_comment'),
    path('search/', views.video_search, name='video_search'),


]
