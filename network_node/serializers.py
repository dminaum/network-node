from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    hierarchy_level = serializers.ReadOnlyField()

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ("debt", "created_at")

    def update(self, instance, validated_data):
        """Запрет обновления поля debt через API"""
        validated_data.pop("debt", None)
        return super().update(instance, validated_data)
