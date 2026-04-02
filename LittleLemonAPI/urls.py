from django.urls import path 
from . import views 
  
urlpatterns = [ 
    path('menu-items/', views.MenuItemView.as_view()), 
    path('menu-items/<int:pk>/', views.SingleMenuItemView.as_view()),

    path('groups/manager/users', views.ManagerUsersView.as_view()),
    path('groups/manager/users/<int:userId>', views.ManagerUserDetailView.as_view()),
    path('groups/delivery-crew/users', views.DeliveryCrewUsersView.as_view()),
    path('groups/delivery-crew/users/<int:userId>', views.DeliveryCrewUserDetailView.as_view()),

    path('cart/menu-items', views.CartView.as_view()),

    path('orders', views.OrderView.as_view()),
    path('orders/<int:orderId>', views.OrderDetailView.as_view()),
] 