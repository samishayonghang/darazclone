from django.urls import path,include
from daraz.api import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()

router.register('users', views.UserViewSet, basename='user')
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('products', views.ProductViewSet, basename='product')
router.register('carts', views.CartViewSet, basename='cart')
router.register('orders', views.OrderplacedViewSet, basename='orderplaced')

urlpatterns = [
    path('', include(router.urls)),
]



