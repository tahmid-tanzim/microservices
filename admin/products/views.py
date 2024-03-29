import random
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User
from .serializers import ProductSerializer
from.producer import publish


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish("PRODUCT_CREATED", serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"message": "Sorry! Product DoesNotExist"}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(instance=product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            publish("PRODUCT_UPDATED", serializer.data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Product.DoesNotExist:
            return Response({"message": "Sorry! Product DoesNotExist"}, status=status.HTTP_404_NOT_FOUND)

    def remove(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            publish("PRODUCT_DELETED", {"id": pk})
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"message": "Sorry! Product DoesNotExist"}, status=status.HTTP_404_NOT_FOUND)


class UserAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })
