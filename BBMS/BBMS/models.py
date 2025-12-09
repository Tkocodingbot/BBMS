from django.db import models
from django.contrib.auth.models import User

class Boardroom(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    location = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    description = models.CharField(max_length=150)
    equipment = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"
   
    
class TimeSlot(models.Model):
    TIME_SLOTS = [
        ('08:00-09:00', '8:00 AM - 9:00 AM'),
        ('09:00-10:00', '9:00 AM - 10:00 AM'),
        ('10:00-11:00', '10:00 AM - 11:00 PM'),
        ('11:00-12:00', '11:00 PM - 12:00 PM'),
        ('12:00-13:00', '12:00 PM - 1:00 PM'),
        ('13:00-14:00', '1:00 PM - 2:00 PM'),
        ('14:00-15:00', '2:00 PM - 3:00 PM'),
        ('15:00-16:00', '3:00 PM - 4:00 PM'),
    ]

    date = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    boardroom = models.ForeignKey(Boardroom, on_delete=models.CASCADE)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['date', 'time_slot', 'boardroom']
        ordering = ['date', 'time_slot']
    
    def __str__(self):
        return f"{self.date} - {self.get_time_slot_display()} - {self.boardroom.name}"

    def __str__(self):
        return f"slot for {self.date} at {self.start_time}"
    
        
class Booking(models.Model):
    subject = models.CharField(max_length=100)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    boardroom = models.ForeignKey(Boardroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}"





