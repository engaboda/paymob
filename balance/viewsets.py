from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import PromoCode, Product, PromoHistory, Transaction
from django.shortcuts import get_object_or_404
import logging
from django.db.models import Sum
from django.utils.translation import gettext as _, get_language, activate
from rest_framework.permissions import IsAuthenticated


# Get an instance of a logger
logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def redeem(request):

    cur_language = get_language()

    code = request.data.get('code')
    product_id = request.data.get('product')

    logger.info("[{}] Start buying products: {} under promo code: {}".format(request.user.email, product_id, code))

    promo_code = get_object_or_404(PromoCode, code=code)
    products = Product.objects.filter(id__in=product_id, category=promo_code.category)
    freq_of_use = request.user.user_promo_code_history.filter(promo_code=promo_code).count()

    logger.info("[{}] still having remain quantity form his promo_code: {}".format(request.user.email, code))
    if not promo_code.is_expired and products.count() == promo_code.quantity and promo_code.frequency_of_use > freq_of_use:
        sum_price = products.aggregate(Sum('price'))['price__sum']
        for product in products:
            PromoHistory.objects.create(user=request.user, promo_code=promo_code, prodcut=product)

        Transaction.objects.create(user=request.user, amount=sum_price - promo_code.benefit)
        activate(cur_language)
        return Response({'statu': _('Done')})

    if promo_code.frequency_of_use == freq_of_use:
        logger.info("[{}] this user try to use promo_code while he exceed his usage: {}".format(request.user, freq_of_use))
    elif products.count() != promo_code.quantity:
        logger.info("[{}] this user try to use promo_code with less than configured quantity".format(request.user))
    else:
        logger.info("[{}] this user try to use promo_code while its expired".format(request.user))

    return Response(status=status.HTTP_400_BAD_REQUEST)
