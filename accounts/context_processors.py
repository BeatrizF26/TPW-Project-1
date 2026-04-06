from .mode import BUYER_MODE, SELLER_MODE, get_active_mode
from chat.models import Message

def account_mode(request):
    active_mode = get_active_mode(request)
    has_unread_messages = False

    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        has_unread_messages = Message.objects.filter(
            chat__buyer=user,
            is_read=False,
        ).exclude(sender=user).exists() or Message.objects.filter(
            chat__seller=user,
            is_read=False,
        ).exclude(sender=user).exists()

    return {
        'active_mode': active_mode,
        'buyer_mode': BUYER_MODE,
        'seller_mode': SELLER_MODE,
        'has_unread_messages': has_unread_messages,
    }
