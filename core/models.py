from django.db import models
from django.contrib.auth.models import User
class Event(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    date=models.DateTimeField()
    venue=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.URLField(blank=True)
    available_seats = models.PositiveIntegerField(default=100)
    def __str__(self):
        return self.title
class Booking(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    event=models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date=models.DateTimeField(auto_now_add=True)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"