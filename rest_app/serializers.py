from pyexpat import model
from rest_framework import serializers
from .models import *

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Movies
        fields = "__all__"

class RrsevationSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Reservation
        fields = "__all__"        
        
class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Guest
        fields = ["pk","reserved","name","mobile"]        
             
                
        