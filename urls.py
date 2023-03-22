from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login, name="login"),
    path('signup', signup, name="signup"),
    path('site_logout', site_logout, name="site_logout"),
    
    path('student_home', student_home, name="student_home"),
    path('follow/<int:id>', add_follower, name="add_follower"),
    
    path('profile/<int:id>', profile, name="profile"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "app1.views.page_not_found_view"