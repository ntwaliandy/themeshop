from django.urls import path
from . import views
from django.conf.urls import url

app_name = 'products'

urlpatterns = [
    path('', views.products, name='products'),
    url(r'^(?P<pid>[0-9]+)/$', views.product_details, name="product-details"),
    path('purchase', views.purchase, name="purchase"),
    path('order-details', views.order, name='order-details'),
    path('user-account', views.user_account, name='user_account'),
    path('user-upload', views.user_upload, name='user_upload'),
    path('user-account/edit', views.user_account_edit, name='user_account_edit')
]