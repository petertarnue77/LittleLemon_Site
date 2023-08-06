from django.db import models

# Create your models here. 
class Category(models.Model):
    title = models.CharField(max_length=50) 
    slug = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.title


class MenuItem(models.Model):
    name = models.CharField(max_length=20) 
    price = models.DecimalField(max_digits=4, decimal_places=2) 
    inventory = models.IntegerField(default=1)
    description = models.TextField(default='') 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'Menu' 
       
        
class Booking(models.Model):
    first_name = models.CharField(max_length=20) 
    last_name = models.CharField(max_length=20) 
    booking_time = models.TimeField(auto_now=True) 
    number_of_person = models.IntegerField() 
    notes = models.TextField() 
    
    def __str__(self):
        return self.first_name 
    
    class Meta:
        db_table = 'Booking' 
        indexes = [
            models.Index(fields=['number_of_person'])
        ]