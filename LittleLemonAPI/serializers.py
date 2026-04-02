from rest_framework import serializers 
from .models import MenuItem, Cart, Order, OrderItem, Category
from rest_framework.validators import UniqueTogetherValidator 
from django.contrib.auth.models import User 
 
class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer (serializers.ModelSerializer): 
    
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']
        
        extra_kwargs = {
            'price': {'min_value': 0, 'max_value':100},
        }

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'status', 'total', 'date', 'user', 'delivery_crew', 'items']

    def get_items(self, obj):
        items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(items, many=True).data