from rest_framework import serializers


class PasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
