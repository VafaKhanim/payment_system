from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('payments/<uuid:payment_id>/process/', views.PaymentProcessView.as_view(), name='payment_process'),
    path('payments/<uuid:payment_id>/page/', views.payment_page, name='payment_page'),
]