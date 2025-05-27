# apps/listings/serializers.py
from rest_framework import serializers
from .models import Property, Offer

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('owner', 'created_at', 'updated_at')

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ('buyer', 'created_at', 'updated_at')