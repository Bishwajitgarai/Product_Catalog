from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product,Sale

server_url='http://localhost:5000'

class CustomTestCase(TestCase):
    def setUp(self):
        # Set up test client
        self.client = APIClient()

        # Create a category via JSON
        self.category_data = {
            "name": "Electronics"
        }
        self.category_response = self.client.post(
            f'{server_url}/api/category/create/',
            self.category_data,
            format='json'
        )
        
        # Check if category creation was successful
        if self.category_response.status_code == status.HTTP_201_CREATED:
            self.category_id = self.category_response.json().get("data", {}).get("id")  # Get the ID directly
        else:
            self.fail("Failed to create category: {}".format(self.category_response.data))

        # Create products associated with the category via JSON
        self.active_product_data = {
            "name": "Laptop",
            "description": "High-end gaming laptop",
            "price": 1500.00,
            "inventory_count": 10,
            "category": self.category_id,  # Use the category ID from the response
            "isActive": True
        }
        self.inactive_product_data = {
            "name": "Old Phone",
            "description": "Outdated model",
            "price": 100.00,
            "inventory_count": 0,
            "category": self.category_id,  # Use the category ID from the response
            "isActive": False
        }

        # Create an active product
        self.client.post(
            f'{server_url}/api/product/create/',
            self.active_product_data,
            format='json'
        )
        # Create an inactive product
        self.client.post(
            f'{server_url}/api/product/create/',
            self.inactive_product_data,
            format='json'
        )

    def test_delete_category_with_active_products(self):
        """
        Attempt to delete a category that has active products.
        Expecting a 403 Forbidden response.
        """
        url = f'{server_url}/api/category/{self.category_id}/delete/'
        response = self.client.delete(url)
        
        # Assert that the response returns a 403 error
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Cannot delete category with active products.", response.data["msg"])

    def test_delete_category_without_active_products(self):
        """
        Deactivate all products in the category, then attempt to delete the category.
        Expecting a 204 No Content response.
        """
        # Deactivate the active product
        product_id = Product.objects.get(name="Laptop").id  # Get the active product ID
        url1 = f'{server_url}/api/product/{product_id}/delete/'
        
        # Send a DELETE request to deactivate the product
        response = self.client.delete(url1)

        # Check if the response indicates success (optional)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Attempt to delete the category now that the product is inactive
        url = f'{server_url}/api/category/{self.category_id}/delete/'
        response = self.client.delete(url)

        # Assert that the category is deleted successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=self.category_id,isActive=True).exists())  # Check that the category no longer exists

    #Search for the products
    def test_search_product(self):
        response = self.client.get(f'{server_url}/api/product/search/?q=Gaming')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_product_list(self):
        response = self.client.get(f'{server_url}/api/product/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_sale(self):
        """ Create a sale record and check if it was created successfully. """
        product_id = Product.objects.get(name="Laptop").id  # Get the active product ID
        sale_data = {
            "product": product_id,
            "quantity": 2
        }
        response = self.client.post(f'{server_url}/api/sales/create/', sale_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sale.objects.count(), 1)  # Ensure one sale record was created
        self.assertEqual(Sale.objects.get().quantity, 2)  # Check the quantity
        
    def test_list_sales(self):
        """ List sales and check if the response is successful. """
        # First create a sale
        product_id = Product.objects.get(name="Laptop").id  # Get the active product ID
        Sale.objects.create(product_id=product_id, quantity=5)  # Manually create a sale for testing
        
        response = self.client.get(f'{server_url}/api/sales/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)  # Should return the created sale