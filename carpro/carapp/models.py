from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    email=models.EmailField(blank=True,null=True)

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    registration_number = models.CharField(max_length=20, unique=True)
    daily_rental_rate = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='car_images/', default="")
    availability = models.BooleanField(default=True)
    category = models.ForeignKey('CarCategory', on_delete=models.SET_NULL, null=True)
    transmission = models.CharField(max_length=50, default="")
    fueltype = models.CharField(max_length=50, default="")
    seats = models.IntegerField(default=1)
    mileage = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], default=0.0)
    stock = models.PositiveIntegerField(default=0)



    def book_car(self):
        if self.stock > 0:
            self.stock -= 1
            if self.stock == 0:
                self.availability = False
            self.save()
            return True
        return False

    def revert_stock(self):
        self.stock += 1
        if self.stock > 0:
            self.availability = True
        self.save()

    def complete_booking(self):
        self.stock += 1
        self.save()

    def __str__(self):
        return self.model





class CarCategory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name








class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def mark_as_completed(self):
        self.status = 'Completed'
        self.save()
        self.car.availability = True
        self.car.save()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

# class Contact(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     message = models.TextField()
#     contact_date = models.DateTimeField(auto_now_add=True)
