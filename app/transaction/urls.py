from django.urls import path, include
from rest_framework.routers import DefaultRouter
from transaction import views


router = DefaultRouter()
router.register('list', views.TransactionViewSet, basename='list')
router.register('create', views.TransactionCreateViewSet, basename='create')
router.register(
    'breakdown',
    views.TransactionBreakdownViewSet,
    basename='breakdown'
)

app_name = 'transaction'


urlpatterns = [
    path('', include(router.urls)),
]
