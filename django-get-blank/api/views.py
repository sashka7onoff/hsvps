import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from main.models import Product, Cart


@csrf_exempt
def add_product(request):
    if request.method == 'POST':
        user_id = request.GET.get('user_id')
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

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
