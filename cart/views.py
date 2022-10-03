from django.shortcuts import render, redirect
from django.http import JsonResponse

from product.models import ProductVariation
from .cart import Cart


# Create your views here.
def cart_add(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        if request.POST.get('action') == 'cart_add':
            variation_id = int(request.POST.get('variationid'))
            quantity = request.POST.get('productquantity')
            if int(quantity) > 0:
                cart.add(variation_id, quantity)
                response = JsonResponse({'json': 'bar'})
                return response
    else:
        return redirect('account:login')


def cart_view(request):

    if request.user.is_authenticated:
        cart = Cart(request)
        itens = cart.get_product(
        )  #então  o que tem aqui rapaziada. Eu pego a session que possui todos os produto nela
        # e antes de eu só colocar pra renderizar no template eu meio que adiciono de novo na session pra atualizar o preço
        #caso tenha ocorrido uma mudança no banco de dados e aí por isso tem todos esses For Loop
        variation_id_list = []
        variation_quantity_list = []
        for product_quantity in itens.values():  #pega a quantidade
            product_quantity = product_quantity.get('quantity')
            variation_quantity_list.append(
                product_quantity)  #adiciona em uma lista
        for variation_id in itens.keys():  # pega o id
            variation_id_list.append(variation_id)  # adiciona na lista

        for index in range(
                0, len(itens)
        ):  #e readiciona na session atualizando preço e coisa do tipo
            cart.add(variation_id_list[index], variation_quantity_list[index])
        itens = cart.get_product()
        #aí eu pego a session de novo e passo pra renderizar
        variations = ProductVariation.objects.all()
        integerid = []
        for stringid in itens:  # tive que criar esse foloop porque os IDs na session estão salvos como string, aí tenho que converter eles pra int
            integerid.append(int(stringid))
        total = cart.cart_total()
        return render(
            request, 'cart/cart_page.html', {
                'other_fields': itens.values(),
                'variations': variations,
                'integerid': integerid,
                'total': total
            })
    else:
        return redirect('account:login')


def remove_item_from_session(request, id):
    cart = Cart(request)
    cart.delete_item_from_session(variation_id=id)
    return redirect('cart:view')
