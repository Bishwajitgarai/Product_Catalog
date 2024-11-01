from rest_framework import serializers
from .models import Product, Category,Sale

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    popularity_score = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = "__all__"
    def get_popularity_score(self, obj):
        return obj.popularity_score()  # Call the method from the Product model

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"
