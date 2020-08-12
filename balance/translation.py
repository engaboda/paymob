from modeltranslation.translator import translator, TranslationOptions
from .models import PromoCode, Product


class PromoCodeTranslationOption(TranslationOptions):
    fields = ('title', 'code')


translator.register(PromoCode, PromoCodeTranslationOption)
