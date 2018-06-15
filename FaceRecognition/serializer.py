from rest_framework import serializers
from FaceRecognition.models import FaceCharacteristic


class FaceCharacteristicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FaceCharacteristic
        fields = ('id', 'union_id', 'characteristic_value')
