# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'is_staff', 'is_superuser')


class SearchSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    result = serializers.ListField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
