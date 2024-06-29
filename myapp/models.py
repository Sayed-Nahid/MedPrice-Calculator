from django.db import models

class ImageClassification(models.Model):
    image = models.ImageField(upload_to='images/')
    output_class = models.CharField(max_length=255)
    corrected_class = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image.name} - {self.output_class} - {self.corrected_class}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=10)
    quantity_in_stock = models.PositiveIntegerField(blank=True, null=True, default=1000)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    image_class = models.ForeignKey(ImageClassification, null=True, related_name='item', on_delete=models.SET_NULL)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.slug
