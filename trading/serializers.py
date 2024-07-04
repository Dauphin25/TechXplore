from rest_framework import serializers
from .models import Trader, Company, Buy, Sell

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'  # or specify fields explicitly

class TraderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')  # Assuming 'user' is a ForeignKey to Django User model

    class Meta:
        model = Trader
        fields = '__all__'

class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = '__all__'

class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'
