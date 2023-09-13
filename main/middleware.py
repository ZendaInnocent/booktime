from django.http import HttpResponse

from .models import Basket


def BasketMiddleware(get_response):
    def middleware(request):
        if 'basket_id' in request.session:
            basket_id: int = request.session['basket_id']
            basket: Basket = Basket.objects.get(id=basket_id)
            request.basket = basket
        else:
            request.basket = None

        response: HttpResponse = get_response(request)
        return response

    return middleware
