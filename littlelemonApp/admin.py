from django.contrib import admin

# Register your models here.
from .models import MenuItem, Category

@admin.register(MenuItem) 
class menu(admin.ModelAdmin):
    list_display = ('name', 'price')  
    
    
@admin.register(Category)
class category(admin.ModelAdmin):
    list_display = ('title', 'slug')
    

from .models import Booking 
@admin.register(Booking) 
class booking(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'booking_time', 'number_of_person') 