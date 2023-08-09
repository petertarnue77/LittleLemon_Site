from django.shortcuts import render 
from rest_framework import generics  
from rest_framework.response import Response 

from django.shortcuts import get_object_or_404 
from django.contrib.auth.models import Group, User

from .models import Category, MenuItem, Cart, Order, OrderItem, Rating
from .serializers import CartSerializer, MenuItemSerializer, OrderSerializer, UserSerializer, CategorySerializer
#Import Authentication classes
from rest_framework.permissions import IsAuthenticated 
from rest_framework.permissions import IsAdminUser

# class based view with viewsets class
from rest_framework import viewsets 
from rest_framework import status  

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer 
    
    def get_permissions(self):
        permission_classes = [] 
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated] 
        return [permission() for permission in permission_classes]


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer 
    search_fields = ['category__title'] 
    ordering_fields =['price','title']  
    
    def get_permissions(self):
        permission_classes = [] 
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer 
    
    def get_permissions(self): 
        permission_classes = [] 
        if self.request.method != 'GET': 
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CartView(generics.ListCreateAPIView): 
    queryset = Cart.objects.all() 
    serializer_class = CartSerializer 
    
    def get_queryset(self): 
        return Cart.objects.all().filter(user=self.request.user) 
    
    def delete(self, request, *args, **kwargs):
        Cart.objects.all().filter(user=self.request.user).delete() 
        return Response('Ok')


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all() 
    serializer_class = OrderSerializer 
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self): 
        if self.request.user.is_superuser: 
            return Order.objects.all() 
        #Normal Customer. belongs to no groups
        elif self.request.user.groups.count()==0: 
            return Order.objects.all().filter(user=self.request.user)
        # delivery crew 
        elif self.request.user.groups.filter(name='Delivery Crew').exists(): 
            return Order.objects.all().filter(delivery_crew=self.request.user)
        else: 
            # delivery crew or Manager
            return Order.objects.all() 
        
    def create(self, request, *args, **kwargs): 
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count() 
        if menuitem_count == 0: 
            return Response({'Message': 'No item in cart'}) 
        
        data = request.data.copy() 
        total = self.get_total_price(self.request.user) 
        data['total'] = total 
        data['user'] = self.request.user.id 
        order_serializer = OrderSerializer(data=data) 
        
        if (order_serializer.is_valid()): 
            order = order_serializer.save() 
            
            items = Cart.objects.all().filter(user=self.request.user).all() 
            for item in items.values(): 
                orderitem = OrderItem(
                    order = order,
                    menuitem_id = item['menuitem_id'],
                    price = item['price'],
                    quantity = item['quantity'],
                ) 
            # delete cart items
            Cart.objects.al().filter(user=self.request.user).delete()
            
            result = order_serializer.data.copy() 
            result['total'] = total 
            return Response(order_serializer.data) 
        
class SingleOrderView(generics.RetrieveUpdateAPIView): 
    queryset = Order.objects.all() 
    serializer_class = OrderSerializer  
    permission_classes = [IsAuthenticated] 
    
    def update(self, request, *args, **kwargs): 
        #Normal user, not belonging to any group = Customer
        if self.request.user.groups.count() == 0: 
            return Response('Not Ok')
        #everyone else - Super Admin, Manager and Delivery Crew
        else:
            return super().update(request, *args, **kwargs) 
        

class GroupViewSet(viewsets.ViewSet): 
    permission_classes = [IsAuthenticated] 
    
    def list(self, request): 
        users = User.objects.all().filter(groups__name='Manager') 
        items = UserSerializer(users, many=True) 
        return Response(items.data) 
    
    def create(self,request): 
        user = get_object_or_404(User, username=request.data['username']) 
        managers = Group.objects.get(name='Manager') 
        managers.user_set.add(user) 
        return Response({"Message": "User added to the Manager group"}, 200) 
    
    def destroy(self, request): 
        user = get_object_or_404(User, username=request.data['username']) 
        managers = Group.objects.get(name="Manager") 
        managers.user_set.remove(user) 
        return Response({"Message": "User removed from the Manager group"},200)


