from product.models import ProductVariation
from django.shortcuts import get_object_or_404


class Cart:
    def __init__(self, request):

        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}  #cria a sessão cart
        self.product = cart

    #def __str__(self):
    #  return {self.product}
    def get_product(self):
        return self.product

    def add(self, variation_id, quantity):
        variation = get_object_or_404(ProductVariation,
                                      available=True,
                                      id=variation_id)
        if variation.stock <= int(quantity):
            quantity = variation.stock
        variation_id = str(variation_id)
        if variation_id in self.product:  #[variation_id]:  ou seja se o produto existe na session:
            self.product[variation_id]['quantity'] = int(quantity)
            if variation.on_promotion == True:
                self.product[variation_id][
                    'price_or_promotion_price'] = variation.promotion_price
                total = float(variation.promotion_price) * int(quantity)
                total = "{:.2f}".format(total)
                self.product[variation_id]['totalitem'] = total
            else:
                self.product[variation_id][
                    'price_or_promotion_price'] = variation.price
                total = float(variation.price) * int(quantity)
                total = "{:.2f}".format(total)
                self.product[variation_id]['totalitem'] = total

        else:
            if variation.on_promotion == True:
                total = float(variation.promotion_price) * int(quantity)
                total = "{:.2f}".format(total)

                self.product[variation.id] = {
                    'quantity': quantity,
                    'price_or_promotion_price': variation.promotion_price,
                    'totalitem': total
                }
            else:
                total = float(variation.price) * int(quantity)
                total = "{:.2f}".format(total)
                self.product[variation.id] = {
                    'quantity': quantity,
                    'price_or_promotion_price': variation.price,
                    'totalitem': total
                }

        self.save()

    def delete_item_from_session(self, variation_id):
        variation_id = str(variation_id)

        if variation_id in self.product:  # se existir a variação dentro da sessão
            del self.product[variation_id]  # exclui da sessão o produto
            self.save()  # chama a função save

    def clear(self):
        self.session['cart'] = {}
        self.save()  # chama a função save

    def cart_total(self):
        total_of_all_itens_in_the_session = 0
        for item in self.product.values():
            total_of_all_itens_in_the_session += float(item.get('totalitem'))
        return total_of_all_itens_in_the_session

    def save(self):
        self.session.modified = True


# for variation_id in self.product
# time = self.product.get(variation_id).get('time')
#timenow = datetime.now()
#if timenow-time>5:
#  self.cart.get(variation_id).remove()
#  self.save
#else:
#  self.cart[variation_id]['time'] = timenow
#variation = product.get()
"""
       # if not request.session.get('cart'):
          # if cart not in request.session['cart']:   senão eixste uma  session(dicionário) com o nome 'cart'

                #  cart = self.session.get('cart')  #get é o método de dicionário #não confunda com o get do django!
        if not 'cart' in request.session:
"""
