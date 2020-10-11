from django.urls import include, path
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet
from django.urls import path



router = DefaultRouter()
router.register(r"products", ProductViewSet)
# router.register(r"admin-view/products", AdminProductViewSet)
# 


urlpatterns = [

    path("", include(router.urls)),
    
]
