from rest_framework import serializers
from .models import Vuelo, Hotel
from django.contrib.auth.models import User

class SerializerUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

class SerializerVuelo(serializers.ModelSerializer):
    # Carrera = serializers.StringRelatedField(read_only=True)
    # Asesor = serializers.StringRelatedField(read_only=True)
    Usuario = SerializerUser()

    class Meta:
        model = Vuelo
        fields = '__all__'

class SerializerHotel(serializers.ModelSerializer):
    # Carrera = serializers.StringRelatedField(read_only=True)
    # Asesor = serializers.StringRelatedField(read_only=True)
    Usuario = SerializerUser()

    class Meta:
        model = Hotel
        fields = '__all__'