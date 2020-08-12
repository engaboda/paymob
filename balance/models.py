from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from django.utils import timezone
from django.utils.translation import gettext as _

CATEGORIES = [
    ('A', 'A Class'),
    ('B', 'B Class'),
]

# Create your models here.
class PromoCode(TimeStampedModel):
    """
        i assume this table will hold promo codes for PayMob Game.
        you can use this promo code for set of time.
        we design quantity to be less than all our product price.
    """
    title = models.CharField(_('Title'), max_length=180)
    description = models.TextField()
    benefit = models.IntegerField() # i assume this field to use how much this code will add to every user use it.
    quantity = models.IntegerField() # refer to number of products that code can work with.
    code = models.CharField(max_length=180, unique=True)
    category = models.CharField(max_length=1, choices=CATEGORIES) # to identify which category this code will work with.
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    # we can delete it and sum all promoHistory and make it frequency but we can let it if some analysis will make on this field.
    # or you want make constriants on this field to not let any one use it more than number of times.
    frequency_of_use = models.IntegerField()

    def __str__(self):
        return "{} {} {} {}".format(self.title, self.code, self.quantity, self.is_active)

    @property
    def is_expired(self):
        return (timezone.now().date() >= self.end_date)


class PromoHistory(TimeStampedModel):
    """
        Here we will see which product this promo code used.
    """
    user = models.ForeignKey(User, related_name='user_promo_code_history', on_delete=models.SET_NULL, null=True)
    promo_code = models.ForeignKey(PromoCode, related_name='promo_code_history', on_delete=models.SET_NULL, null=True)
    prodcut = models.ForeignKey("Product", related_name='product_promo_history', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} {} {}".format(self.user.email, self.promo_code.code, self.quantity)


class TransactionHistory(TimeStampedModel):
    """
        will hold information about one transaction.
        user can buy three item in one trnasaction.
    """
    transaction = models.ForeignKey("Transaction", related_name='transaction_history', on_delete=models.SET_NULL, null=True)
    prodcut = models.ForeignKey("Product", related_name='product_history', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{} {}".format(self.transaction.id, self.prodcut.id)


class Transaction(TimeStampedModel):
    """
        who make this transaction.
        from which bank pulled his mony.
        quantity for the whole transaction.
        if you want get all history of of transaction you should combine PromoHistory, TransactionHistory
    """
    user = models.ForeignKey(User, related_name='user_transaction_history', on_delete=models.SET_NULL, null=True)
    bank_account = models.ForeignKey("BankAccount", related_name="bank_account_transaction", on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField("Price")

    def __str__(self):
        return "{} {}".format(self.user.email, self.quantity)


class Product(TimeStampedModel):
    """
        here we have set of products.
        each product has price.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    category = models.CharField(max_length=1, choices=CATEGORIES)

    def __str__(self):
        return "{} {}".format(self.name, self.price)

class BankAccount(TimeStampedModel):
    user = models.ForeignKey(User, related_name='user_bank', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    routing_number = models.CharField(max_length=100)
    holder_name = models.CharField(max_length=100)

    def __str__(self):
        return '{} {} {}'.format(self.user.email, self.account_number, self.routing_number)
