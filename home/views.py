from django import contrib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from requests.api import request
from .models import Product, Order, Category, Tag
from products.models import UserDetails
from . import PaymentGateways
import json
from django.db.models import Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.

def dashboard(request):
    if request.user.is_superuser:
        user_id = request.user.id

        # Stats (Total Earnings, Total Products, Total Orders)
        earnings = Order.objects.aggregate(Sum('payment'))['payment__sum']
        products = Product.objects.count()
        orders = Order.objects.count()
        
        if earnings == None:
            earnings = 0


        # Best selling products section
        best_products = reversed(Product.objects.order_by('orders')[:3])

        # Recent User Orders
        recent_orders = Order.objects.order_by('dtime')[:3]
        context = {
            'total_earnings': earnings,
            'total_orders': orders,
            'total_products': products,
            'best_products': best_products,
            'recent_orders': recent_orders,
        }


        return render(request, 'dashboard.html', context)
    else:
        return redirect('login')

def manage(request):
    if request.user.is_superuser:
        username = request.user.username[0].title

        products = Product.objects.all()
        context = {
            'user': username,
            'products': products
        }
        return render(request, "manage_items.html", context)

    else:
        return redirect('login')


def activity(request):
    if request.user.is_superuser:
        username = request.user.username[0].title

        user_id = request.user.id
        orders = Order.objects.filter(user=user_id).all()
        reversed = 0
        completed = 0
        on_hold = 0
        for i in orders:
            if i.status == 'completed':
                completed += 1
            elif i.status == 'on-hold':
                on_hold += 1
            elif i.status == 'reversed':
                reversed += 1
                pass
        context = {
            'user': username,
            'orders': orders,
            'completed': completed,
            'reversed': reversed,
            'on_hold': on_hold,
        }

        return render(request, "order_activity.html", context)
    else:
        return redirect('login')


def uploadp1(request):
    if request.user.is_superuser:
        username = request.user.username

        if request.method == "POST":
            data = request.POST
            
            brand = data['brand']
            tagline = data['tagline']
            single_price = data['singlePrice']
            multiple_price = data['multiplePrice']
            extended_price = data['extendedPrice']
            gateway = request.POST.get('gateway', 'paddle')
            exclusive = request.POST.get('exclusive', 0)
            compatibility = data['compatibility']
            version = request.POST.get('version', 1.0)
            category = data['category']
            topic = data['topic']
            tags = data['tags']
            status = request.POST.get('status', 'pending')
            description = data['description']
            link = data['link']
            thumbnail = request.FILES.get('thumbnail')
            zipfile = request.FILES.get('zipfile')
            
            # Form validation
            if brand == '':
                messages.info(request, 'Brand field cannot be empty')
                return redirect('product_upload1')
            elif tagline == '':
                messages.info(request, 'Tagline field cannot be empty')
                return redirect('product_upload1')
            elif single_price == '':
                messages.info(request, 'Give your product a price (Single License)')
                return redirect('product_upload1')
            elif compatibility == '':
                messages.info(request, 'Compatibility field cannot be empty')
                return redirect('product_upload1')
            elif category == '':
                messages.info(request, 'Select the category of your product')
                return redirect('product_upload1')
            elif topic == '':
                messages.info(request, 'Select the topic of your product')
                return redirect('product_upload1')
            elif tags == '':
                messages.info(request, 'Tags cannot be empty (Used to promote your product)')
                return redirect('product_upload1')
            elif status == '':
                messages.info(request, 'status cannot be empty')
                return redirect('poduct_upload1')
            elif description == '':
                messages.info(request, 'Give a description to your product')
                return redirect('product_upload1')
            else:
                
                browser_support_ls = []
                css_type_ls = []
                layout_ls = []
                

                if 'chrome' in data:
                    browser_support_ls.append('chrome')
                if 'safari' in data:
                    browser_support_ls.append('safari')
                if 'edge' in data:
                    browser_support_ls.append('edge')
                if 'firefox' in data:
                    browser_support_ls.append('safari')
                if 'explorer10' in data:
                    browser_support_ls.append('explorer10')
                if 'explorer11' in data:
                    browser_support_ls.append('explorer11')
                
                if 'saas' in data:
                    css_type_ls.append('saas')
                if 'scss' in data:
                    css_type_ls.append('scss')
                if 'less' in data:
                    css_type_ls.append('less')
                
                if 'fixed' in data:
                    layout_ls.append('fixed')
                if 'responsive' in data:
                    layout_ls.append('responsive')
                if 'fluid' in data:
                    layout_ls.append('fluid')

                
                
                if len(browser_support_ls) < 1:
                    browser_support = "None"
                else:
                    browser_support = browser_support_ls
                
                if len(css_type_ls) < 1:
                    css_type = "None"
                else:
                    css_type = css_type_ls

                if len(layout_ls) < 1:
                    layout = "None"
                else:
                    layout = layout_ls

                
                if exclusive == 0:
                    list_price = float(single_price) + (60/100)*float(single_price)
                else:
                    list_price = float(single_price) + (20/100)*float(single_price)
                
                # Insert record into db
                Product.objects.create(
                    brand =brand,
                    tagline = tagline,
                    single_price = single_price,
                    multiple_price = multiple_price,
                    extended_price = extended_price,
                    list_price = list_price,
                    exlusive = exclusive,
                    gateway = gateway,
                    compatibility = compatibility,
                    version = version,
                    browser_support = browser_support,
                    layout = layout,
                    css_type = css_type,
                    category = category,
                    topic = topic,
                    tags = tags,
                    status = status,
                    description = description,
                    link = link,
                    thumbnail = thumbnail,
                    zipfile = zipfile, 
                    user = username
                )

                return redirect('home:manage_items')
        else:
            return render(request, "uploadp1.html")

    else:
        return redirect('login')



