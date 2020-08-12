from rest_framework.test import APITestCase
from .models import PromoCode, Product, PromoHistory, Transaction
from model_mommy import mommy
from django.utils import timezone
from monthdelta import monthdelta
from django.contrib.auth.models import User


# Create your tests here.
class TestPromoCode(APITestCase):

    def test_valid_code(self):
        user = mommy.make(User)
        code = mommy.make(PromoCode, frequency_of_use=5, benefit=5, quantity=5, code='1234abc', category='A', start_date=timezone.now(), end_date=timezone.now() + monthdelta(1))
        products = mommy.make(Product, _quantity=5, category='A')
        data = {
            'code': code.code,
            'product': [product.id for product in products]
        }
        url = '/ar/paymob_game/promo_code/'
        self.client.force_login(user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PromoHistory.objects.filter(user=user).count(), 5)
        self.assertEqual(Transaction.objects.filter(user=user).count(), 1)

    def test_invalid_code(self):
        user = mommy.make(User)
        mommy.make(PromoCode, frequency_of_use=5, benefit=5, quantity=5, code='1234abc', category='A', start_date=timezone.now(), end_date=timezone.now() + monthdelta(1))
        products = mommy.make(Product, _quantity=5, category='A')
        data = {
            'code': 'BAD',
            'product': [product.id for product in products]
        }
        url = '/paymob_game/promo_code/'
        self.client.force_login(user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_user_try_to_code_more_than_freq_of_use(self):
        user = mommy.make(User)
        code = mommy.make(PromoCode, frequency_of_use=5, benefit=5, quantity=5, code='1234abc', category='A', start_date=timezone.now(), end_date=timezone.now() + monthdelta(1))
        mommy.make(PromoHistory, _quantity=5, user=user, promo_code=code)
        products = mommy.make(Product, _quantity=5, category='A')
        data = {
            'code': code.code,
            'product': [product.id for product in products]
        }
        url = '/paymob_game/promo_code/'
        self.client.force_login(user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_try_to_code_expired(self):
        user = mommy.make(User)
        code = mommy.make(PromoCode, frequency_of_use=5, benefit=5, quantity=5, code='1234abc', category='A', start_date=timezone.now(), end_date=timezone.now() - monthdelta(1))
        mommy.make(PromoHistory, _quantity=4, user=user, promo_code=code)
        products = mommy.make(Product, _quantity=5, category='A')
        data = {
            'code': code.code,
            'product': [product.id for product in products]
        }
        url = '/paymob_game/promo_code/'
        self.client.force_login(user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_try_to_code_with_more_Than_configured_quantity(self):
        user = mommy.make(User)
        code = mommy.make(PromoCode, frequency_of_use=5, benefit=5, quantity=5, code='1234abc', category='A', start_date=timezone.now(), end_date=timezone.now() - monthdelta(1))
        mommy.make(PromoHistory, _quantity=4, user=user, promo_code=code)
        products = mommy.make(Product, _quantity=7, category='A')
        data = {
            'code': code.code,
            'product': [product.id for product in products]
        }
        url = '/paymob_game/promo_code/'
        self.client.force_login(user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
