from django.contrib import admin
from django.urls import path, re_path
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name="archive"),
    path('sign-up/', views.sign_up, name="sign_up"),
    path('sign-in/', views.sign_in, name="sign_in"),
    path('logout/', views.custom_logout, name="custom_logout"),
    path('article/new/', views.create_post, name="create_post"),
    re_path(r'^article/(?P<article_id>\d+)$', views.get_article, name='get_article'),
]