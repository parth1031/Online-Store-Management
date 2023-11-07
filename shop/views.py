from math import ceil
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Products, Customers, cartitems, cart, wishlist, wishlistitems
from django.db.models import Q


# Create your views here.


def index(request):
    trending = Products.objects.filter(sub_category='trending')

    featured = Products.objects.filter(sub_category='featured')

    arrival = Products.objects.filter(sub_category='new arrivals')

    params = {'trending': list(trending), 'featured': list(featured), 'arrival': list(arrival)}
    return render(request, 'shop/indextrial.html', params)


def register_customer(username, phone, add, key):
    new_customer = Customers(user=username, phone_number=phone, address=add, security_key=key)
    new_customer.save()


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'shop/Login page.html')


def LogoutPage(request):
    logout(request)
    return redirect('/login')


def signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['Phone_number']
        address = request.POST['address']
        key = request.POST['key']
        print(fname)
        print(lname)
        print(email)
        print(username)
        print(password1)
        print(password2)
        print(phone_number)
        print(address)
        print(key)

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                # username already exists
                messages.error(request, "username already exists")
                return render(request, 'shop/Signup page.html')
            elif User.objects.filter(email=email).exists():
                # email already exists
                messages.error(request, "email already exists")
                return render(request, 'shop/Signup page.html')

            user = User.objects.create_user(username=username, email=email, password=password1, first_name=fname,
                                            last_name=lname)
            user.save()
            uname = User.objects.get(username=username)
            print(uname)
            print("reaching here")
            register_customer(uname, phone_number, address, key)
            print("reaching here also")

            return redirect('/login')
        else:
            messages.error(request, "both passwords should match!!")

    return render(request, 'shop/Signup page.html')


def forget(request):
    if request.method == 'POST':

        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone']
        key2 = request.POST['key']
        customer_data = Customers.objects.get(user__username=username)

        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                # username already exists
                messages.error(request, "username not exists")
                return render(request, 'shop/forget.html')

            elif phone_number != customer_data.phone_number:
                messages.error(request, "phone number should match")
                return render(request, 'shop/forget.html')

            elif key2 != customer_data.security_key:
                messages.error(request, "key should match")
                return render(request, 'shop/forget.html')

            user = User.objects.get(username=username)
            new_password = password1

            # Change the user's password
            user.set_password(new_password)

            # Save the user object 
            user.save()

            return redirect('/login')
        else:
            messages.error(request, "both passwords should match!!")

    return render(request, 'shop/forget.html')


def ProductView(request, id):
    # fetch the product using id
    product = Products.objects.filter(product_id=id)
    category = product[0].category
    price = product[0].price
    discount = product[0].discount
    mrp = int(price) // (1 - (int(discount) / 100))

    CatProds = Products.objects.filter(category=category).exclude(product_id=id)
    n = len(CatProds)
    nSlides = n // 3 + ceil((n / 3) - (n // 3))

    return render(request, 'shop/product.html',
                  {'product': product[0], 'CatProds': CatProds, 'no_of_slides': nSlides, 'range': range(1, nSlides),
                   'mrp': mrp}, )


# def wishlist(request):
#     return render(request,'shop/index.html')

