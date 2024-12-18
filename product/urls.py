from django.urls import path

from .views import ProductCreateView, UserProductListView, ProductDeleteView, ProductDetailView, ProductUpdateView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('view/', UserProductListView.as_view(), name='user-products'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # New route for viewing a product by ID
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),  # URL for updating product

]
