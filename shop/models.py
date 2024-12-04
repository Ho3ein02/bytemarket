from django.db import models
from django_jalali.db import models as jmodels


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    weight = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    off_percent = models.PositiveIntegerField(default=0)
    new_price = models.PositiveIntegerField(default=0)
    inventory = models.PositiveIntegerField(default=0)
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=('slug', 'id')),
            models.Index(fields=('name',)),
            models.Index(fields=('created',)),
        ]

    def save(self, *args, **kwargs):
        self.slug = self.name.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="features")

    def __str__(self):
        return f"{self.name}: {self.value}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='product_images/%Y-%m-%d', max_length=255)
    title = models.CharField(max_length=255)
    created = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