@login_required(login_url='/login/')
def add_to_cart(request, id):
    
    product = Products.objects.get(product_id=id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        
        user_cart, created = cart.objects.get_or_create(user=user)

        
        cart_item, created = cartitems.objects.get_or_create(cart=user_cart, user=user, product=product)

        if not created:
            
            cart_item.quantity += 1

        else:
            
            cart_item.price = product.price

        cart_item.save()

        
        user_cart.total_quantity += 1
        user_cart.total_price += product.price
        user_cart.save()

        return ProductView(request, id)  
    else:
        
        return redirect('login')  


def update_quantity(request, product_id):
    try:
        cart_items = cartitems.objects.get(product__product_id=product_id)
    except cartitems.DoesNotExist:
        return redirect('cart')

    new_quantity = int(request.GET.get(f'quantity_{product_id}', 0))
    print(new_quantity)
    user=request.user
    user_cart = cart.objects.get(user=user)

    user_cart.total_quantity -= cart_items.quantity
    user_cart.total_price -= cart_items.quantity * cart_items.price
    print(user_cart.total_quantity)

    if new_quantity == 0:
        cart_items.delete()
    else:
        cart_items.quantity = new_quantity
        cart_items.save()
        print(cart_items.quantity)
        user_cart.total_quantity += cart_items.quantity
        print(user_cart.total_quantity)
        user_cart.total_price += cart_items.quantity * cart_items.price

    user_cart.save()
    return cart_view(request)

@login_required(login_url='/login/')
def cart_view(request):
    user = request.user

    try:
        user_cart = cart.objects.get(user=user)
        cart_items = cartitems.objects.filter(cart=user_cart)
        total_price = user_cart.total_price
        total_quantity = user_cart.total_quantity
    except cart.DoesNotExist:
        user_cart = None
        cart_items = []
        total_price = 0
        total_quantity = 0

    context = {
        'user_cart': user_cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    }

    return render(request, 'shop/shopping cart trial.html', context)

@login_required(login_url='/login/')
def add_to_wish(request, product_id):
    # Retrieve the product you want to add to the cart
    product = Products.objects.get(product_id=product_id)

    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        # Get or create the user's wishlist
        user_wishlist, created = wishlist.objects.get_or_create(user=user)

        # Check if the product is already in the user's wishlist
        wishlist_item, created = wishlistitems.objects.get_or_create(wishlist=user_wishlist, user=user, product=product)

        if created:
            wishlist_item.price = product.price
            wishlist_item.save()

            # Update the total quantity and total price in the user's wishlist
            user_wishlist.total_quantity += 1
            user_wishlist.total_price += product.price
            user_wishlist.save()
        return ProductView(request, product_id)
    else:
        return redirect('login')

@login_required(login_url='/login/')
def wishlist_view(request):
    user = request.user

    try:
        user_wishlist = wishlist.objects.get(user=user)
        wishlist_items = wishlistitems.objects.filter(wishlist=user_wishlist)
        # total_price = user_wishlist.total_price
        # total_quantity = user_.total_quantity
    except wishlist.DoesNotExist:
        user_wishlist = None
        wishlist_items = []

    context = {
        'user_wishlist': user_wishlist,
        'wishlist_items':wishlist_items,

    }

    return render(request, 'shop/wishlist.html', context)


def move_all_to_cart(request):
    user = request.user
    wishlist_items = wishlistitems.objects.filter(user=user)
    print(wishlist_items)

    for wishlist_item in wishlist_items:
        product = wishlist_item.product
        try:
            user_cart = cart.objects.get(user=user)
            cart_item = cartitems.objects.get(cart=user_cart, product=product)
            # If the product is in the cart, don't duplicate it; just increase the quantity
            cart_item.quantity += 1

            cart_item.save()
            user_cart.total_quantity += 1
            user_cart.total_price += product.price

        except cart.DoesNotExist or cartitems.DoesNotExist:
            # If the user doesn't have a cart, create one and add the product
            if cart.DoesNotExist:
                user_cart = cart.objects.create(user=user)
                cart_item = cartitems.objects.create(cart=user_cart, user=user, product=product, price=product.price,
                                                     quantity=1)
                user_cart.totalquantity += 1
                user_cart.total_price += product.price

            else:
                cart_item = cartitems.objects.create(cart=user_cart, user=user, product=product, price=product.price,
                                                     quantity=1)
                user_cart.totalquantity += 1
                user_cart.total_price += product.price

        except cartitems.DoesNotExist:
            # If the product is not in the cart, create a new cart item
            cart_item = cartitems.objects.create(cart=user_cart, user=user, product=product, price=product.price,
                                                 quantity=1)
            user_cart.total_quantity += 1
            user_cart.total_price += product.price

        # Remove the product from the wishlist
        wishlist_item.delete()
        user_cart.save()

    return wishlist_view(request)  # Redirect to the wishlist page


def delete_from_wishlist(request, product_id):
    wishlist_item = wishlistitems.objects.get(user=request.user, product_id=product_id)
    wishlist_item.delete()

    return wishlist_view(request)
# def search(request):
#     return render(request,'shop/index.html')
def home(request):
    return index(request)


def search(request):
    search = request.GET.get('search')

    if not search:
        # If the search query is empty, redirect to the home page
        return redirect('/home/')

    res = Products.objects.filter(Q(product_name=search) | Q(category=search) | Q(sub_category=search))

    if res.exists():
        
        best_prod = res[0]
        id = best_prod.product_id
        return ProductView(request, id)
    else:
        
        return redirect('/home/')

def checkout(request):
    
    try:
        user_customer = Customers.objects.get(user=request.user)
        address = user_customer.address
    except Customers.DoesNotExist:
        address = ""

    # Get the user's cart
    try:
        user_cart = cart.objects.get(user=request.user)
        total_quantity = user_cart.total_quantity
        total_price = user_cart.total_price

        user_cart.total_price=0
        user_cart.total_quantity=0

        # Delete all products in the user's cart
        user_cart.cartitems_set.all().delete()
        user_cart.save()
    except cart.DoesNotExist:
        total_quantity = 0
        total_price = 0

    messages.success(request, "All the "+str(total_quantity)+" have been dispatched and they will reach "+str(address)+" in few days.")

    return render(request, 'shop/shopping cart trial.html')