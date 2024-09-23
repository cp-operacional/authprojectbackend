from rest_framework import serializers
from .models import UserAccount


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        if 'avatar' not in validated_data or not validated_data['avatar']:
            validated_data.pop('avatar', None)
        user = UserAccount.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        avatar = validated_data.pop('avatar', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        if avatar:
            instance.avatar = avatar
        elif 'avatar' in self.initial_data:
            instance.avatar = None
        instance.save()
        return instance
