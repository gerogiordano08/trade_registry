from rest_framework import serializers

class TickerSearchSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    name = serializers.CharField()