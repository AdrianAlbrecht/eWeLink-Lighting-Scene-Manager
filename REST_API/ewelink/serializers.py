from rest_framework import serializers
from .models import Scene, Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'type']
        read_only_fields = ['id', 'name', 'type']

class SceneSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if ' ' in value:
            raise serializers.ValidationError("The name cannot contain spaces.")
        return value
    
    class Meta:
        model = Scene
        fields = ['id', 'name', 'device', 'statuses']
        read_only_fields = ['id']    