@csrf_exempt
@require_POST
def webhook(request):
    data1 = request.POST
    data = json.dumps(data1)
    print('\n', data, '\n')
    return HttpResponse('Under construction')



def categories(request):
    if request.user.is_superuser:
        name = request.user.username
        all_categories = Category.objects.order_by('dtime').all()[:6]

        context = {
            'name': name, 
            'all_categories': all_categories,
            'action': 'normal',
        }

        return render(request, 'category.html', context)
    
    else:
        return redirect('login')



def add_category(request):
    if request.user.is_superuser and request.method == 'POST':
        category = request.POST['category']
        slug = request.POST.get('slug', 'None')
        
        if category == '':
            messages.info(request, 'Category cannot be empty')
            return redirect('home:categories')
        elif Category.objects.filter(category_name=category):
            print(Category.objects.filter(category_name=category))
            messages.info(request, 'Category already exist')
            return redirect('home:categories')

        else:    
            Category.objects.create(
                category_name = category,
                slug = slug
            )

            messages.info(request, 'Category added successfully')
            return redirect('home:categories')

    else:
        return redirect('logout')
    


def edit_category(request):
    if request.user.is_superuser:
        if request.method == "POST":
            cat_id = request.POST['cat_id']
            if request.POST['category'] == '':
                messages.info(request, 'Category cannot be empty')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                cat = request.POST['category']
                slug = request.POST['slug']

                ins = Category.objects.filter(id=cat_id).update(
                    category_name = cat,
                    slug = slug
                )
                
                messages.info(request, 'Category updated successfully')
                return redirect('home:categories')
        else:
            cat_id = request.GET['cat_id']
            if cat_id == '':
                messages.info(request, 'Category ID cannot be empty')
                return redirect('home:categories')
            elif Category.objects.get(id=cat_id):
                category = Category.objects.get(id=cat_id)
                
                cont = {
                    'action': 'edit',
                    'category': category
                }
                print(category)
                return render(request, 'category.html', cont)
            else:
                messages.info(request, 'Category not Found!')
                return redirect('home:categories')
    else:
        return redirect('logout')



