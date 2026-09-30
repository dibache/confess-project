from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('write/', views.write_post, name='write_post'),
    path('read/', views.choose_category, name='choose_category'),
    path('read/<int:category_id>/', views.read_category, name='read_category'),
    path('upvote/<int:post_id>/', views.upvote, name='upvote'),

    # مسیر جدید ثبت‌نام
   path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'), # این خط اضافه شود
]