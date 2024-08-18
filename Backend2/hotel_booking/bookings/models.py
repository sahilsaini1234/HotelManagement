from django.db import models


class Room(models.Model):
    room_type = models.CharField(max_length=50)
    price_per_hour = models.FloatField()
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self

class Booking(models.Model):
    user_email = models.EmailField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_price = models.FloatField()

    def __str__(self):
        return self


# Create your models here.
