from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
    )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    class Meta:
        unique_together = [('name', 'email'), ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True


# ADDRESS_CHOICES = (
#     ('B', 'Billing'),
#     ('S', 'Shipping'),
# )


# class Address(models.Model):
#     SUPPORTED_COUNTRIES = (
#         ('TZ', 'Tanzania'),
#     )
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     zip_code = models.CharField('ZIP / Postal Code', max_length=12)
#     city = models.CharField(max_length=60)
#     country = models.CharField(
#         max_length=3, choices=SUPPORTED_COUNTRIES, default='TZ')
#     address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)

#     class Meta:
#         verbose_name_plural = "Addresses"

#     def __str__(self):
#         return self.user.name
