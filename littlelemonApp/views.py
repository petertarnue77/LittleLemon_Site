from django.shortcuts import render 
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError 

from django.views.decorators.csrf import csrf_exempt 
from rest_framework.decorators import renderer_classes
from django.forms.models import model_to_dict 

from rest_framework import generics 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import status

from .models import MenuItem
from .models import Booking
from .forms import BookingForm  
from .serializers import MenuItemSerializer


# Create your views here. 
def home(request):
    return render(request, 'index_home.html')


def about(request):
    return render(request, 'about.html')


def book(request):
    booking = BookingForm()
    if request.method == "POST":
        booking = BookingForm(request.POST)
        if booking.is_valid():
            booking.save() 
    booked = {'booking': booking}
    return render(request, 'book.html',booked)


# Add your code here to create new views 
def menu(request):
    menu_data = MenuItem.objects.all() 
    menu_content = {'menu_data': menu_data} 
    return render(request, 'menu.html', menu_content)


def display_menu_item(request, pk=None):
    if pk:
        menu_item = MenuItem.objects.get(pk=pk)
    else:
        menu_item = ""
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 
 

def booking_list(request):
    booking_items = Booking.objects.all() 
    bookingitems = {'booking_items': booking_items} 
    return render(request, 'bookingItems.html', bookingitems) 

# API booking 
@csrf_exempt 
@api_view(['GET','POST'])
def books(request):
    if request.method == "GET": 
        booking = Booking.objects.all().values() 
        return Response({'booking': list(booking)}) 
     
    elif request.method == 'POST':
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        booking_time = request.POST.get('booking_time') 
        number_of_person = request.POST.get('number_of_person') 
        notes = request.POST.get('notes') 
        
        booking = Booking(
            first_name = first_name,
            last_name = last_name,
            booking_time = booking_time,
            number_of_person = number_of_person,
            notes = notes
        ) 
        
        try: 
            booking.save() 
        except IntegrityError:
            return Response({'error': 'true', 'message': 'required field missing'}, status=400)
        
        return Response(model_to_dict(booking), status=201)        

# class based menuItem views
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer 

# class based single menuItem view
class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer
    ordering_fields = ['price','inventory']

# Creating a nested relationship as detial
@api_view(['POST', 'GET'])
def menu_restApi(request):
    items = MenuItem.objects.select_related('category').all() 
    serializered_item = MenuItemSerializer(items, many=True) 
    return Response(serializered_item.data) 


from django.shortcuts import get_object_or_404
@api_view(['POST','GET'])
def single_item_rest(request, id):
    items = get_object_or_404(MenuItem, pk=id) 
    serialized_item = MenuItemSerializer(items) 
    return Response(serialized_item.data)

#creating nested fields as hyperlinked 
from .models import Category 
from .serializers import CategorySerializer

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk) 
    serialized_category = CategorySerializer(category) 
    return Response(serialized_category.data) 


@api_view(['GET','POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        #retrieve the category name
        category_name = request.query_perams.get('category')
        #retrieve the price name
        to_price = request.query_perams.get('to_price') 
        #retrive the search name
        search = request.query_perams.get('search') 
        #retrived the odring name
        ordering = request.query_perams.get('ordering')
        #filter by manu items name
        if category_name:
            items = items.filter(category__title=category_name)
            
        # filter by menu item price
        if to_price:
            items = items.filter(price__lte=to_price) 
            
        # filter by searching menu item name
        if search:
            items = items.filter(title__startswith=search) 
            
        # ordering
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(ordering_fields)
            
        serialized_item = MenuItemSerializer(items, many=True, context={'request':request})
        return Response(serialized_item.data) 
    
    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data) 
        serialized_item.is_valid(raise_exception=True) 
        serialized_item.save() 
        return Response(serialized_item.validated_data, status.HTTP_201_CREATED)
    
@api_view()
def single_menuItem(request, id):
    item = get_object_or_404(MenuItem, pk = id) 
    serialized_item = MenuItemSerializer(item) 
    return Response(serialized_item.data)