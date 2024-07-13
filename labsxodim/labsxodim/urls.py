"""
URL configuration for labsxodim project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reviews import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/", views.register, name="register"),
    path("login_user", views.user_login, name="login"),
    path("logout_user", views.logout_user, name="logout"),
    path('', views.item_list, name=''),
    path('add', views.add_item, name='add_item'),
    path('delete/<int:pk>/', views.delete_view, name='delete'),
    path('Item/<int:pk>/', views.update_view, name='update'),
    path('search', views.item_search, name='item_search'),
    path('details/<int:pk>/', views.item_detail, name='detail'),
    path('profile', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('users/', views.UserAdminListView.as_view(), name='user_list'),
    path('users/<int:pk>/edit/', views.UserAdminUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserAdminDeleteView.as_view(), name='user_delete'),
    path('create_item_request/', views.create_item_request, name='create_item_request'),
    path('item_request_list/', views.item_request_list, name='item_request_list'),
    path('approve_item_request/<int:item_request_id>/', views.approve_item_request, name='approve_item_request'),
    path('reject_item_request/<int:item_request_id>/', views.reject_item_request, name='reject_item_request'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
