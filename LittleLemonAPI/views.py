from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsManager
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework import status
from django.utils import timezone


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'title']
    filterset_fields = ['price', 'title']
    search_fields = ['title']
    def get_permissions(self):
        if(self.request.method=='GET'):
            return [IsAuthenticated()]
        return [IsManager()]
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        # Anyone authenticated can GET
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        # Only manager can update
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsManager()]
        return []

class ManagerUsersView(APIView):
    permission_classes = [IsManager]
    def get(self, request):
        try:
            group = Group.objects.get(name='Manager')
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=404)
        users = group.user_set.all()
        data = users.values('id', 'username', 'email')
        return Response(data, status=status.HTTP_200_OK)
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        group = Group.objects.get(name='Manager')
        group.user_set.add(user)
        return Response({"message": "User added to Manager group"}, status=status.HTTP_201_CREATED)
 
class ManagerUserDetailView(APIView):
    permission_classes = [IsManager]
    def get(self, request, userId):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        return Response(data, status=status.HTTP_200_OK)
    
    def delete(self, request, userId):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            group = Group.objects.get(name='Manager')
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        group.user_set.remove(user)
        return Response({"message": "User removed from Manager group"}, status=status.HTTP_200_OK)

class DeliveryCrewUsersView(APIView):
    permission_classes = [IsManager]
    def get(self, request):
        try:
            group = Group.objects.get(name='Delivery Crew')
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=404)
        users = group.user_set.all()
        data = users.values('id', 'username', 'email')
        return Response(data, status=status.HTTP_200_OK)
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        group = Group.objects.get(name='Delivery Crew')
        group.user_set.add(user)
        return Response({"message": "User added to Delivery Crew group"}, status=status.HTTP_201_CREATED)    
class DeliveryCrewUserDetailView(APIView):
    permission_classes = [IsManager]
    def delete(self, request, userId):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            group = Group.objects.get(name='Delivery Crew')
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        group.user_set.remove(user)
        return Response({"message": "User removed from Delivery Crew group"}, status=status.HTTP_200_OK)
    
class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        menuitem_id = request.data.get('menuitem')
        quantity = request.data.get('quantity')
        # Validate menu item
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=404)
        # Create cart item
        cart_item = Cart.objects.create(
            user=request.user,
            menuitem=menuitem,
            quantity=quantity,
            unit_price=menuitem.price,
            price=menuitem.price * int(quantity)
        )
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)

# Custom permission check
def user_is_manager(user):
    return user.groups.filter(name='Manager').exists()

def user_is_delivery_crew(user):
    return user.groups.filter(name='Delivery Crew').exists() 

# Order View:   
class OrderView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    filterset_fields = ['status', 'date', 'user', 'delivery_crew']
    ordering_fields = ['status', 'date', 'user', 'delivery_crew']

    def post(self, request):
        user = request.user
        # Get cart items
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Calculate total
        total = sum(item.price for item in cart_items)
        # Create order
        order = Order.objects.create(
            user=user,
            total=total,
            date=timezone.now().date()
        )
        #  Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
        # Step 5: Clear cart
        cart_items.delete()
        # Step 6: Return response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        user = self.request.user
      
        # Manager sees all orders
        if user_is_manager(user):
            orders = Order.objects.all()
        # Delivery crew sees only orders assigned to them
        elif user_is_delivery_crew(user):
            orders = Order.objects.filter(delivery_crew=user)
        # Customer sees only their own orders
        else:
            orders = Order.objects.filter(user=user)
        return orders
    

# Order Details View:
class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, orderId):
        user = request.user
        # Check if order exists
        try:
            order = Order.objects.get(id=orderId)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if order belongs to current user
        if order.user != user:
            return Response({"error": "You are not allowed to view this order"},
                            status=status.HTTP_403_FORBIDDEN)

        # Get order items
        order_items = OrderItem.objects.filter(order=order)
        order_serializer = OrderSerializer(order)
        items_serializer = OrderItemSerializer(order_items, many=True)

        # Return combined response
        data = {
            "order": order_serializer.data,
            # "items": items_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    # ---------------- PATCH ----------------
    def patch(self, request, orderId):
        return self._update_order(request, orderId, partial=True)

    # ---------------- PUT ----------------
    def put(self, request, orderId):
        return self._update_order(request, orderId, partial=False)

    # ---------------- Shared logic ----------------
    def _update_order(self, request, orderId, partial):
        try:
            order = Order.objects.get(id=orderId)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        user = request.user
        data = request.data

        # -------- Manager --------
        if user_is_manager(user):
            # PUT expects full data
            if not partial:
                if "status" not in data or "delivery_crew" not in data:
                    return Response(
                        {"error": "status and delivery_crew are required for PUT"},
                        status=400
                    )

            # Update status
            if "status" in data:
                order.status = bool(int(data["status"]))

            # Update delivery crew
            if "delivery_crew" in data:
                try:
                    crew = User.objects.get(id=data["delivery_crew"])
                    if not user_is_delivery_crew(crew):
                        return Response({"error": "User is not delivery crew"}, status=400)
                    order.delivery_crew = crew
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=404)

            order.save()
            return Response(OrderSerializer(order).data, status=200)

        # -------- Delivery Crew --------
        elif user_is_delivery_crew(user):
            if order.delivery_crew != user:
                return Response({"error": "Not assigned to this order"}, status=403)

            if "status" not in data:
                return Response({"error": "status is required"}, status=400)

            order.status = bool(int(data["status"]))
            order.save()

            return Response(OrderSerializer(order).data, status=200)

        # -------- Others --------
        return Response({"error": "Not allowed"}, status=403)
    
    def delete(self, request, orderId):
        try:
            order = Order.objects.get(id=orderId)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)
        # Only Manager can delete
        if not user_is_manager(request.user):
            return Response({"error": "Not allowed"}, status=403)
        order.delete()
        return Response({"message": "Order deleted"}, status=200)
 
    
