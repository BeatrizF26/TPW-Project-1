BUYER_MODE = 'buyer'
SELLER_MODE = 'seller'

def get_active_mode(request):
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return None

    if user.is_buyer and user.is_seller:
        stored_mode = request.session.get('active_mode')
        if stored_mode in {BUYER_MODE, SELLER_MODE}:
            return stored_mode
        return SELLER_MODE

    if user.is_seller:
        return SELLER_MODE

    if user.is_buyer:
        return BUYER_MODE

    return None

def set_active_mode(request, mode):
    if mode in {BUYER_MODE, SELLER_MODE}:
        request.session['active_mode'] = mode
