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
    date = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"slot for {self.date} at {self.start_time}"
    
        
class Booking(models.Model):
    subject = models.CharField(max_length=200)
    slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    boardroom = models.ForeignKey(Boardroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
class Attendee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    is_external = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({'External' if self.is_external else 'Internal'})"


                                                                                                                                                                                                                                                                                                                                                                



