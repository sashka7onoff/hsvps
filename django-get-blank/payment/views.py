from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .models import PaymentTransaction
from yookassa import Configuration, Payment
import uuid


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


@login_required
def create_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('payment', '0')
        try:
            amount = float(amount)
        except ValueError:
            return redirect('balance')

        if amount <= 0:
            return redirect('balance')

        idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            'amount': {
                'value': amount,
                'currency': 'RUB',
            },
            'confirmation': {
                'type': 'redirect',
                'return_url': request.build_absolute_uri('/payment/success/'),
            },
            'capture': False,
            'description': f'Пополнение баланса в сервисе Get-blank (user: {request.user.login})',
        }, idempotence_key)

        payment_id = payment.id
        PaymentTransaction.objects.create(
            user=request.user,
            payment_id=payment_id,
            status='pending',
            amount=amount,
        )

        confirmation_url = payment.confirmation.confirmation_url
        return redirect(confirmation_url)

    return redirect('balance')


@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        event = data.get('event')
        if event == 'payment.waiting_for_capture':
            payment_id = data['object']['id']
            value = float(data['object']['amount']['value'])
            try:
                payment = Payment.capture(payment_id)
                if payment.status == 'succeeded':
                    transaction = PaymentTransaction.objects.get(payment_id=payment_id)
                    transaction.status = 'succeeded'
                    transaction.save()
                    user = transaction.user
                    user.balance += value
                    user.save()
            except PaymentTransaction.DoesNotExist:
                pass
        elif event == 'payment.succeeded':
            payment_id = data['object']['id']
            value = float(data['object']['amount']['value'])
            try:
                transaction = PaymentTransaction.objects.get(payment_id=payment_id)
                if transaction.status != 'succeeded':
                    transaction.status = 'succeeded'
                    transaction.save()
                    user = transaction.user
                    user.balance += value
                    user.save()
            except PaymentTransaction.DoesNotExist:
                pass
        elif event == 'payment.canceled':
            payment_id = data['object']['id']
            try:
                transaction = PaymentTransaction.objects.get(payment_id=payment_id)
                transaction.status = 'canceled'
                transaction.save()
            except PaymentTransaction.DoesNotExist:
                pass

        return HttpResponse(status=200)

    return HttpResponse(status=405)


@login_required
def payment_success(request):
    user = request.user
    from django.contrib import messages
    messages.success(request, 'Баланс успешно пополнен!' if True else '')
    return redirect('balance')
