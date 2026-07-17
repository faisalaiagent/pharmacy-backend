from rest_framework import serializers

from products.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()

    class Meta:
        model = Review

        fields = (
            "id",
            "user",
            "rating",
            "title",
            "comment",
            "is_verified_purchase",
            "created_at",
        )