class DeliveryCrewView(viewsets.ViewSet): 
    permission_classes = [IsAuthenticated] 
    
    def list(self, request): 
        users = User.objects.all().filter(groups__name='Delivery Crew') 
        items = UserSerializer(users,many=True) 
        return Response(items.data)

    def create(self, request): 
        # only for super admin and manager
        if self.request.user.is_superuser == False: 
            if self.request.user.groups.filter(name="Manger").exists() == False: 
                return Response({"Message": "forbidden"}) 
        
        user = get_object_or_404(User,username=request.data['username']) 
        delivery_crew = Group.objects.get(name="Delivery Crew") 
        delivery_crew.user_set.add(user) 
        return Response({'Message': "User added to the Delivery Crew group"}, 200) 
    
    def destroy(self, request): 
        # only for super admin and Managers 
        if self.request.user.is_superuser == False: 
            if self.request.user.groups.filter(name='Manager').exists() == False: 
                return Response({"Message": "forbidden"}, status.HTTP_403_FORBIDDEN) 
        
        user = get_object_or_404(User, username=request.data['username']) 
        delivery_crew = Group.objects.get(name="Delivery Crew") 
        delivery_crew.user_set.remove(user) 
        return Response({"Message": "User removed from the deliver crew group"}, 200)


# class RatingsView(generics.ListCreateAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer

#     def get_permissions(self):
#         if(self.request.method=='GET'):
#             return []
#         return [IsAuthenticated()]



# from django.http import HttpResponse, JsonResponse
# from django.db import IntegrityError 

# from django.views.decorators.csrf import csrf_exempt 
# from rest_framework.decorators import renderer_classes
# from django.forms.models import model_to_dict  
# from django.core.paginator import EmptyPage, Paginator 
# from rest_framework import viewsets

# from rest_framework import generics 
# from rest_framework.decorators import api_view, throttle_classes
# from rest_framework.response import Response 
# from rest_framework import status

# from .models import MenuItem, Category, Booking
# from .forms import BookingForm  
# from .serializers import MenuItemSerializer , CategorySerializer  

# from rest_framework.throttling import AnonRateThrottle 
# from rest_framework.throttling import UserRateThrottle  
# from .throttles import TenCallsPerMinutes


# # Create your views here. 
# def home(request):
#     return render(request, 'index_home.html')


# def about(request):
#     return render(request, 'about.html')


# def book(request):
#     booking = BookingForm()
#     if request.method == "POST":
#         booking = BookingForm(request.POST)
#         if booking.is_valid():
#             booking.save() 
#     booked = {'booking': booking}
#     return render(request, 'book.html',booked)


# # Add your code here to create new views 
# def menu(request):
#     menu_data = MenuItem.objects.all() 
#     menu_content = {'menu_data': menu_data} 
#     return render(request, 'menu.html', menu_content)


# def display_menu_item(request, pk=None):
#     if pk:
#         menu_item = MenuItem.objects.get(pk=pk)
#     else:
#         menu_item = ""
#     return render(request, 'menu_item.html', {"menu_item": menu_item}) 
 

# def booking_list(request):
#     booking_items = Booking.objects.all() 
#     bookingitems = {'booking_items': booking_items} 
#     return render(request, 'bookingItems.html', bookingitems) 

# # API booking 
# @csrf_exempt 
# @api_view(['GET','POST'])
# def books(request):
#     if request.method == "GET": 
#         booking = Booking.objects.all().values() 
#         return Response({'booking': list(booking)}) 
     
#     elif request.method == 'POST':
#         first_name = request.POST.get('first_name') 
#         last_name = request.POST.get('last_name') 
#         booking_time = request.POST.get('booking_time') 
#         number_of_person = request.POST.get('number_of_person') 
#         notes = request.POST.get('notes') 
        
#         booking = Booking(
#             first_name = first_name,
#             last_name = last_name,
#             booking_time = booking_time,
#             number_of_person = number_of_person,
#             notes = notes
#         ) 
        
#         try: 
#             booking.save() 
#         except IntegrityError:
#             return Response({'error': 'true', 'message': 'required field missing'}, status=400)
        
#         return Response(model_to_dict(booking), status=201)        


