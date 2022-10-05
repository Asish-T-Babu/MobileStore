from unicodedata import category
from django.shortcuts import render,redirect
from .models import *
from django.shortcuts import render,redirect
import random
from .models import Users
from django.contrib import messages
import datetime
from django.core.paginator import *
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import json
from django.http import JsonResponse
import razorpay
from django.contrib import messages
from twilio.rest import Client
from django.utils import timezone
from django.views.decorators.csrf  import csrf_exempt
import string

# Create your views here.
def index(request):
    a=product.objects.all()
    for i in a:
        i.price=i.actual_price_category
        i.save()
    now=datetime.datetime.now().strftime('%Y-%m-%d')
    print(now)
    products=product.objects.all()
    for k in products:
        try:
            p_offer=Product_offer.objects.get( start_date_and_time__lte=now,end_date_and_time__gte=now,product=k.id)
            try:
                c_offer=Category_offer.objects.get( start_date_and_time__lte=now,end_date_and_time__gte=now,Category=k.cat_id)
                if int(p_offer.discount_percentage) > int(c_offer.discount_percentage):
                    print("p_offer.discount_percentage > c_offer.discount_percentage",p_offer.discount_percentage,c_offer.discount_percentage)
                    calculating_discount=int(p_offer.discount_percentage)*k.actual_price_category/100
                    k.price=k.actual_price_category-calculating_discount
                    k.save()
                elif int(p_offer.discount_percentage) < int(c_offer.discount_percentage):
                    print("p_offer.discount_percentage < c_offer.discount_percentage",p_offer.discount_percentage,c_offer.discount_percentage)
                    calculating_discount=int(c_offer.discount_percentage)*k.actual_price_category/100
                    k.price=k.actual_price_category-calculating_discount
                    k.save()
                elif int(p_offer.discount_percentage) == int(c_offer.discount_percentage):
                    print("p_offer.discount_percentage == c_offer.discount_percentage",p_offer.discount_percentage,c_offer.discount_percentage)
                    calculating_discount=int(p_offer.discount_percentage)*k.actual_price_category/100
                    k.price=k.actual_price_category-calculating_discount
                    k.save()
            except:
                p_offer=Product_offer.objects.get( start_date_and_time__lte=now,end_date_and_time__gte=now,product=k.id)
                calculating_discount=int(p_offer.discount_percentage)*k.actual_price_category/100
                k.price=k.actual_price_category-calculating_discount
                k.save()
        except:
            try:
                c_offer=Category_offer.objects.get( start_date_and_time__lte=now,end_date_and_time__gte=now,Category=k.cat_id)
                calculating_discount=int(c_offer.discount_percentage)*k.actual_price_category/100
                k.price=k.actual_price_category-calculating_discount
                k.save()
            except:
                pass
            

    # c_offer=Category_offer.objects.filter( start_date_and_time__lte=now,end_date_and_time__gte=now)
    # print(c_offer)
    # if c_offer:
    #     for i in c_offer:
    #         apply_category_product=product.objects.filter(cat_id=i.Category)
    #         for j in apply_category_product:
    #             calculating_discount=int(i.discount_percentage)*j.actual_price_category/100
    #             print("calculating_discount",calculating_discount)
    #             j.price=j.actual_price_category-calculating_discount
    #             j.save()
    
    # p_offer=Product_offer.objects.filter( start_date_and_time__lte=now,end_date_and_time__gte=now)
    # print(p_offer)
    # if p_offer:
    #     for i in p_offer:
    #         apply_category_product_offer=product.objects.filter(id=i.product.id)
    #         for j in apply_category_product_offer:
    #             calculating_discount=int(i.discount_percentage)*j.actual_price_category/100
    #             j.price=j.actual_price_category-calculating_discount
    #             j.save()
    if 'user_id' in request.session:
        data=product.objects.all()[:3]
        return render(request, 'index1.html',{'data':data})
    data=product.objects.all()[:3]
    return render(request, 'index.html',{'data':data})

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user=Users.objects.filter(username=username,password=password)
        if user:
            status=Users.objects.get(username=username,password=password)
            print(status.username,status.status)
            if status.status == True:
                print("hi ajo",status.id)
                request.session['user_id']=status.id
                s=request.session.get('user_id')
                return redirect(index)
            else:
                return redirect(login)
            
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def login_home(request):
    if request.method=='POST':
        username = request.POST['username']
        otp=request.session.get('otp')
        print(otp,username)
        print(type(otp),type(username))
        if(int(username)==otp):
            uname=request.session.get('uname')
            user=Users.objects.get(phone=uname)
            request.session['user_id']=user.id
            return redirect(index)
    return render(request, 'login_home.html')

