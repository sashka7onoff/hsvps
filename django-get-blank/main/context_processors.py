def seo_defaults(request):
    return {
        'seo_title': 'GET-BLANK - сервис автоматического заполнения Excel бланков товарами с 1688.com, Taobao.com и Tmall.com',
        'seo_keywords': 'Как быстро заполнить бланк посредника Taobao, Легко заполнить файл посредника 1688.com',
        'seo_description': 'Если вы заказываете товары с помощью посредников на китайских площадках через Excel бланки, тогда сервис GET-BLANK поможет вам быстрее, удобнее и качественнее оформлять ваши заказы',
    }


def cart_context(request):
    from main.models import Cart, Product
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, deleted=False)
        current_cart_id = request.session.get('current_cart')
        if current_cart_id:
            try:
                current_cart = Cart.objects.get(id=current_cart_id, user=request.user, deleted=False)
            except Cart.DoesNotExist:
                current_cart = carts.first()
                if current_cart:
                    request.session['current_cart'] = current_cart.id
        else:
            current_cart = carts.first()
            if current_cart:
                request.session['current_cart'] = current_cart.id

        if current_cart:
            products = Product.objects.filter(user=request.user, cart=current_cart, deleted=False).order_by('cart_order')
        else:
            products = []
        return {'carts': carts, 'current_cart': current_cart, 'products': products}
    return {}
