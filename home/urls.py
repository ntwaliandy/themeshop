from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('manage', views.manage, name="manage_items"),
    path('order-activity', views.activity, name="order_activity"),
    path('uploadp1', views.uploadp1, name="product_upload1"),
    path('webhook', views.webhook, name="webhook"),
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add-category'),
    path('categories/edit/', views.edit_category, name='edit-category'),
    path('categories/delete/', views.remove_category, name='delete-category'),
    path('tags/', views.tags, name='tags'),
    path('tags/add/', views.add_tags, name='add-tags'),
    path('product/delete/', views.remove_product, name='delete-product'),
    path('product/edit/', views.edit_product, name='edit-product'),
    path('all-users/', views.all_users, name='all-users')
]