def login_otp(request):
    if request.method=='POST':
        username = request.POST['username']
        user=Users.objects.filter(phone=username)
        if user:
            otp= random.randint(1000,9999)
            account_sid = "ACea1db142f98a1e87384255b29ee82e18"
            auth_token = 'a9348108964e344da16c1874447dca33'
            client = Client(account_sid,auth_token)
            msg = client.messages.create(
                body = f"Your OTP is {otp}",
                from_ = "+16304488428",
                to = "+919188109889"
            )
            request.session['otp']=otp
            request.session['uname']=username
            return redirect(login_home)
        else:
            return redirect(insert)
    return render(request, 'login_otp.html')

def home(request):
    return render(request, 'home.html')

def insert(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        referal_code=request.POST['referal_code']
        if referal_code:
            user_table=Users.objects.filter(referal=referal_code)
            if user_table:
                pass
            else:
                messages.info(request,'Enter a valid Referal Code')
                return redirect(insert)
        if Users.objects.filter(email=email).exists():
            messages.info(request,'Email already exist')
            return redirect(insert)
        phone = request.POST['phone']
        if Users.objects.filter(email=email).exists():
            messages.info(request,'Email already exist')
            return redirect(insert)
        username = request.POST['username']
        if Users.objects.filter(username=username).exists():
            messages.info(request,'Username is not available')
            return redirect(insert)
        password = request.POST['password']
        S = 10
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
        reg=Users.objects.create(name=name,email=email,phone=phone,username=username,password=password,referal=ran)
        reg.save()
        if referal_code:
            if user_table:
                wal=Wallet()
                wal.user=reg
                wal.wallet_amount=40
                wal.save()
                one_user=Users.objects.get(referal=referal_code)
                refered_wallet=Wallet.objects.get(user=one_user.id)
                refered_wallet.wallet_amount=refered_wallet.wallet_amount+100
                refered_wallet.save()
            else:
                wal=Wallet()
                wal.user=reg
                wal.wallet_amount=0
                wal.save()
        else:
            wal=Wallet()
            wal.user=reg
            wal.wallet_amount=0
            wal.save()
        return redirect(login)
    return render(request, 'register.html')

def products(request):
    data1=add_category.objects.all()
    if request.method=='POST':
        search = request.POST['search']
        print("hdsgajfhjkshdjasdhgklrahgkhkrdhagkjraehgjkrehnjgkhekjghke",search)
        if len(search) == 0:
            data=product.objects.all() 
            return render(request, 'products.html',{'data':data})
        data=product.objects.filter(product_name__icontains=search)
        return render(request, 'products.html',{'data':data})
    data=product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.session.get('user_id'):
        return render(request,'products1.html',{'data':users,'data1':data1})
    return render(request,'products.html',{'data':users,'data1':data1})

def view_product(request):
    data=product.objects.all()
    return render(request,'list_product.html',{'data':data})

def product_details(request,id):
    if request.method == "POST":
        if 'user_id' in request.session:

            if request.POST.get('cart_button'):
                user_id=request.session.get('user_id')
                cart_for_check=Cart.objects.filter(user_id=user_id,product_id=id)
                if cart_for_check:
                    cart_last=Cart.objects.get(user_id=user_id,product_id=id)
                    cart_last.quantity=int(cart_last.quantity)+1
                    cart_last.save()
                else:
                    product_id=id
                    quantity=1
                    print("Hello Asish",user_id,product_id,quantity)
                    data1=Users.objects.get(id=user_id)
                    data2=product.objects.get(id=product_id)
                    my_cart=Cart.objects.create(user_id=data1,product_id=data2,quantity=quantity)
                    my_cart.save()
            if request.POST.get('wishlist_button'):
                user_id=request.session.get('user_id')
                product_id=id
                data1=Users.objects.get(id=user_id)
                data2=product.objects.get(id=product_id)
                my_wishlist=Wishlist.objects.create(user_table=data1,product_table=data2)
                my_wishlist.save()
        else:
            return redirect(login)
    data=product.objects.get(id=id)
    if 'user_id' in request.session:
        return render(request,'product_details1.html',{'data':data})
    return render(request,'product_details.html',{'data':data})
    

def logout(request):
    if 'user_id' in request.session:
        request.session.flush()
    return redirect(index)

def view_cart(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        a=0                                                          
        for i in cart:
            a = a+i.product_id.price*int(i.quantity)
        if request.method == "POST":
            if cart:
                return redirect(checkout)
            else:
                return redirect(view_cart)
        return render(request,'view_cart.html',{'cart':cart,'total':a})
    return redirect(login)

def add_quantity(request,id):
    data=Cart.objects.get(id=id)
    data.quantity=int(data.quantity)+1
    data.save()
    return redirect(view_cart)

def sub_quantity(request,id):
    data=Cart.objects.get(id=id)
    f=int(data.quantity)
    if f != 1:
        data.quantity=int(data.quantity)-1
    else:
        pass
    data.save()
    return redirect(view_cart)

def delete_from_cart(request,id):
    data=Cart.objects.get(id=id)
    data.delete()
    return redirect(view_cart)

def checkout(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        wallet=Wallet.objects.get(user=id)
        if cart:
            id = request.session.get('user_id')
            cart=Cart.objects.filter(user_id=id)
            a=0
            for i in cart:
                a = a+i.product_id.price*int(i.quantity)
            coupan_price=0
            total1=a
            if 'coupan_session' in request.session:
                coupan_id=request.session.get('coupan_session')
                request.session['not_valid']=coupan_id
                del request.session['coupan_session']
            if 'not_valid' in request.session:
                coupan_id=request.session.get('not_valid')
                coupan_obj=Coupan.objects.get(id=coupan_id)
                coupan_price=coupan_obj.discount_amount
                a=a - int(coupan_price)
            address=Address.objects.filter(user_id=id)
            if request.method=='POST':
                payment_method=request.POST['payment_method']
                selected_address_id=request.POST.get('selected_address')
                wallet_amount_applied=request.POST.get('wallet_amount_applied')
                if wallet_amount_applied:
                    if wallet.wallet_amount>a:
                        a=0
                    else:                    
                        a=a-int(wallet_amount_applied)
                print("selected_Address_id",selected_address_id)
                request.session['address_session']=selected_address_id
                print("selected_address_id_using_session",request.session.get('address_session'))
                if payment_method == 'paypal':
                    return redirect(payment_methods,a)
                user_id = request.session.get('user_id')
                data1=Users.objects.get(id=user_id)
                reg=Payment()
                reg.user=data1
                if payment_method == 'COD':
                    reg.payment_method=payment_method
                    reg.status='pending'
                    if 'not_valid' in request.session:
                        user=data1.id
                        if 'not_valid' in request.session:
                            b=request.session.get('not_valid')
                            print("cod_coupan_id",b)
                            cou=Coupan_applied.objects.create(coupan=b,user=user)
                            cou.save()
                            del request.session['not_valid']
                reg.save()
                data=Order()
                if wallet_amount_applied:
                    wallet.wallet_amount=0
                    # wallet.wallet_amount=0
                    # if wallet.wallet_amount<a:
                    #     wallet.wallet_amount=0
                    # else:
                    #     wallet.wallet_amount=wallet.wallet_amount-a
                    #     wallet.save()
                    wallet.save()
                data.user=data1
                data.payment=reg
                selected_address_id=request.session.get('address_session')
                print("rijin raju",selected_address_id)
                data.address=Address.objects.get(id=selected_address_id)
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                data.order_number = current_date + str(reg.id)
                data.order_total=a
                data.save()
                for i in cart:
                    data2=OrderProduct()
                    data2.order=data
                    data2.payment=reg
                    data2.user=data1
                    data2.product=product.objects.get(id=i.product_id.id)
                    data2.quantity=i.quantity
                    data2.product_price=i.product_id.price
                    data2.save()
                if payment_method == 'razorpay':
                    return redirect(payment_methods_razorpay, reg.pk) 
                for item in cart:
                    product1 = product.objects.get(id=item.product_id.id)
                    product1.stock -= int(item.quantity)
                    product1.save()                    
                cart.delete()
                return render(request,'order_successfully.html')
            return render(request,'checkout.html',{'cart':cart,'total':a,'address':address,'coupan_price':coupan_price,'total1':total1,'wallet':wallet})
        else:
            return redirect(view_cart)
    else:
        return redirect(login)

def add_address(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        buyer_name = request.POST['b_name']
        buyer_phone = request.POST['b_phone']
        address=request.POST['b_address']
        pincode=request.POST['b_pincode']
        city=request.POST['b_city']
        state=request.POST['b_state']
        country="india"
        reg=Address.objects.create(user_id=user_id,buyer_name=buyer_name,buyer_phone=buyer_phone,address=address,pincode=pincode,city=city,state=state,country=country)
        reg.save()
        return redirect(checkout)
    return render(request,'address.html')   

def view_wishlist(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        wishlist=Wishlist.objects.filter(user_table=id)
        return render(request,'view_wishlist.html',{'wishlist': wishlist})
    return redirect(login)

def delete_from_wishlist(request,id):
    data=Wishlist.objects.get(id=id)
    data.delete()
    return redirect(view_wishlist)

def my_profile(request):
    user_id=request.session.get('user_id')
    data=Users.objects.get(id=user_id)
    return render(request,'my_profile.html',{'data':data})

def address_management(request):
    user_id=request.session.get('user_id')
    data=Address.objects.filter(user_id=user_id)
    return render(request,"address_management.html",{'data':data})

def delete_address(request,id):
    data=Address.objects.get(id=id)
    data.delete()
    return redirect(address_management)

def edit_profile(request,id):
    data = Users.objects.get(id=id)
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        if Users.objects.filter(email=email).exists():
            check = Users.objects.get(email=email)
            print("msg", check.email, check.id, type(check.id))
            print(id, type(id))

            if int(id) == check.id:
                print(id, check.id)
            else:
                messages.info(request,'Email already exist')
                return redirect(edit_profile,id)
        username = request.POST['username']
        if Users.objects.filter(username=username).exists():
            check = Users.objects.get(username=username)
            print("msg", check.email, check.id, type(check.id))
            print(id, type(id))

            if int(id) == check.id:
                print(id, check.id)
            else:
                messages.info(request,'Username already exist')
                return redirect(edit_profile,id)
        password = request.POST['password']
        data_tb=Users.objects.get(id=id)
        data_tb.name=name
        data_tb.email=email
        data_tb.username=username
        data_tb.password=password
        data_tb.save()
        messages.info(request,'Updated successfully')
        return redirect(edit_profile,id)
    return render(request,"update.html",{'data':data})

def user_order_management(request):
    user_id=request.session.get('user_id')
    data=OrderProduct.objects.filter(user=user_id)
    for i in data:
        print(i.status)
    return render(request,'user_order_management.html',{'data':data})

def user_cancel_order(request,id):
    data=OrderProduct.objects.get(id=id)
    print("gfshjkghkshgbklrshk",data)
    data.ordered=True
    data.save()
    return redirect(user_order_management)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def download(request,productID):
    v=OrderProduct.objects.get(id=productID)
    mydict={
        'customerName':v.user.name,
        'customerEmail':v.user.email,
        'customerMobile':v.user.phone,
        'shipmentAddress':v.order.address.address,
        'orderStatus':v.status,
        'productimage':v.product.image1,
        'productName':v.product.product_name,
        'productPrice':v.product.price,
        'productDescription':v.product.p_description,
    }
    return render_to_pdf('download.html',mydict)

def user_order_detailed_view(request,id):
    data=OrderProduct.objects.get(id=id)
    return render(request,'user_order_detailed_view.html',{'i':data})

def payment_methods(request,order_total):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        print("cart 123",cart)
        # order = Order.objects.get(payment_id=id)
        a= order_total
        # if 'not_valid' in request.session:
        #     coupan_id=request.session.get('not_valid')
        #     coupan_obj=Coupan.objects.get(id=coupan_id)
        #     coupan_price=coupan_obj.discount_amount
        #     a=a - int(coupan_price)
    return render(request,'paypal_checkout.html',{'cart':cart,'total':a})

def payment_confirm(request,order_total):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        user_id = request.session.get('user_id')
        data1=Users.objects.get(id=user_id)
        body = json.loads(request.body)
        print("nothing to worry",body)
        reg=Payment()
        reg.user=data1
        reg.payment_id = body['transId']
        reg.payment_method = 'Paypal'
        reg.amount_paid = order_total
        reg.status= body['status']
        reg.save()
        if 'not_valid' in request.session:
            user=data1.id
            b=request.session.get('not_valid')
            print("cod_coupan_id",b)
            cou=Coupan_applied.objects.create(coupan=b,user=user)
            cou.save()
            del request.session['not_valid']
        data=Order()
        data.user=data1
        data.payment=reg
        selected_address_id=request.session.get('address_session')
        print("rijin raju",selected_address_id)
        data.address=Address.objects.get(id=selected_address_id)
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        data.order_number = current_date + str(reg.id)
        data.order_total=order_total
        data.save()
        for i in cart:
            data2=OrderProduct()
            data2.order=data
            data2.payment=reg
            data2.user=data1
            data2.product=product.objects.get(id=i.product_id.id)
            data2.quantity=i.quantity
            data2.product_price=i.product_id.price
            data2.save()  
        for item in cart:
            product1 = product.objects.get(id=item.product_id.id)
            product1.stock -= int(item.quantity)
            product1.save()                  
        cart.delete()
        data={
            'transId': reg.payment_id,
        }
        return JsonResponse(data)       

def payment_complete(request):
     return render(request,'order_successfully.html')

def payment_methods_razorpay(request,id):
    print(id)
    if 'razorpay_payment_for_order' in request.session:
        del request.session['razorpay_payment_for_order']
    if 'user_id' in request.session:
        usrr=request.session.get('user_id')
        user=Users.objects.get(id=usrr)
        order = Order.objects.get(payment_id=id)
        a= order.order_total
        # if 'not_valid' in request.session:
        #     coupan_id=request.session.get('not_valid')
        #     coupan_obj=Coupan.objects.get(id=coupan_id)
        #     coupan_price=coupan_obj.discount_amount
        #     a=a - int(coupan_price)
        client = razorpay.Client(auth=("rzp_test_PinpVqIdosJzfO","Mhck0Csm86cu12nRGtFyTTKK"))

        data = { "amount": a*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        cart = OrderProduct.objects.filter(payment_id=id)
        print("cart 123",cart)
        request.session['razorpay_payment_for_order']=payment
        
    return render(request,'razorpay_checkout.html',{'cart':cart,'total':a,'Razorpay_payment_id':id,'order':order,'payment':payment})

def filter_product(request,id):
    print(id)
    data1=add_category.objects.all()
    data=product.objects.filter(cat_id=id)
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.session.get('user_id'):
        return render(request,'products1.html',{'data':users,'data1':data1})
    return render(request,'products.html',{'data':users,'data1':data1})

def apply_coupan(request):
    if 'user_id' in request.session:
        user=request.session.get('user_id')
        if request.method=='POST':
            coupan_code = request.POST['coupan_code']
            c=Coupan.objects.filter(coupan_code=coupan_code)
            if c:
                coupan=Coupan.objects.get(coupan_code=coupan_code)
                d=Coupan_applied.objects.filter(coupan=coupan.id,user=user)
                if d:
                    messages.info(request,'Already Applied Coupon Code')
                    return render(request,'apply_coupan.html')
                now = timezone.now()
                start_date_and_time=coupan.start_date_and_time
                if start_date_and_time < now:
                    if now < coupan.end_date_and_time:
                        coupan_id=coupan.id
                        print(coupan_code,coupan_id)
                        request.session['coupan_session']=coupan_id
                        return redirect(checkout)
                    else:
                        messages.info(request,'Coupon Expired')
                        return render(request,'apply_coupan.html')
                else:
                    messages.info(request,'Coupon is from coupan.start_date_and_time ')
                    return render(request,'apply_coupan.html')
            else:
                messages.info(request,'invalid Coupon Code')
                return render(request,'apply_coupan.html')        
        return render(request,'apply_coupan.html')
    else:
        return redirect(login)

@csrf_exempt
def razor_pay(request,id):
    if 'user_id' in request.session:
        order = Order.objects.get(payment_id=id)
        userid=request.session.get('user_id')
        user=Users.objects.get(id=userid)
        payment=request.session.get('razorpay_payment_for_order')
        pay = Payment.objects.get(id=id)
        pay.payment_method = 'razorpay'
        pay.status = payment['status']
        pay.payment_id = payment['id']
        pay.user = user
        actual_amount=payment['amount']
        actual_amount=actual_amount/100
        pay.amount_paid = actual_amount
        pay.save()
        cart1=Cart.objects.filter(user_id=userid)
        for item in cart1:
            product1 = product.objects.get(id=item.product_id.id)
            product1.stock -= int(item.quantity)
            product1.save()   
            cart1.delete()
        if 'razorpay_payment_for_order' in request.session:
            del request.session['razorpay_payment_for_order']
    return render(request,'order_successfully.html')

def user_order_returned(request,id):
    if 'user_id' in request.session:
        order= Order.objects.get(id=id)
        order.status = 'Returned'
        order.save()
    return redirect(user_order_management)