def remove_category(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if request.POST['cat_id'] == '':
                messages.info(request, 'Category cannot be found')
                return redirect('home:categories')
            else:
                cat_id = request.POST['cat_id']

                if Category.objects.filter(id=cat_id):
                    Category.objects.filter(id=cat_id).delete()
                    messages.info(request, 'Category removed successfully')
                    return redirect('home:categories')
                else:
                    messages.info(request, 'Category cannot be found')
                    return redirect('home:categories')
        else:
            return HttpResponse('Bad Request')
    else:
        return redirect('login')




def tags(request):
    if request.user.is_superuser:
        tags = Tag.objects.order_by('tag_name')[:10]
        return render(request, 'tags.html', {'tags': tags})
    
    else:
        return redirect('login')


def add_tags(request):
    if request.user.is_superuser:
        if request.method != "POST":
            return redirect('home:tags')
        
        else:
            tag = request.POST['tag']
            slug = request.POST['slug']

            if tag == '':
                messages.info(request, 'Tag Name cannot be empty')
                return redirect('home:tags')
            else:

                Tag.objects.create(
                    tag_name = tag,
                    slug = slug
                )

                messages.info(request, 'Tag inserted successfully')
                return redirect('home:tags')
    else:
        return redirect('login')


# deleting a product
def remove_product(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            if request.POST['prod_id'] == '':
                messages.info(request, 'Category cannot be found')
                return redirect('home:manage_items')
            else:
                prod_id = request.POST['prod_id']

                if Product.objects.filter(id=prod_id):
                    Product.objects.filter(id=prod_id).delete()
                    messages.info(request, 'product removed successfully')
                    return redirect('home:manage_items')
                else:
                    messages.info(request, 'product cannot be found')
                    return redirect('home:manage_items')
        else:
            return HttpResponse('Bad Request')
    else:
        return redirect('login')


# edit product
def edit_product(request):
    
    if request.user.is_superuser:
        name = request.user.username
        if request.method == "POST":
            prod_id = request.POST['prod_id']
            
            brand = request.POST['brand']
            tagline = request.POST['tagline']
            single_price = request.POST['singlePrice']
            multiple_price = request.POST['multiplePrice']
            extended_price = request.POST['extendedPrice']
            gateway = request.POST.get('gateway', 'paddle')
            exclusive = request.POST.get('exclusive', 0)
            compatibility = request.POST['compatibility']
            version = request.POST.get('version', 1.0)
            cat = request.POST['category']
            topic = request.POST['topic']
            tags = request.POST['tags']
            status = status = request.POST.get('status', 'pending')
            
           
            
            description = request.POST['description']
            link = request.POST['link']
            thumbnail = request.FILES.get('thumbnail')
            zipfile = request.FILES.get('zipfile')

            ins = Product.objects.filter(id=prod_id).update(
                brand =brand,
                tagline = tagline,
                single_price = single_price,
                multiple_price = multiple_price,
                extended_price = extended_price,
                exlusive = exclusive,
                gateway = gateway,
                compatibility = compatibility,
                version = version,
                
                
                
                category = cat,
                topic = topic,
                tags = tags,
                status = status,
                description = description,
                link = link,
                thumbnail = thumbnail,
                zipfile = zipfile, 
                user = name
            )
            
            messages.info(request, 'Product updated successfully')
            return redirect('home:manage_items')
        else:
            prod_id = request.GET['prod_id']
            if prod_id == '':
                messages.info(request, 'Product ID cannot be empty')
                return redirect('home:manage_items')
            elif Product.objects.get(id=prod_id):
                product = Product.objects.get(id=prod_id)
                
                cont = {
                    'action': 'edit',
                    'product': product
                }
                print(product)
                return render(request, 'uploadp1.html', cont)
            else:
                messages.info(request, 'Product not Found!')
                return redirect('home:manage_items')
    else:
        return redirect('login')


def all_users(request):
    if request.user.is_superuser:
        users = reversed(UserDetails.objects.all())
        context = {
            'users': users,
        }
        return render(request, 'all_users.html', context)
    else:
        return redirect('login')
