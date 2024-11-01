from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer,Sale,SaleSerializer
from django.db.models import Q

# Helper function to check for duplicate names
def check_duplicate_name(model, name, exclude_id=None):
    filters = Q(name=name, isActive=True)
    if exclude_id:
        filters &= ~Q(id=exclude_id)
    return model.objects.filter(filters).exists()


# ---------- CATEGORY VIEWS ----------

# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_category(request):
    """
    Create a new category.
    """
    try:
        if check_duplicate_name(Category, request.data.get("name")):
            return Response({"type": "error", "msg": "Category name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"type": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"type": "error", "msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def retrieve_category(request, pk):
    """
    Retrieve a category by id.
    """
    try:
        category = get_object_or_404(Category, pk=pk, isActive=True)
        serializer = CategorySerializer(category)
        return Response({"type": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_category(request, pk):
    """
    Update a category by id.
    """
    try:
        category = get_object_or_404(Category, pk=pk, isActive=True)
        if check_duplicate_name(Category, request.data.get("name"), exclude_id=pk):
            return Response({"type": "error", "msg": "Category name already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"type": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"type": "error", "msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_category(request, pk):
    """
    Soft-delete a category by id.
    """
    try:
        category = get_object_or_404(Category, pk=pk)
        
        # Ensure there are no active products under this category
        if category.products.filter(isActive=True).exists():
            return Response({"type": "error", "msg": "Cannot delete category with active products."}, status=status.HTTP_403_FORBIDDEN)
        
        category.isActive = False
        category.save()
        return Response({"type": "success", "msg": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---------- PRODUCT VIEWS ----------

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_product(request):
    """
    Create a new product.
    """
    try:
        if check_duplicate_name(Product, request.data.get("name")):
            return Response({"type": "error", "msg": "Product name already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"type": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"type": "error", "msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def retrieve_product(request, pk):
    """
    Retrieve a product by id.
    """
    try:
        product = get_object_or_404(Product, pk=pk, isActive=True)
        serializer = ProductSerializer(product)
        return Response({"type": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_product(request, pk):
    """
    Update a product by id.
    """
    try:
        product = get_object_or_404(Product, pk=pk, isActive=True)
        if check_duplicate_name(Product, request.data.get("name"), exclude_id=pk):
            return Response({"type": "error", "msg": "Product name already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"type": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"type": "error", "msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_product(request, pk):
    """
    Soft-delete a product by id.
    """
    try:
        product = get_object_or_404(Product, pk=pk)
        product.isActive = False
        product.save()
        return Response({"type": "success", "msg": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def search_products(request):
    """
    Search for products by name, description, or category.
    """
    try:
        query = request.GET.get('q', '')  # Get the search query from the request
        print(query)
        products = Product.objects.filter(
            Q(name__icontains=query) |  # Search by name
            Q(description__icontains=query) |  # Search by description
            Q(category__name__icontains=query)  # Search by category name
        ).filter(isActive=True)  # Ensure only active products are returned

        serializer = ProductSerializer(products, many=True)
        return Response({"type": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_products(request):
    """
    Retrieve a list of products along with their popularity scores.
    """
    try:
        products = Product.objects.filter(isActive=True)
        serializer = ProductSerializer(products, many=True)
        return Response({"type": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# views.py

# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_sale(request):
    """
    Create a new sale record.
    """
    try:
        product = get_object_or_404(Product, pk=request.data.get("product"), isActive=True)
        quantity = request.data.get("quantity")

        # Check if there's enough inventory to fulfill the sale
        if product.inventory_count < quantity:
            return Response({"type": "error", "msg": "Stock unavailable."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            # Decrease the inventory count of the product
            product.inventory_count -= quantity
            product.save()
            
            serializer.save()
            return Response({"type": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"type": "error", "msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def list_sales(request):
    """
    Retrieve a list of all sales records.
    """
    try:
        sales = Sale.objects.filter(isActive=True).all()
        serializer = SaleSerializer(sales, many=True)
        return Response({"type": "success", "data": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"type": "error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
