from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


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


class Basket(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = (
        (OPEN, 'Open'),
        (SUBMITTED, 'Submitted'),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATUSES, default=OPEN)

    def is_empty(self):
        return self.basketlines.count() == 0

    def count(self):
        return sum([i.quantity for i in self.basketlines.all()])


class BasketLine(models.Model):
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name='basketlines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1), ])
