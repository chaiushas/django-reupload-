from django.urls import path
from . import views
from .views import ProductDetailView

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('store/<int:pk>', ProductDetailView.as_view(), name="product_detail"),
    path('store/<int:pk>/update', views.ProductUserUpdateView.as_view(), name='product-update'),
    path('store/<int:pk>/delete', views.ProductUserDeleteView.as_view(), name='product-delete'),
    path('store/new', views.ProductUserCreateView.as_view(), name='product-new'),
    path('register/', views.register, name='register'),
    path('process_order/', views.processOrder, name="process_order"),
]