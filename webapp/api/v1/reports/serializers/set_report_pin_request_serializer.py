from rest_framework import serializers


class SetReportPinRequestSerializer(serializers.Serializer):
    pin = serializers.CharField(required=True)

    class Meta:
        fields = ["pin"]
        write_only_fields = ["pin"]
