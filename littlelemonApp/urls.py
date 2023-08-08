from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('categories/', views.CategoriesView.as_view()),
    path('menu-items/', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()), 
    path('cart/', views.CartView.as_view()), 
    path("cart/menu-items", views.CartView.as_view()), 
    path('order/', views.OrderView.as_view()), 
    path('orders/<int:pk>', views.SingleMenuItemView.as_view()), 
    
    path("groups/manager/users", views.GroupViewSet.as_view(
        {'get': 'list', 'post': 'create','delete':'destroy'})),
    
    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'})),
]
    
    
    
    
    
    
#     path('', views.home, name='home'),
#     path('about/', views.about, name='about'),
#     path('menu/', views.menu, name = 'menu'),
#     path('book/', views.book, name='booking'),
#     path('booking_list/', views.booking_list, name='booking_list'), 
#     path('menu_item/<int:pk>/', views.display_menu_item, name='menu_items'), 
    
#     #API for booking 
#     path('books/', views.books, name='books'),
#     path('menu-items/', views.MenuItemViews.as_view()),
#     path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    
#     # path('menu-restapi/', views.menu_restApi),
#     # path('menu-restapi/<int:id>', views.single_item_rest),
    
#     # path('category/<int:pk>',views.category_detail, name='category-detail'), 
#     # path('menu-nested/', views.menu_items),
#     # path('menu-nested/<int:id>', views.single_menuItem),
#     path('secret/', views.secret),
#     path('api-token-auth/', obtain_auth_token),
#     path('manager-view/', views.manager_view),
#     path('throttle-check', views.throttle_check),
#     path('throttle-check-auth/', views.throttle_check_auth),
# ]