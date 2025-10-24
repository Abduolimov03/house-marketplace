from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Foydalanuvchi telefon raqamini kiritishi kerak")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='users/', null=True, blank=True)
    role = models.CharField(max_length=13, default='user')
    is_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.phone_number


class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class House(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    room_count = models.IntegerField()
    floor = models.IntegerField()
    all_floors = models.IntegerField()
    home_situation = models.CharField(max_length=250)
    area_m2 = models.IntegerField()
    area_ar = models.IntegerField()
    location = models.CharField(max_length=250)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    price = models.BigIntegerField()

    def __str__(self):
        return f"{self.category} - {self.price} so'm"

class PricedHouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    room_count = models.IntegerField()
    floor = models.IntegerField()
    all_floors = models.IntegerField()
    home_situation = models.CharField(max_length=250)
    area_m2 = models.IntegerField()
    area_ar = models.IntegerField()
    location = models.CharField(max_length=250)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.category} - {self.price} so'm"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    income_expenditure = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.phone_number} - {self.amount}"

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    expiration_time = models.BigIntegerField()

    def __str__(self):
        return f"Code {self.code} for {self.user.phone_number}"



class BannedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.reason}"


