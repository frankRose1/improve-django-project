from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_list, name='list'),
    path('menu/<int:pk>/edit/', views.edit_menu, name='edit'),
    path('menu/<int:pk>/', views.menu_detail, name='detail'),
    path('menu/item/<int:pk>/', views.item_detail, name='item_detail'),
    path('menu/new/', views.create_new_menu, name='new'),
]