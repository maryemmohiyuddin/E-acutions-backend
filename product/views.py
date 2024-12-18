from rest_framework import generics, permissions
from .models import Product, Category
from .serializers import ProductSerializer, ProductUpdateSerializer
from categories.serializers import CategorySerializer
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from .permissions import IsOwner  # Import your custom permission

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create products
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication

    def perform_create(self, serializer):
        user = self.request.user  # Get the authenticated user
        if user.is_anonymous:
            raise ValidationError("User must be authenticated to create a product.")
        
        serializer.save(user=user)  # Save the product with the authenticated user

class UserProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]  # Add custom permission

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Product.objects.filter(user=user)
        else:
            print("User is not authenticated.")
            return Product.objects.none()  # Return an empty queryset

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwner]  # Add both IsAuthenticated and IsOwner permissions
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication

    def get_queryset(self):
        user = self.request.user
        # Ensure that the queryset only includes products owned by the authenticated user
        return Product.objects.filter(user=user)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can view products
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication

    def get_queryset(self):
        
        # user = self.request.user
        # Optionally, you can filter to show only products owned by the authenticated user
        return Product.objects.all()

    def get_object(self):
        """Override to get the object by 'id'."""
        obj = super().get_object()
        if obj is None:
            raise ValidationError("Product not found.")
        return obj

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]  # Only authenticated users and owners can update
    authentication_classes = [JWTAuthentication]  # Use JWT Authentication

    def get_object(self):
        # Get the product by the 'id' passed in the URL
        obj = super().get_object()
        if obj is None:
            raise ValidationError("Product not found.")
        return obj

    def update(self, request, *args, **kwargs):
        # Allow partial updates by setting `partial=True`
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()  # Save with updated fields only
