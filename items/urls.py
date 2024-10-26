from django.urls import path

from .views import create_view, list_view, update_view, delete_view, search_view
urlpatterns = [
    path('', list_view, name='list'),
    path('<int:pk>/', list_view, name='list'),
    path('create/', create_view, name='create'),
    path('update/<int:pk>/', update_view, name='update'),
    path('delete/<int:pk>/', delete_view, name='delete'),
    path('search/', search_view, name='search'),
]