from django.contrib import admin

# Register your models here.
from .models import MenuItem, Category
from .models import Booking, Cart, Order, OrderItem

@admin.register(MenuItem) 
class menuItem(admin.ModelAdmin):
    list_display = ('title', 'price')  
    
    
@admin.register(Category)
class category(admin.ModelAdmin):
    list_display = ('title', 'slug')
    

@admin.register(Booking) 
class booking(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'booking_time', 'number_of_person') 
    
    
@admin.register(Cart)
class cart(admin.ModelAdmin):
    list_display = ('user','menuitem','quantity','price') 
    
    
@admin.register(Order) 
class order(admin.ModelAdmin):
    list_display = ('user','delivery_crew','status','total','date') 


@admin.register(OrderItem) 
class orderItem(admin.ModelAdmin): 
    list_display = ('order','menuitem','quantity', 'price')