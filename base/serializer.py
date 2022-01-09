from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Invoice

# Serializer to validate the data for entry as well as to serialize the data for sending to user

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        # fields = '__all__'
        exclude = ['_id']
    