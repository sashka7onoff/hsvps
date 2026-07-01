import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from main.models import Product, Cart


@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        user_id = request.GET.get('user_id')
        cart_id = request.GET.get('cart_id')
        marketplace = request.GET.get('marketplace', '1688')

        User = get_user_model()
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        data = request.POST.get('myData', '')
        if not data:
            return JsonResponse({'error': 'No data'}, status=400)

        import urllib.parse
        data = urllib.parse.unquote(data)
        products_data = json.loads(data)

        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id, user=user, deleted=False)
            except Cart.DoesNotExist:
                return JsonResponse({'error': 'Cart not found'}, status=404)
        else:
            cart_id = request.session.get('current_cart')
            try:
                cart = Cart.objects.get(id=cart_id, user=user, deleted=False)
            except Cart.DoesNotExist:
                cart = Cart.objects.filter(user=user, deleted=False).first()
                if not cart:
                    cart = Cart.objects.create(user=user, name='Список 1')

        if marketplace == '1688':
            for color_group in products_data.get('data', [products_data] if isinstance(products_data, dict) else products_data):
                color = '' if color_group.get('color_name') == 'No Colors' else color_group.get('color_name', '')
                shop_home_page = color_group.get('shopHomePage', '')
                color_img_default = color_group.get('colorImgUrlDefault', '')
                color_img_url = color_group.get('colorImgUrl', '')

                for size_item in color_group.get('sizes', []):
                    size_img_url = size_item.get('sizeImgUrl', '')
                    img = color_img_default
                    if size_img_url != 'No img':
                        img = size_img_url
                    if color_img_url != 'No img':
                        img = color_img_url

                    if size_item.get('sizeAmount'):
                        Product.objects.create(
                            user=user,
                            cart=cart,
                            link=size_item.get('pageUrl', ''),
                            img_url=img,
                            color=color,
                            size=size_item.get('sizeName', ''),
                            amount=size_item.get('sizeAmount', 1),
                            price=size_item.get('sizePrice', 0),
                            shop_home_page=shop_home_page,
                        )

        request.session['current_cart'] = cart.id
        return JsonResponse({'status': 'ok', 'cart_id': cart.id})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def me(request):
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)
    return JsonResponse({
        'authenticated': True,
        'id': request.user.id,
        'login': request.user.login,
    })


def carts_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    carts = Cart.objects.filter(user=request.user, deleted=False)
    current_cart_id = request.session.get('current_cart')
    data = []
    for c in carts:
        count = Product.objects.filter(cart=c, deleted=False).count()
        data.append({
            'id': c.id,
            'name': c.name,
            'product_count': count,
            'is_current': c.id == current_cart_id,
        })
    return JsonResponse({'carts': data, 'current_cart_id': current_cart_id})


def cart_detail(request, cart_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    try:
        cart = Cart.objects.get(id=cart_id, user=request.user, deleted=False)
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Cart not found'}, status=404)
    products = Product.objects.filter(cart=cart, deleted=False).order_by('cart_order')
    items = []
    for p in products:
        items.append({
            'id': p.id,
            'link': p.link,
            'img_url': p.img_url,
            'color': p.color,
            'size': p.size,
            'amount': p.amount,
            'price': str(p.price),
        })
    return JsonResponse({'cart': {'id': cart.id, 'name': cart.name}, 'products': items})


@csrf_exempt
def cart_select(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        cart_id = body.get('cart_id')
        if not cart_id:
            return JsonResponse({'error': 'cart_id required'}, status=400)
        try:
            cart = Cart.objects.get(id=cart_id, user=request.user, deleted=False)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart not found'}, status=404)
        request.session['current_cart'] = cart.id
        return JsonResponse({'status': 'ok', 'cart_id': cart.id})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def cart_create(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        name = body.get('name', 'Новый список')
        cart = Cart.objects.create(user=request.user, name=name)
        request.session['current_cart'] = cart.id
        return JsonResponse({'status': 'ok', 'id': cart.id, 'name': cart.name})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_product(request, product_id):
    if request.method == 'DELETE':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        try:
            product = Product.objects.get(id=product_id, user=request.user)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        product.deleted = True
        product.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
