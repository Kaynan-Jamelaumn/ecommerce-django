from django.shortcuts import render, redirect

#from .models import account
from django.contrib.auth.models import User  # REGISTER  # REGISTER

from validator import password_validator  #REGISTER
from validator import state_city_validator  #State_On_Change

from django.contrib.auth import authenticate, login, logout  #LOGIN

from django.http import JsonResponse  #State_on_change
from .models import Address  #Address Address_register Address_delete

from order.models import Orders

import re  #i  dont know regex


# Create your views here.
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'account/login.html')
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                the_user_filtered_by_email = User.objects.get(email=email)
                the_username = the_user_filtered_by_email.username
                if the_user_filtered_by_email:

                    user = authenticate(request,
                                        username=the_username,
                                        password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('product:index')
                    else:
                        return render(request, 'account/login.html',
                                      {'message': 'credentials are wrong'})
            except:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('product:index')
                else:
                    return render(request, 'account/login.html',
                                  {'message': 'Credentials are wrong'})
    else:
        return redirect('product:index')


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'account/register.html')

        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_confirmation = request.POST.get('password_confirmation')

            is_password_valid = password_validator(
                password, password_confirmation)  #Validator
            if is_password_valid == True:
                pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
                if not re.match(pat, email):
                    return render(request, 'account/register.html',
                                  {'message': 'e-mail is invalid'})
                if not User.objects.filter(
                        email=email) and not User.objects.filter(
                            username=name):
                    user = User.objects.create_user(username=name,
                                                    email=email,
                                                    password=password)
                    user.save()
                    login(request, user)
                    return redirect('product:index')
                else:
                    return render(request, 'account/register.html',
                                  {'message': 'already registred'})
            else:

                return render(request, 'account/register.html',
                              {'message': is_password_valid[0]})

    else:
        return redirect('product:index')


def user_logout(request):
    logout(request)
    return redirect('account:login')


def user_update(request):
    if request.method == 'GET':
        return render(request, 'account/update.html')
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        is_password_valid = password_validator(
            password, password_confirmation)  #Validator
        if is_password_valid == True:
            User.objects.filter(user=request.user).update(password=password)
            return render(request, 'account/dashboard.html',
                          {'message': 'password updated successfuly'})
        else:
            return render(request, 'account/update.html',
                          {'message': is_password_valid[0]})


def dashboard(request):
    if request.user.is_authenticated:
        orders = Orders.objects.filter(user=request.user).order_by('-id')
        return render(request, 'account/dashboard.html', {'orders': orders})
    else:
        return redirect('account:login')


def address(request):
    if request.user.is_authenticated:

        addresses = Address.objects.filter(user=request.user)
        return render(request, 'account/address.html',
                      {'addresses': addresses})

    else:
        redirect('account:login')


def address_delete(request, id):
    if request.user.is_authenticated:
        address = Address.objects.get(id=id, user=request.user)
        if address is not None:
            address.delete()

        return redirect('account:address')

    else:
        return redirect('account:login')


def address_register(request):

    if request.user.is_authenticated:
        states = (
            ('Acre'),
            ('Alagoas'),
            ('Amapá'),
            ('Amazonas'),
            ('Bahia'),
            ('Ceará'),
            ('Distrito Federal'),
            ('Espírito Santo'),
            ('Goiás'),
            ('Maranhão'),
            ('Mato Grosso'),
            ('Mato Grosso do Sul'),
            ('Minas Gerais'),
            ('Pará'),
            ('Paraíba'),
            ('Paraná'),
            ('Pernambuco'),
            ('Piauí'),
            ('Rio de Janeiro'),
            ('Rio Grande do Norte'),
            ('Rio Grande do Sul'),
            ('Rondônia'),
            ('Roraima'),
            ('Santa Catarina'),
            ('São Paulo'),
            ('Sergipe'),
            ('Tocantins'),
        )
        acre = ('Rio Branco', 'Cruzeiro do Sul', 'Sena Madureira', 'Tarauacá',
                'Feijó', ' Brasileia', 'Senador Guiomard', 'Plácido de Castro',
                'Xapuri', 'Rodrigues Alves', 'Marechal Thaumaturgo',
                'Mâncio Lima', 'Porto Acre', 'Epitaciolândia', 'Acrelândia',
                'Porto Walter', 'Capixaba', 'Bujari', 'Manoel Urbano',
                'Jordão', 'Assis Brasil', 'Santa Rosa do Purus')
        if request.method == 'GET':
            return render(request, 'account/address_register.html', {
                'states': states,
                'acre': acre
            })
        if request.method == 'POST':
            postcode = request.POST.get('postcode')
            address = request.POST.get('address')
            number = request.POST.get('number')
            state = request.POST.get('state')
            city = request.POST.get('city')

            address_object = Address(user=request.user,
                                     address=address,
                                     number=number,
                                     post_code=postcode,
                                     state=state,
                                     city=city)
            address_object.save()
            return redirect('account:dashboard')
    else:
        return redirect('account:login')


def state_on_change(request):
    if request.POST.get('action') == 'state_on_change':
        state_selected = request.POST.get('state_selected')
        receive_cities = state_city_validator(state_selected)

        if receive_cities:

            response = JsonResponse({'cities_in_state': receive_cities})

            return response
