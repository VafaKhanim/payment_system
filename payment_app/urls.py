from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/payment/<uuid:payment_id>/process/', views.PaymentProcessView.as_view(), name='process_payment'),
    path('payment/<uuid:payment_id>/', views.payment_page, name='payment_page'),
]