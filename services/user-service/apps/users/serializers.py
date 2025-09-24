from .models import CustomUser

from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('id', 'mail', 'first_name', 'last_name',
                  'middle_name', 'address', 'phone', 'is_active')

class UserRegistrationsSerializers(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True, min_length = 8)
    password_confirm = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ('id', 'mail', 'first_name', 'last_name', 'password',
                  'password_confirm', 'address', 'phone')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return attrs
    
    def validate_mail(self, attr):
        if CustomUser.objects.filter(mail=attr).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return attr
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=False, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ('id', 'mail', 'first_name', 'last_name', 'middle_name',
                  'address', 'phone', 'is_active', 'password', 'password_confirm')
        read_only_fields = ('id', 'is_active')

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password or password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError("Пароли не совпадают.")
            try:
                validate_password(password, self.instance)
            except exceptions.ValidationError as e:
                raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

    def validate_mail(self, value):
        qs = CustomUser.objects.filter(mail=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirm', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance