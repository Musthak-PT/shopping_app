from rest_framework import serializers
from django.contrib.auth.models import User
from shop.models import Product, Order
from rest_framework import serializers
from django.contrib.auth.models import User
from shop.models import Product, Order
from django.contrib.auth.hashers import make_password, check_password

#--------Start Customer registeration----------
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    username           = serializers.CharField(required=True)
    password            = serializers.CharField(required=True)
    confirm_password    = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username','password', 'confirm_password', ]
        
    def validate(self, attrs):
     
        username               = attrs.get('username')
        password            = attrs.get('password')
        confirm_password    = attrs.get('confirm_password')
        instance_id         = attrs.get('instance_id')
        
        if not instance_id:
            if username and User.objects.filter(username=username).exists():
                raise serializers.ValidationError({"error": ['Sorry, that user name is already in exists!']})
            if password != confirm_password:
                raise serializers.ValidationError({"error": ['Sorry, Password do not match!']})
            return super().validate(attrs)
    
    def create(self, validated_data):
        request               = self.context.get('request')
        instance              = User()
        instance.username    = validated_data.get('username', None)
        password              = validated_data.get('password', None)
        confirm_password      = validated_data.get('confirm_password', None)
        
        if password == confirm_password:
            instance.password = make_password(password)
            
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'