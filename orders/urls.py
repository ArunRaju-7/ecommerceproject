from django.urls import path
from .views import OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView, OrderDetailView

urlpatterns = [
    path('', OrderListView.as_view(), name='orderlist'),
    path('<int:id>/', OrderDetailView.as_view(), name='detailorder'),
    path('create/', OrderCreateView.as_view(), name='addorder'),
    path('update/<int:id>/', OrderUpdateView.as_view(), name='updateorder'),
    path('delete/<int:id>/', OrderDeleteView.as_view(), name='deleteorder')
]