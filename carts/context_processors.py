from .models import Cart, CartItem
from . import _cart_id

def counter(request):
  cart_counter = 0
  if 'admin' in request.path:
    return {}

  else:
    try:
      cart = Cart.objects.filter(cart_id = _card_id(request))
      cart_items = CartItem.objects.all().filter(cart = cart[:1])
      for cart_item in cart_items:
        cart_count += cart_item.quantity

    except Cart.DoesNotExist:
      cart_count = 0
  return dict(cart_count = cart_count)