# rentals/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Zone(models.Model):
    name = models.CharField(max_length=100) # Örn: Oldtown, Waterfront

    def __str__(self):
        return self.name

class Bike(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'), # Müsait (Yeşil)
        ('reserved', 'Reserved'),   # Rezerve (Turuncu)
        ('unavailable', 'Unavailable'), # Alınmış (Kırmızı)
    )
    
    bike_number = models.CharField(max_length=10) # Örn: 01, 02
    bike_type = models.CharField(max_length=50, default="Standard")
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='bikes')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Bike {self.bike_number} - {self.zone.name} ({self.status})"
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Rezervasyon aktif mi, bitti mi yoksa iptal mi edildi?
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user.username} - {self.bike.bike_number} ({self.status})"

class RentalsDemanddata(models.Model):
    # timestamp alanını primary_key=True yaparak Django'nun hata vermesini engelliyoruz
    timestamp = models.TextField(primary_key=True) 
    zone = models.TextField(blank=True, null=True)
    is_weekend = models.IntegerField(blank=True, null=True)
    temperature_c = models.FloatField(blank=True, null=True)
    rain_mm = models.FloatField(blank=True, null=True)
    event_score = models.FloatField(blank=True, null=True)
    commute_index = models.FloatField(blank=True, null=True)
    bike_demand = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True  # Bunu True yapalım ki Django tabloyu tam kontrol edebilsin
        db_table = 'rentals_demanddata'