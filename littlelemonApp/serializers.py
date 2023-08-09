from rest_framework import serializers 
from django.contrib.auth.models import User 
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator
from decimal import Decimal 
import bleach

from .models import MenuItem, Category, Cart, Order, OrderItem, Rating



class CategorySerializer(serializers.ModelSerializer): 
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        attrs['slug'] = bleach.clean(attrs['title'])
        
    class Meta: 
        model = Category 
        fields = ['id', 'title']


# view for nesting category field as detial field inside MenuItems
class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    title = serializers.CharField(source='name', validators = [UniqueValidator(queryset=MenuItem.objects.all())]) 
    
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        
        attrs['featured'] = bleach.clan(attrs['featured'])
        
        attrs['price'] = bleach.clean(attrs['price'])
        
        if (attrs['price']<2):
            raise serializers.ValidationError("price can't less then 2.00.")
        
        return super().validate(attrs) 
    
    class Meta: 
        model = MenuItem
        fields = ['id','price','title','price_after_tax', 'category', 'featured'] 
        #depth keyword is used to display nested fields
        depth = 1
        
    def calculate_tax(self, product:MenuItem): 
        result = product.price * Decimal(1.1) 
        return result 


class CartSerializer(serializers.ModelSerializer): 
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), default=serializers.CurrentUserDefault) 
    
    def validate(self, attrs): 
        attrs['price'] = (bleach.clean(attrs['quantity'] * attrs['unit_price']))
        return attrs 
    
    class Meta: 
        model = Cart 
        fields = ['user','menuitem','unit_price','quantity','price'] 
        extra_kwargs = {'price': {'read_only': True}} 
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta: 
        models = OrderItem 
        fields = ['order', 'menuitem', 'quantity', 'price'] 
        
        
class OrderSerializer(serializers.ModelSerializer): 
    orderitem = OrderItemSerializer(many=True, read_only=True, source='order') 
    class Meta: 
        model = Order 
        fields = ['id','user','delivery_crew','status','date', 'total','orderitem'] 


class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User 
        fields =['id', 'username', 'email']
    

# class RatingSerializer (serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Rating
#         fields = ["user", 'menuitem_id', 'rating']

#     validators = [
#         UniqueTogetherValidator(
#             queryset=Rating.objects.all(),
#             fields=['user', 'menuitem_id', 'rating']
#         )
#     ]
    
#     extra_kwargs = {
#         'rating': {'min_value': 0, 'max_value':5},
#     }


# View for nesting category field inside MenuItems as hyperlinked
# class MenuItemSerializer(serializers.HyperlinkedModelSerializer): 
#     price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax') 
#     stock = serializers.IntegerField(source='inventory') 
#     # vaidate for unique name in the MenuItem
#     title = serializers.CharField(source='name', validators=[UniqueValidator(queryset=MenuItem.objects.all())] ) 
    
#     # Validate price and inventory fields
#     def validate(self, attrs):
#         attrs['title'] = bleach.clean(attrs['title'])
#         if (attrs['price'] < 2):
#             raise serializers.ValidationError('Price should not be less 2.0') 
#         if (attrs['inventory'] < 0):
#             raise serializers.ValidationError("Stock cannot be negative") 
#         return super().validate(attrs)
    
#     class Meta: 
#         model = MenuItem 
#         fields = ['id', 'title','price','stock','description','price_after_tax','category'] 
    
#     def calculate_tax(self, product:MenuItem):
#         result = product.price * Decimal(1.1) 
#         return result


        