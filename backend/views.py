from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import *
from .utils import refresh_count_for_products

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods



from django.http import HttpResponseRedirect

@csrf_exempt  # Отключаем CSRF защиту для этого запроса
@require_http_methods(["POST"])  # Разрешаем только POST запросы
def save_table_data(request):
    try:
        data = json.loads(request.body)  # Преобразуем JSON из тела запроса в Python словарь
        products = data.get('products')
        status = False
        refund = None
        for data in products:
            order = Order.objects.get(id=int(data.get('order_id')))
            if 'quantity' in data and int(data['quantity']) > 0:
                if not status:
                    refund = Refund.objects.create(order=order)
                    status = True
                product = Product.objects.get(name=data['name'])
                refund_product = RefundProduct.objects.create(
                    product=product,
                    price=data['price'],
                    count=int(data['quantity']),
                    refund=refund
                )
                
        
        # Обработка данных
        return JsonResponse({'status': 'success', 'message': 'Malumotlar saqlandi'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        # Получаем данные из POST-запроса
        payment_amount = request.POST.get('paymentAmount')
        client_id = request.POST.get('clientId')
        if int(payment_amount) <= 0:
            raise ValueError()
        client = Client.objects.get(id=client_id)
        payment = Payment.objects.create(
            client=client,
            cash = int(payment_amount)
            )
        if payment_amount and client_id:
            # Здесь вы можете обработать оплату и выполнить любую другую логику
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid data in POST request'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def process_products_check_ingredients(products):
    refresh_count_for_products()
    for ingredient in Ingredient.objects.all():
        for data in products:
            for data in products:
                if 'count' in data and data['count'] != '' and int(data['count']) > 0:
                    product = Product.objects.get(name=data['name'])
                    for product_ingedient in ProductIngedients.objects.filter(product=product, ingredient=ingredient):
                        ingredient.weight -= product_ingedient.weight
        if ingredient.weight < 0:
            return False
    return True
@csrf_exempt
@require_http_methods(["POST"])
def process_products(request):
    if request.method == 'POST':
        # Получите данные из запроса
        data = json.loads(request.body)
        print(data)
        products = data.get('products')
        client_id = data.get('clientId')
        status = False
        order = None
        client = Client.objects.get(id=client_id)
        cash = 0
        if not process_products_check_ingredients(products):
            return JsonResponse({'error': 'Invalid request method or not an AJAX request.'}, status=400)
        for data in products:
            if 'count' in data and data['count'] != '' and int(data['count']) > 0:
                if not status:
                    order = Order.objects.create(
                    client=client,
                    )
                    status = True
                product = Product.objects.get(name=data['name'])
                order_product = OrderProduct.objects.create(
                    product=product,
                    count=int(data['count']),
                    order=order,
                    price=data['price'],
                )
                cash += int(order_product.count) * int(order_product.price)
        order.cash = cash
        order.save()
        refresh_count_for_products()
        if not status :
            raise ValueError
        return HttpResponseRedirect(f'/document/{order.id}')  # Замените '/success/' на URL вашего редиректа
    else:
        return JsonResponse({'error': 'Invalid request method or not an AJAX request.'}, status=400)

@login_required
def document(request, id=1):
    context = dict()
    if id == 1:
        order = list(Order.objects.all())[-1]
    else:
        order = Order.objects.get(id=id)
    client = order.client
    order_products = OrderProduct.objects.filter(order=order)
    total_sum = 0
    products = []
    for order_product in order_products:
        products.append(
            {
                'id': order_product.id,
                'product': order_product.product,
                'price': order_product.price,
                'count': order_product.count,
                'order': order_product.order,
                'cash': order_product.count * order_product.price,
            }
        )
        total_sum += order_product.count * order_product.price
    context['products'] = products
    context['client'] = client
    context['total_sum'] = total_sum
    context['order'] = order
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'document.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def inventory(request, id=1):
    context = dict()
    inventory = Inventory.objects.get(id=id)
    products = InventoryIngredient.objects.filter(inventory=inventory)
    total_count = 0
    for product in products:
        total_count += product.count
    context['products'] = products
    context['inventory'] = inventory
    context['total_count'] = total_count
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'inventory.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def documents(request):
    context = dict()
    orders = Order.objects.all().order_by('-created_date')
    inventorys = Inventory.objects.all().order_by('-created_date')
    context['orders'] = orders
    context['inventorys'] = inventorys
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'documents.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def select_documents(request):
    context = dict()
    orders = Order.objects.all()
    context['orders'] = orders
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'select_documents.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@csrf_exempt  # Отключаем CSRF защиту для этого запроса
@require_http_methods(["POST"])  # Разрешаем только POST запросы
def save_products(request):
    try:
        data = json.loads(request.body)  # Преобразуем JSON из тела запроса в Python словарь
        products = data.get('products')
        status = False
        inventory = None
        for data in products:
            if 'quantity' in data:
                if int(data['quantity']) < 0:
                    raise ValueError
                
        for data in products:
            if 'quantity' in data and int(data['quantity']) > 0:
                if not status:
                    inventory = Inventory.objects.create()
                    status = True
                ingredient = Ingredient.objects.get(name=data['name'])
                inventory_product = InventoryIngredient.objects.create(
                    ingredient=ingredient,
                    weight=int(data['quantity']),
                    inventory=inventory
                )
        # Обработка данных
        return JsonResponse({'status': 'success', 'message': 'Malumotlar saqlandi'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': "Malumotlarni to'ldirishda xatolik"})


def logout_view(request):
    logout(request)
    return redirect('login') 

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Неправильный логин или пароль'})
    else:
        return render(request, 'login.html')

@login_required
def index(request):
    context = dict()
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        refresh_count_for_products()
        context['ingredients'] = list(Ingredient.objects.filter(weight__gt=0).order_by('name'))    
        return render(request, 'index-1.html', context)
    elif request.user.groups.filter(name='Бугалтер').exists():
        return render(request, '1-block/bugalter.html', context)
    
    elif request.user.groups.filter(name='Стройка').exists():
        return render(request, '2-block/stroyka.html', context)
    elif request.user.groups.filter(name='Маркетинг').exists():
        return render(request, '3-block/marketing.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def stroy(request, id):
    context = dict()
    if request.user.groups.filter(name='Стройка').exists():
        return render(request, '2-block/stroy.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
    
@login_required
def dom(request, id):
    context = dict()
    if request.user.groups.filter(name='Маркетинг').exists():
        return render(request, '3-block/dom.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def kirim(request):
    context = dict()
    context['Ingredients'] = list(Ingredient.objects.all().order_by('name'))
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'kirim.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

@login_required
def chiqim(request):
    refresh_count_for_products()
    clients_list = list(Client.objects.all().order_by('name'))*25

    clients = []
    for client in  clients_list:
        cash = 0
        for payment in Payment.objects.filter(client=client):
            cash -= payment.cash
        for order in Order.objects.filter(client=client):
            order_cash = order.cash
            cash += order_cash
        clients.append(
            {
                'id': client.id,
                'name': client.name,
                'phone': client.phone,
                'auto': client.comment,
                'cash': cash
            }
        )
    context = {
        'id': 1,
        'clients': clients,
    }
    
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'chiqim.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
    
@login_required
def client(request, id=1):
    client = Client.objects.get(id=id)
    context = dict()
    context['products'] = list(Product.objects.order_by('name'))
    context['client'] = client
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'client.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
    

""" @login_required
def finance(request):
    
    orders_all = Order.objects.all().order_by('-created_date')
    orders_1 = Order.objects.filter(status='Yakunlandi').order_by('-created_date')
    orders_2 = Order.objects.filter(status='Jarayonda').order_by('-created_date')
    context = dict()
    context['orders_all'] = orders_all
    context['orders_1'] = orders_1
    context['orders_2'] = orders_2
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'finance.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.") """

@login_required
def finance_client(request):
    refresh_count_for_products()
    clients_list = list(Client.objects.all())*25
    total_cash = 0
    clients = []
    for client in  clients_list:
        cash = 0
        for order in Order.objects.filter(client=client):
            order_cash = order.cash
            for refund in Refund.objects.filter(order=order):
                for refund_product in refund.Refund.all():
                    order_cash -= refund_product.product.case * refund_product.count * refund_product.price
            cash += order_cash
        for payment in Payment.objects.filter(client=client):
            cash -= payment.cash
        clients.append(
            {
                'id': client.id,
                'photo': client.photo,
                'name': client.name,
                'phone': client.phone,
                'auto': client.auto,
                'cash': cash
            }
        )
        total_cash += cash
    context = {
        'id': 1,
        'clients': clients,
        'total_cash': total_cash
    }
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'finance-client.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")

""" @login_required
def order_detail(request, id=1):
    context = dict()
    order = Order.objects.get(id=id)
    payments = Payment.objects.filter(order=order)
    refunds = Refund.objects.filter(order=order)
    refund_products = []
    total_cash = 0
    for refund in refunds:
        for refund_product in refund.Refund.all():
            refund_products.append(
                {
                    'id': refund_product.id,
                    'name': refund_product.product.name,
                    'product': refund_product.product,
                    'refund': refund_product.refund,
                    'price': refund_product.price,
                    'count': refund_product.count,
                    'cash': refund_product.product.case * refund_product.count * refund_product.price,
                }
            )
            total_cash += refund_product.product.case * refund_product.count * refund_product.price
    order_products = OrderProduct.objects.filter(order=order)
    context['refund_products'] = refund_products
    context['order_products'] = order_products
    context['total_cash'] = total_cash
    context['order'] = order
    context['payments'] = payments
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'order_detail.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.") """

@login_required
def finance_client_detail(request, id=1):
    context = dict()
    client = Client.objects.get(id=id)
    orders = Order.objects.all()
    payments = Payment.objects.filter(client=client)

    cash = 0
    for order in Order.objects.filter(client=client):
        order_cash = order.cash
        """ for refund in Refund.objects.filter(order=order):
            for refund_product in refund.Refund.all():
                order_cash -= refund_product.product.case * refund_product.count * refund_product.price """
        cash += order_cash
    """ for payment in Payment.objects.filter(client=client):
        cash -= payment.cash """
    context['client'] = {
            'client':client,
            'id': client.id,
            'photo': client.photo,
            'name': client.name,
            'phone': client.phone,
            'auto': client.auto,
            'cash': cash
    }
    

    orders = Order.objects.filter(client=client)
    context['payments'] = payments
    context['orders'] = orders
    # Проверяем, принадлежит ли пользователь к группе "Склад"
    if request.user.groups.filter(name='Склад').exists():
        return render(request, 'finance-client-detail.html', context)
    else:
        # Если пользователь не входит ни в одну из этих групп
        return HttpResponse("У вас нет прав для просмотра этой страницы.")
