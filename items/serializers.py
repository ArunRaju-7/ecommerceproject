
from rest_framework import serializers
from .models import Categories, Products

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'category', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None