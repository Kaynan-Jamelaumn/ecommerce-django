from django.shortcuts import render, redirect

from django.http import JsonResponse

from .models import Product, Category, SubCategory, ProductVariation, ExtraVariationProductPicture

from django.core.paginator import Paginator

from django.urls import resolve


# Create your views here.
def index(request):
    on_promotion = Product.objects.filter(on_promotion=True)

    products = Product.objects.filter(available=True).order_by('id')
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    paginator = Paginator(products, 25)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(
        request, 'index.html', {
            'on_promotion': on_promotion,
            'products': products,
            'categories': categories,
            'subcategories': subcategories
        })


def category(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category_id)

    return render(request, 'product/category.html', {
        'products': products,
        'category': category
    })


def subcategory(request, category_id, subcategory_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(subcategory=subcategory_id)

    subcategory = SubCategory.objects.get(id=subcategory_id)
    return render(request, 'product/subcategory.html', {
        'products': products,
        'category': category,
        'subcategory': subcategory
    })


def detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'product/detail.html', {'detailproduct': product})


def search(request):
    result = request.GET.get('result')
    if result is None:
        current_url = resolve(request.path_info).url_name
        return render(request, current_url)

    products = Product.objects.filter(available=True,
                                      name__icontains=result).order_by('id')
    #print(products.query)
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    paginator = Paginator(products, 1)

    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(
        request, 'product/search.html', {
            'products': products,
            'categories': categories,
            'subcategories': subcategories
        })


def variation_on_change(request):
    if request.POST.get('action') == 'variation_on_change':
        variation_id = request.POST.get('variation_selected')
        variation = ProductVariation.objects.get(id=variation_id)
        if variation:
            pictures = ExtraVariationProductPicture.objects.filter(variation=variation)
            picture_list = []
            for picture in pictures:
              picture_list.append(picture.image.url)
            description = variation.long_description
            stock = variation.stock
            if variation.on_promotion == True:
                price = variation.price
                promotion_price = variation.promotion_price         
                return JsonResponse({
                    'price': price,
                    'promotion_price': promotion_price,
                    'description': description,
                    'stock': stock, 'pictures': picture_list
                })
            else:
                price = variation.price
                return JsonResponse({
                    'price': price,
                    'description': description,
                    'stock': stock, 'pictures': picture_list
                })
        return redirect('product:index')


def buy_product(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            request.POST.get('quantity')
        return redirect('product:index')
    else:
        redirect('account:login')
