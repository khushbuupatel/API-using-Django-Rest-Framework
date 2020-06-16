from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'analysis', views.AnalysisView, basename='Analysis')
router.register(r'products', views.ProductView, basename='Products')


urlpatterns = [
    path('', include(router.urls))
]