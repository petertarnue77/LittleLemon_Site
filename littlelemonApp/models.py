from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True) 
    
    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT) 
    
    class Meta:
        unique_together = ('title',)
    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('menuitem', 'user')

    def __str__(self):
        return self.user

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(default=0, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    date = models.DateField(db_index=True) 
    
    def __str__(self):
        return self.user


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem') 
        
    def __str__(self):
        return self.order
       
        
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


class Rating(models.Model): 
    menuitem_id = models.SmallIntegerField() 
    rating = models.SmallIntegerField() 
    category = models.ForeignKey(User,on_delete=models.CASCADE) 
    