# class CategoryView(generics.ListCreateAPIView):
#     queryset = Category.objects.all() 
#     serializer_class = CategorySerializer

    
# # class based menuItem View
# class MenuItemViews(generics.ListCreateAPIView): 
#     # impliment rate limiting or throttling
#     throttle_classes = [AnonRateThrottle, UserRateThrottle]
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#     ordering_fields = ['price', 'title']  
#     filterset_fields = ['price', 'title']
#     search_fields = ['title', 'category__title']

# # class based single menuItem with viewset class
# class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MenuItem.objects.all() 
#     serializer_class = MenuItemSerializer

# # Creating a nested relationship as detial
# @api_view(['POST', 'GET'])
# def menu_restApi(request):
#     items = MenuItem.objects.select_related('category').all() 
#     serializered_item = MenuItemSerializer(items, many=True) 
#     return Response(serializered_item.data) 


# from django.shortcuts import get_object_or_404
# @api_view(['POST','GET'])
# def single_item_rest(request, id):
#     items = get_object_or_404(MenuItem, pk=id) 
#     serialized_item = MenuItemSerializer(items) 
#     return Response(serialized_item.data)

# #creating nested fields as hyperlinked 
# from .models import Category 
# from .serializers import CategorySerializer

# @api_view()
# def category_detail(request, pk):
#     category = get_object_or_404(Category, pk=pk) 
#     serialized_category = CategorySerializer(category) 
#     return Response(serialized_category.data) 


# @api_view(['GET','POST'])
# def menu_items(request):
#     if request.method == 'GET':
#         items = MenuItem.objects.select_related('category').all()
#         #retrieve the category name
#         category_name = request.query_perams.get('category')
#         #retrieve the price name
#         to_price = request.query_perams.get('to_price') 
#         #retrive the search name
#         search = request.query_perams.get('search') 
#         #retrived the odring name
#         ordering = request.query_perams.get('ordering') 
#         # pagination
#         perpage = request.query_perams.get('perpage', default=2) 
#         page = request.query_perams.get('page', default=1)
#         #filter by manu items name
#         if category_name:
#             items = items.filter(category__title=category_name)
            
#         # filter by menu item price
#         if to_price:
#             items = items.filter(price__lte=to_price) 
            
#         # filter by searching menu item name
#         if search:
#             items = items.filter(title__startswith=search) 
            
#         # ordering
#         if ordering:
#             ordering_fields = ordering.split(',')
#             items = items.order_by(ordering_fields)
        
#         #perform pagination   
#         paginator = Paginator(items, per_page=perpage) 
#         try:
#             items = paginator.page(number=page) 
#         except EmptyPage:
#             items = []
            
#         serialized_item = MenuItemSerializer(items, many=True, context={'request':request})
#         return Response(serialized_item.data) 
    
#     elif request.method == 'POST':
#         serialized_item = MenuItemSerializer(data=request.data) 
#         serialized_item.is_valid(raise_exception=True) 
#         serialized_item.save() 
#         return Response(serialized_item.validated_data, status.HTTP_201_CREATED)
    
# @api_view()
# def single_menuItem(request, id):
#     item = get_object_or_404(MenuItem, pk = id) 
#     serialized_item = MenuItemSerializer(item) 
#     return Response(serialized_item.data)  


# from rest_framework.permissions import IsAuthenticated 
# from rest_framework.decorators import permission_classes

# @api_view() 
# @permission_classes([IsAuthenticated])
# def secret(request):
#     return Response({'message':'secret message'}) 

# # function base authentication
# @api_view()
# @permission_classes([IsAuthenticated]) 
# def manager_view(request): 
#     if request.user.groups.filter(name='Manager').exists():
#         return Response({'message': 'Only Manager should see this site'}) 
#     elif request.user.groups.filter(name='Staff').exists():
#         return Response({'message': 'You are one of the staff members'})
#     else:
#         return Response({'message': 'You are not authorized'}, 403) 
    
# # throttle or rate limiting for anonymous user
# @api_view()
# @throttle_classes([AnonRateThrottle])
# def throttle_check(request):
#     return Response({'message': 'successful'}) 


# # throttle or rate limiting for anonymous user
# @api_view()
# @permission_classes([IsAuthenticated])
# @throttle_classes([TenCallsPerMinutes]) 
# def throttle_check_auth(request):
#     return Response({'message':'Message for log in users only'})