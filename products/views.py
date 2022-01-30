
from multiprocessing import context
from django.shortcuts import render
import requests, json
from .models import UserDetails
from home.models import Product, PurchasedItem, Order
from django.shortcuts import HttpResponse, redirect
from home import PaymentGateways
from django.template import RequestContext

from products.models import UserDetails

# Create your views here.

def products(request):
    products = Product.objects.filter(status='published')[:3]

    context = {
        'products': products
    }

    return render(request, 'products.html', context)



def product_details(request, pid):
    bought = False
    if Product.objects.filter(id=pid):
        item = Product.objects.get(id=pid)
        # Checks if User has already bought item
        if request.user.is_authenticated:
            user_id = request.user.id
            if PurchasedItem.objects.filter(product_id=pid, user_id=user_id):
                bought = True
                return render(request, 'product-details.html', {'item': item, 'bought': bought})
            else:
                return render(request, 'product-details.html', {'item': item, 'bought': bought})
            
        else:
            return render(request, 'product-details.html', {'item': item, 'bought': bought})
    
    else:
        return HttpResponse('Product Not FOUND!')



def purchase(request):
    if request.user.is_authenticated:
        if request.GET['pid'] != '':
            id = request.GET['pid']
            if Product.objects.get(id=id):
                product = Product.objects.get(id=id)

                # verify & call payment option
                if product.gateway == 'paddle':
                    price = product.list_price
                    product_name = product.brand
                    product_id = id
                    pay = PaymentGateways.PaddlePayment(price, product_name, product_id)
                    checkout_url = pay.checkoutrequest()
                    
                    if len(checkout_url) > 1:
                        r_url = (json.loads(checkout_url))['response']['url']
                        return redirect(r_url)
                    else:
                        print('\n')
                        error = (checkout_url)['url']
                        print((checkout_url)['url'])
                        return HttpResponse(error)

                elif product.gateway == 'stripe':
                    return HttpResponse('Stripe Payment under Maintainance')
                elif product.gateway == 'bitpay':
                    return HttpResponse('BitPay Payment under Maintainance')
                else:
                    return HttpResponse('Unknown payment gateway. Contact admin for help')

            else:
                return HttpResponse('Product not found')

        else:
            return HttpResponse('Error 502: Bad Request')
    
    else:
        return redirect('reg_user')



def order(request):
    if request.user.is_authenticated:
        user_id = request.user.id

        checkout_id = request.GET['checkout_id']
        order_details = 'https://sandbox-checkout.paddle.com/api/1.0/order?checkout_id=' + checkout_id
        response = requests.get(url=order_details)
        data = response.json()

        # print('Response****************************************')
        # print('\n', response.json(), '\n')
    
        if data['state'] != 'processed':
            return HttpResponse('Something went wrong')
        else:
            Order.objects.create(
                status = data['state'],
                checkout_id=checkout_id,
                product_name=data['lockers'][0]['product_name'],
                product_id=1,
                payment=data['order']['formatted_total'],
                order_id=data['order']['order_id'],
                tax=data['order']['formatted_tax'],
                coupon_code=data['order']['coupon_code'],
                receipt_url=data['order']['receipt_url'],
                email=data['order']['customer']['email'],
                marketing_consent=data['order']['customer']['marketing_consent'],
                is_subscription=data['order']['is_subscription'],
                user=user_id
            )

            PurchasedItem.objects.create(
                product_id=1,
                user_id=user_id,
                order_id=data['order']['order_id']
            )
        return redirect(data['order']['receipt_url'])
    else:
        return redirect('reg_user')

# showing user details
def user_account(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        userdetail = UserDetails.objects.filter(user=user_id).all()
        context = {
            'userdetail': userdetail,
        }
        return render(request, 'user_Account.html', context)
    else:
        return redirect('reg_user')

def user_upload(request):
    if request.user.is_authenticated:
        id = request.user.id
        if request.method == "POST":
            data = request.POST
            full_name = data['full_name']
            email = data['email']
            phone_number = data['phone_number']
            country = data['country']
            postcode = data['postcode']

            # form validations
            if full_name == '':
                return redirect('user_upload')
            elif email == '':
                return redirect('user_upload')
            elif phone_number == '':
                return redirect('user_upload')
            elif country == '':
                return redirect('user_upload')
            elif postcode == '':
                return redirect('user_upload')
            else:
                UserDetails.objects.create(
                    full_name = full_name,
                    email = email,
                    phone_number = phone_number,
                    country = country,
                    postcode = postcode,
                    user = id

                )
                return redirect('products:user_account')
        else:
            return render(request, 'user_upload.html')

    else:
        return redirect('reg_user')


def user_account_edit(request):
    if request.user.is_authenticated:
        single_id = request.user.id
        if request.method == 'POST':
            user_id = request.POST.get('user_id', True)
            full_name = request.POST['full_name']
            email = request.POST['email']
            phone_number = request.POST['phone_number']
            country = request.POST['country']
            postcode = request.POST['postcode']

            ins = UserDetails.objects.filter(id=user_id).update(
                full_name = full_name,
                email = email,
                phone_number = phone_number,
                country = country,
                postcode = postcode,
                user = single_id
            )
            return redirect('products:products')
        else:
            user_id = request.GET['user_id']
            if user_id == '':
                return redirect('products:user_account')
            elif UserDetails.objects.get(id=user_id):
                details = UserDetails.objects.get(id=user_id)

                cont = {
                    'action': 'edit',
                    'details': details
                }
                return render(request, 'user_upload.html', cont)

            else:
                return redirect('products:user_account')
    else:
        return redirect('logout')

