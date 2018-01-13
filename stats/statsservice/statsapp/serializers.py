from rest_framework import serializers
from statsapp.models import RequestInfo


class RequestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestInfo
        fields = ('guid', 'uri', 'method', 'params','status', 'errors')
