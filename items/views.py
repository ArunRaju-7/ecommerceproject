from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import  Products, Categories
from .serializers import ProductsSerializer


@api_view(['POST'])
def create_view(request):
    category_name = request.data.get('category', None)
    if category_name is None:
        return Response({'error': 'category_name is missing'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Try to find the category by name
        category = Categories.objects.get(name=category_name)
    except Categories.DoesNotExist:
        category = Categories.objects.create(name=category_name)

    data = request.data.copy()
    data['category'] = category.id
    product = ProductsSerializer(data=data)
    if product.is_valid():
        product.save()
        return Response(product.data, status=status.HTTP_201_CREATED)
    return Response(product.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_view(request, pk=None):
    if pk is None:
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
    else:
        try:
            product = Products.objects.get(pk=pk)
            serializer = ProductsSerializer(product)
        except Products.DoesNotExist:
            return Response({'error': 'product does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', 'PATCH'])
def update_view(request, pk):
    if pk is None:
        return Response({'error': 'id is missing'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        product = Products.objects.get(pk=pk)

        category_name = request.data.get('category', None)

        if category_name is not None:
            try:
                # Try to find the category by name
                category = Categories.objects.get(name=category_name)
            except Categories.DoesNotExist:
                category = Categories.objects.create(name=category_name)
            data = request.data.copy()
            data['category'] = category.id
        else:
            data = request.data.copy()

        serializer = ProductsSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Products.DoesNotExist:
        return Response({'error': 'product does not exist'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def delete_view(request, pk):
    try:
        product = Products.objects.get(pk=pk)
        product_id = product.id
        product.delete()
        return Response({'data' : f"product {product_id} {product.name} is deleted"},status=status.HTTP_204_NO_CONTENT)
    except Products.DoesNotExist:
        return Response({'error': 'product does not exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_view(request):

    search_val = request.query_params.get('product', None)
    if search_val is None:
        return Response({'error': 'search_val is missing'}, status=status.HTTP_400_BAD_REQUEST)
    product = Products.objects.filter(name__icontains=search_val)
    if product is None:
        return Response({'error': 'product does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ProductsSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)