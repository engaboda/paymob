from rest_framework import serializers


class RedeemCode(serializers.Serializer):
    code = serializers.CharField(max_length=180)
    product = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = ('code', 'product')
