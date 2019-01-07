from rest_framework import serializers
from apps.models import android,iOS,UWP
from member_portal.templatetags.encryption import encode,decode


class androidSerializer(serializers.ModelSerializer):
    # appURL = serializers.CharField(source='app_url')
    # publisherURL = serializers.CharField(source='pub_url')
    # icon = serializers.CharField(source='cover')
    def to_representation(self, android):
        return {
            'id': encode(android.id),
            'title': android.title,
            'appURL': android.app_url,
            'publisher': android.publisher,
            'publisherURL': android.pub_url,
            'icon': android.cover,
            'price': android.price,
        }
    # class Meta:
    #     model = android
    #     fields = ('id','title','appURL','publisher','publisherURL','icon','price',)
    #     # read_only_fields = ('id','title','appURL','publisher','publisherURL','icon','price',)

class iOSSerializer(serializers.ModelSerializer):
    def to_representation(self, iOS):
        return {
            'id': encode(iOS.id),
            'title': iOS.title,
            'appURL': iOS.app_url,
            'publisher': iOS.publisher,
            'publisherURL': iOS.publisher_url,
            'icon': iOS.cover,
            'price': iOS.price,
            'appID': iOS.appid,
            'devices': iOS.devices,
        }

class UWPSerializer(serializers.ModelSerializer):
    def to_representation(self, UWP):
        return {
            'id': encode(UWP.id),
            'title': UWP.title,
            'appURL': UWP.app_url,
            'publisher': UWP.publisher,
            'publisherURL': '',
            'icon': UWP.cover,
            'price': UWP.price,
            'appID': UWP.appid,
        }