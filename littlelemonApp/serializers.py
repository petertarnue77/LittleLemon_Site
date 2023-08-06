from rest_framework import serializers 
from .models import MenuItem, Category 
from decimal import Decimal 
import bleach

from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category 
        fields = ['id','title', 'slug']

# view for nesting category field as detial field inside MenuItems
class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    title = serializers.CharField(source='name', validators = [UniqueValidator(queryset=MenuItem.objects.all())]) 
    stock = serializers.IntegerField(source='inventory')     
    
    def validate(self, attrs):
        attrs['title'] = bleach.clean(attrs['title'])
        if (attrs['price']<2):
            raise serializers.ValidationError("price can't less then 2.00.") 
        if (attrs['inventory']< 0):
            raise serializers.ValidationError('Stock cannot be less then 0')
        return super().validate(attrs)
    
    class Meta: 
        model = MenuItem
        fields = ['id','price','title','stock','description','price_after_tax', 'category'] 
        #depth keyword is used to display nested fields
        depth = 1
        
    def calculate_tax(self, product:MenuItem): 
        result = product.price * Decimal(1.1) 
        return result 


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


        