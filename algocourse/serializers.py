from rest_framework import serializers


class KnoxSerializer(serializers.Serializer):
    token = serializers.CharField()
