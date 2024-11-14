from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status, serializers
from orders.models import Order
from orders.serializers import OrderSerializer
from rest_framework import permissions

# Create your views here.

class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def list(self, request, order_id, *args, **kwargs):
        #order_id = request.data['pk']
        queryset = self.get_queryset().filter(id=order_id)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
       serializer.save(user=self.request.user)


class OrderUpdateView(UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDeleteView(DestroyAPIView):
    serializer_class = OrderSerializer
    lookup_field = 'id'
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        if not instance:
            # If instance doesn't exist, return a custom error response
            raise serializers.ValidationError("Order not found.")

        instance.delete()

    def delete(self, request, *args, **kwargs):
        # Retrieve the order instance by id
        try:
            order_instance = self.get_object()
            # Call perform_destroy to delete
            self.perform_destroy(order_instance)
        except Order.DoesNotExist:
            # If order is not found, return a custom response
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except serializers.ValidationError as e:
            return Response({"error": str(f"{e}")}, status=status.HTTP_400_BAD_REQUEST)


        return Response({"message": "Order deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
