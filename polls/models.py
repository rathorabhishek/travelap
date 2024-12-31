from django.db import models
from django.contrib.auth.models import  User
from django.utils import timezone
import datetime
# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class TimeHrs(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class TravelOneWayInput(models.Model):
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, blank=True, null=True)
    destination = models.ForeignKey(Destination, on_delete=models.DO_NOTHING, blank=True, null=True)
    date = models.DateField()
    time = models.ForeignKey(TimeHrs, on_delete=models.SET_NULL, blank=True, null=True)

class CarDetails(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}  {self.brand}"

class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(CarDetails, on_delete=models.CASCADE )
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)  # Timesta

    def __str__(self):
        return f"{self.user.name} booked {self.car.name}  from {self.start_date} to {self.end_date}"

# class OneWayTravel(models.Model):
#     CATEGORY_CHOICES = [
#         ('option1', 'Option1'),
#         ('option2', 'Option2'),
#         ('option3', 'Option3'),
#     ]
#     source = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default='option1')
#     destination = models.CharField(max_length=40,choices='', default='')

class Country(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=124)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

class CarName(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self):
        return  self.name


class CarModelName(models.Model):
    carname = models.ForeignKey(CarName,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class DriverDetail(models.Model):
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)
    carname = models.ForeignKey(CarName, on_delete=models.SET_NULL, blank=True, null=True)
    cartype = models.ForeignKey(CarModelName, on_delete=models.SET_NULL, blank=True, null=True)
    carnumber = models.CharField(max_length=20)
    address = models.TextField(name="address")
    mobilenumber = models.IntegerField(default=0000000000)
    adharnumber = models.CharField(max_length=20)
    hiringdate = models.DateField()

    def __str__(self):
        return self.firstname +"-"+ self.lastname

class Questions(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("Date Published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return  self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
