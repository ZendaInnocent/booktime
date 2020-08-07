from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):

    def active(self):
        return self.filter(active=True)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField()
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('ProductTag', related_name='producttags',
                                  blank=True)

    objects = ProductManager()

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='productimages',
                                on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product-images/')
    thumbnail = models.ImageField(upload_to='product-thumbnails/',
                                  null=True, blank=True)


class ProductTagManager(models.Manager):

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class ProductTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    objects = ProductTagManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug, )
