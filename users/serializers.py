from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Address, Security


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'address_1',
            'address_2',
            'country',
            'state',
            'city',
            'zip'
        ]


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'has_other_names',
            'other_name',
            'username',
            'email',
            'gender',
            'phone',
            'addresses'
        ]

    def create(self, validated_data):
        addresses = validated_data.pop('addresses')
        user = super().create(validated_data)
        for address in addresses:
            address['user'] = user
            form = AddressSerializer(data=address)
            if form.is_valid():
                form.validated_data['user_id'] = user.id
                user.addresses.add(
                    form.save()
                )
        return user

    def save(self):
        user = super().save()
        user.create_all_related_blocks()
        return user