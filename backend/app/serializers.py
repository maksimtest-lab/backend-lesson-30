from rest_framework import serializers
from .models import Product, Rating, Comment


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class ProductRatingWithCommentsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    average_rating = serializers.FloatField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def validate_product_id(self, value):
        from .models import Product
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product not found")
        return value

    def create(self, validated_data):
        from .models import Product
        product = Product.objects.get(id=validated_data["product_id"])

        avg = product.ratings.aggregate(avg=models.Avg("value"))["avg"] or 0
        comments = product.comments.all()

        return {
            "average_rating": avg,
            "comments": comments
        }
