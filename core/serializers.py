from rest_framework import serializers


class TimeStampedSerializer(serializers.Serializer):
    """Serializer base para campos de timestamp"""
    creado_en = serializers.DateTimeField(read_only=True)
    actualizado_en = serializers.DateTimeField(read_only=True)