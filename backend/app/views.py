from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from .models import Product
from .serializers import (
    ProductSerializer,
    CommentSerializer,
    ProductRatingWithCommentsSerializer,
)


@extend_schema(tags=["Products"])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @extend_schema(
        summary="Получить средний рейтинг и комментарии продукта",
        description="Возвращает средний рейтинг и список комментариев для продукта.",
        request=ProductRatingWithCommentsSerializer,
        responses={
            200: OpenApiResponse(
                response=ProductRatingWithCommentsSerializer,
                description="Успешный ответ"
            ),
            404: OpenApiResponse(description="Product not found"),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"product_id": 1},
                request_only=True,
            ),
            OpenApiExample(
                "Пример ответа",
                value={
                    "average_rating": 4.5,
                    "comments": [
                        {"id": 1, "product": 1, "text": "Отличный товар!"},
                        {"id": 2, "product": 1, "text": "Нормально"},
                    ],
                },
                response_only=True,
            ),
        ],
    )
    @action(detail=True, methods=["post"])
    def rating_info(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        avg = product.ratings.aggregate(avg=Avg("value"))["avg"] or 0
        comments = product.comments.all()

        data = {
            "average_rating": avg,
            "comments": CommentSerializer(comments, many=True).data,
        }

        return Response(data, status=status.HTTP_200_OK)
