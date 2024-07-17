# myapp/utils.py
""" from .models import Template, Template2Button, FileForDocuments


def get_text(title, lang, button=False):
    try:
        if button:
            text = Template2Button.objects.get(title=title)
        else:
            text = Template.objects.get(title=title)
        if lang == 'ru':
            text = text.body_ru
        elif lang == 'en':
            text = text.body_en
        else:
            text = text.body_uz
    except Exception:
        text = f'Шаблон: {title} не найден!!! '
    return text


def get_document(id):
    result = FileForDocuments.objects.filter(document=id)
    return result """

from .models import *
def intcomma(number):
    """
    Функция для форматирования целых чисел с добавлением запятых как разделителя разрядов.
    
    Args:
        number (int): Целое число для форматирования.
    
    Returns:
        str: Отформатированная строка с добавлением запятых как разделителя разрядов.
    """
    parts = []
    for i, digit in enumerate(reversed(str(number))):
        if i > 0 and i % 3 == 0:
            parts.append(' ')
        parts.append(digit)
    return ''.join(reversed(parts))

def refresh_count_for_products():
    #Checked
    ingredients  = Ingredient.objects.all()
    for ingredient in ingredients:
        ingredient.weight = 0
        inventory_products = InventoryIngredient.objects.filter(ingredient=ingredient.id)
        print(inventory_products, 1212)
        order_products = OrderProduct.objects.all()
        for p in inventory_products:
            ingredient.weight += p.weight
        for p in order_products:
            ings = ProductIngedients.objects.filter(product=p.id)
            print(ings, 1121212)
            if len(ings) > 0:
                for ing in ings:
                    ingredient.weight -= p.count*ing.weight
        ingredient.save()


def calculate_driver_cash(driver, payed):
    if payed:
        cash = 0
        for payment in Payment.objects.filter(driver=driver):
            cash += payment.cash
    else:
        cash = 0
        for payment in Payment.objects.filter(driver=driver):
            cash -= payment.cash
        for order in Order.objects.filter(driver=driver):
            cash += order.cash
            for refund in Refund.objects.filter(order=order):
                for refund_product in refund.Refund.all():
                    cash -= refund_product.product.case * refund_product.count * refund_product.price
    return intcomma(cash)