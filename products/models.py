from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    isActive=models.BooleanField(default=True)     

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    isActive=models.BooleanField(default=True)     


    def __str__(self):
        return self.name
    
    def popularity_score(self):
        sales = Sale.objects.filter(product=self)
        total_sales = sales.count()
        total_revenue = sum(sale.quantity * sale.product.price for sale in sales)
        # Example popularity score calculation
        score = (total_sales * 0.5) + (total_revenue * 0.5)  # Adjust weights as necessary
        return score

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    isActive=models.BooleanField(default=True) 