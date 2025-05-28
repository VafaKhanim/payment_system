from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
import requests
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from .models import Payment, Card
from .serializers import PaymentCreateSerializer, CardDataSerializer, PaymentSerializer
from .utils.validation import CardValidator


def send_callback(payment, status_, message):
    try:
        callback_data = {
            'payment_id': str(payment.payment_id),
            'status': status_,
            'amount': str(payment.amount),
            'message': message
        }
        response = requests.post(payment.callback_url, json=callback_data, timeout=30)
        print(f"Callback sent to {payment.callback_url}, Response: {response.status_code}")
    except requests.RequestException as e:
        print(f"Callback failed: {e}")


def find_card(card_data):
    try:
        for card in Card.objects.all():
            decrypted_data = card.get_decrypted_data()
            if (
                decrypted_data['card_number'] == card_data['card_number'] and
                decrypted_data['card_holder'].lower() == card_data['card_holder'].lower() and
                decrypted_data['expiry_date'] == card_data['expiry_date'] and
                decrypted_data['cvv'] == card_data['cvv']
            ):
                return card
        return None
    except Exception:
        return None


class PaymentViewSet(ViewSet):
    # /payments/ POST - create payment
    def create(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment = Payment.objects.create(
                amount=serializer.validated_data['amount'],
                callback_url=serializer.validated_data['callback_url']
            )
            payment_page_url = request.build_absolute_uri(
                reverse('payment_page', kwargs={'payment_id': payment.payment_id})
            )
            return Response({
                'payment_id': str(payment.payment_id),
                'payment_url': payment_page_url,
                'status': 'pending'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # /payments/<payment_id>/ GET - payment details
    def retrieve(self, request, pk=None):
        payment = get_object_or_404(Payment, payment_id=pk)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data)


class PaymentProcessView(APIView):
    # /payments/<payment_id>/process/ POST - card data to process payment
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request, payment_id):
        payment = get_object_or_404(Payment, payment_id=payment_id)

        if payment.status != 'pending':
            return Response({
                'status': 'error',
                'message': 'Payment already processed'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = CardDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'failed',
                'message': 'Invalid card data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        card_data = serializer.validated_data

        try:
            card = find_card(card_data)
            if not card:
                raise ValueError("Invalid card details")

            if card.balance < payment.amount:
                raise ValueError("Insufficient funds")

            card.balance -= payment.amount
            card.save()

            payment.status = 'success'
            payment.card = card
            payment.save()

            send_callback(payment, 'success', 'Payment successful')

            return Response({
                'status': 'success',
                'message': 'Payment successful'
            })

        except Exception as e:
            payment.status = 'failed'
            payment.error_message = str(e)
            payment.save()
            send_callback(payment, 'failed', str(e))
            return Response({
                'status': 'error',
                'message': 'Payment processing failed',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


def payment_page(request, payment_id):
    payment = get_object_or_404(Payment, payment_id=payment_id)

    if payment.status != 'pending':
        return HttpResponse('Bu payment artıq emal olunub')

    if request.method == 'POST':
        card_data = {
            'card_number': request.POST.get('card_number', '').strip(),
            'card_holder': request.POST.get('card_holder', '').strip(),
            'expiry_date': request.POST.get('expiry_date', '').strip(),
            'cvv': request.POST.get('cvv', '').strip()
        }

        is_valid, errors = CardValidator.validate_card_data(card_data)
        if not is_valid:
            messages.error(request, ' | '.join(errors.values()))
            return render(request, 'payment/payment_form.html', {'payment': payment})

        try:
            card = find_card(card_data)
            if not card:
                raise ValueError("Invalid card details")

            if card.balance < payment.amount:
                raise ValueError("Insufficient funds")

            card.balance -= payment.amount
            card.save()

            payment.status = 'success'
            payment.card = card
            payment.save()

            send_callback(payment, 'success', 'Payment successful')
            messages.success(request, 'Payment successful!')

        except Exception as e:
            payment.status = 'failed'
            payment.error_message = str(e)
            payment.save()
            send_callback(payment, 'failed', str(e))
            messages.error(request, str(e))

    return render(request, 'payment/payment_form.html', {'payment': payment})

