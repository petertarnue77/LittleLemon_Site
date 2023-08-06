from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name = 'menu'),
    path('book/', views.book, name='booking'),
    path('booking_list/', views.booking_list, name='booking_list'), 
    path('menu_item/<int:pk>/', views.display_menu_item, name='menu_items'), 
    
    #API for booking 
    path('books/', views.books, name='books'),
    path('menu-items/', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItem.as_view()), 
    
    path('menu-restapi/', views.menu_restApi),
    path('menu-restapi/<int:id>', views.single_item_rest),
    
    path('category/<int:pk>',views.category_detail, name='category-detail'), 
    path('menu-nested/', views.menu_items),
    path('menu-nested/<int:id>', views.single_menuItem)
]