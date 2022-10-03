from django.shortcuts import render, redirect
from .models import Orders, Order

from product.models import ProductVariation
from account.models import Address
from cart.cart import Cart


# Create your views here.
def order_info(request, id):
    if request.user.is_authenticated:
        orders = Orders.objects.get(id=id, user=request.user)
        if orders is not None:
            return render(request, 'order/order_details.html',
                          {'orders': orders})
        else:
            redirect('account:dashboard')
    else:
        return redirect('account:login')


def pay(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        if not cart.cart_total() > 0:
            return redirect('product:index')
        if request.method == 'GET':
            cart = Cart(request)

            addresses = Address.objects.filter(user=request.user)
            return render(request, 'order/create.html', {
                'addresses': addresses,
                'total': cart.cart_total()
            })
        if request.method == 'POST':
            address = request.POST.get('address')
            if not address:
                return redirect('account:address_register')
            cart = Cart(request)
            itens = cart.get_product()

            variation_id_list = []
            variation_quantity_list = []
            variation_total_list = []
            variation_price_list = []
            for product in itens.values():  #pega a quantidade total preço
                product_quantity = product.get('quantity')
                product_total = product.get('totalitem')
                product_price = product.get('price_or_promotion_price')
                variation_price_list.append(product_price)
                variation_quantity_list.append(product_quantity)
                variation_total_list.append(product_total)

            for variation_id in itens.keys():  # pega o id
                variation_id_list.append(variation_id)  # adiciona na lista

            for index in range(
                    0, len(itens)):  #creating an order object
                variation_object = ProductVariation.objects.get(
                    id=int(variation_id_list[index]))

                if variation_object.stock < int(
                        variation_quantity_list[index]):
                    return redirect('cart:view', )
                else:
                    quantity = variation_quantity_list[index]
                    total = variation_total_list[index]
                    total = float(total)

                    order_object = Order(user=request.user,
                                         variation=variation_object,
                                         quantity=quantity,
                                         total=total)
                    order_object.save()
                    stock = variation_object.stock
                    stock = stock - quantity
                    ProductVariation.objects.filter(
                        id=variation_object.id).update(stock=stock)

                order_all = Order.objects.all()
                orders_all = Orders.objects.all()
                list_order = []

                for order_object in order_all:
                    the_order_object_is_not_fk_in_orders = True
                    for orders in orders_all:
                        for orders_order_object in orders.order.all():
                          if orders_order_object == order_object:
                            the_order_object_is_not_fk_in_orders = False
                            break
                    if the_order_object_is_not_fk_in_orders == True:
                        list_order.append(order_object)

            address = request.POST.get('address')
            address = Address.objects.get(id=address)
            orders_object = Orders.objects.create(user=request.user,
                                                  address=address,
                                                  total_paid=cart.cart_total(),
                                                  status='P')
            if list_order:
                for order in list_order:
                    orders_object.order.add(order)
                order_object.save()
            cart = cart.clear()
            return redirect('account:dashboard')
    else:
        return redirect('account:login')
