from urllib import response
from django.shortcuts import render,redirect
from user_app.models import *
from django.contrib.auth import authenticate
import os
from django.core.paginator import *
import xlwt
import datetime
from django.http import HttpResponse
from django.template.loader import *
from django.db.models import Count,Sum
from xhtml2pdf import pisa
from django.contrib import messages

# from user_app.models import add_category,category_by_price

# Create your views here.
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            request.session['username']=username
            return redirect(admin_home)
        else:
            print('invalid credentials')
    return render(request,'admin_login.html')

def admin_home(request):
    y=[]
    z=[]
    a=product.objects.all()
    for i in a:
        b=i.id
        c=OrderProduct.objects.filter(product=b).count()
        y.append(i.product_name)
        z.append(c)
    print(y,z)
    return render(request, 'admin_home.html',{'labels':y,'data':z})

def block(request,id):
    data = Users.objects.get(id=id)
    data.status=False
    data.save()
    return redirect(admin_view_users)

def unblock(request,id):
    print(type(id))
    data = Users.objects.get(id=id)
    data.status=True
    data.save()
    return redirect(admin_view_users)
    
def category_add(request):
    if request.method == 'POST':
        category = request.POST['category']
        print("hello",category)
        reg=add_category.objects.create(category_name=category)
        reg.save()
        messages.info(request,'Created successfully')
    return render(request,'category_add.html')

# def category_price(request):
#     if request.method == 'POST':
#         pro=category_by_price()
#         pro.memory=request.POST.get('memory')
#         c_id=request.POST.get('category')
#         pro.cat_id = add_category.objects.get(id=c_id)
#         print("hello",cars)
#         # if len(request.FILES):
#         pro.image1 = request.FILES.get('img1')
#         pro.save()
#     data=add_category.objects.all()
#     return render(request,'category_by_price.html',{'data':data})

def add_product(request):
    if request.method=='POST':
        product_id = request.POST.get('p_id')
        product_name = request.POST.get('p_name')
        p_description = request.POST.get('p_description')
        price = request.POST.get('pric')
        print("price",price)
        ram = request.POST.get('ram')
        storage = request.POST.get('storage')
        c_id=request.POST.get('c_id')
        print("stock",c_id)
        stock=request.POST.get('stock')
        cat_id = add_category.objects.get(id=c_id)
        image1 = request.FILES.get('img1')
        image2 = request.FILES.get('img2')
        image3 = request.FILES.get('img3')
        image4 = request.FILES.get('img4')
        c=product.objects.create(product_id=product_id,product_name=product_name,p_description=p_description,actual_price=price,actual_price_category=price,price=price,stock=stock,ram=ram,storage=storage,cat_id=cat_id,image1=image1,image2=image2,image3=image3,image4=image4)
        c.save()
    data=add_category.objects.all()
    return render(request, 'add_product.html',{'data':data})

def list_product(request):
    if request.method=='POST':
        search = request.POST['search']
        print("hdsgajfhjkshdjasdhgklrahgkhkrdhagkjraehgjkrehnjgkhekjghke",search)
        if len(search) == 0:
            data=product.objects.all() 
            page = request.GET.get('page', 1)
            paginator = Paginator(data, 1)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            return render(request,'list_product.html',{'data':users})
        data=product.objects.filter(product_name__icontains=search)
        return render(request, 'list_product.html',{'data':data})
    data=product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'list_product.html',{'data':users})

def updaterow(request,id):
    data1=product.objects.get(id=id)
    if request.method == 'POST':
        data2=product.objects.get(id=id)
        pro=product(id=id)
        pro.product_id = request.POST.get('p_id')
        pro.product_name = request.POST.get('p_name')
        pro.p_description = request.POST.get('p_description')
        pro.price = request.POST.get('price')
        pro.ram = request.POST.get('ram')
        pro.storage = request.POST.get('storage')
        pro.cat_id=data2.cat_id
        if len(request.FILES) != 0:
            pro.image1 = request.FILES.get('img1')
            pro.image2 = request.FILES.get('img2')
            pro.image3 = request.FILES.get('img3')
            pro.image4 = request.FILES.get('img4')
        pro.save()
    data=add_category.objects.all()
    return render(request,'edit_product.html',{'data':data,'data1':data1})

def deleterow(request,id):
    data=product.objects.get(id=id)
    if len(data.image1) > 0:
        os.remove(data.image1.path)
    if len(data.image2) > 0:
        os.remove(data.image2.path)
    if len(data.image3) > 0:
        os.remove(data.image3.path)
    if len(data.image4) > 0:
        os.remove(data.image4.path)
    data.delete()
    return redirect(list_product)


def admin_view_users(request):
    if request.method=='POST':
        search = request.POST['search']
        print("hdsgajfhjkshdjasdhgklrahgkhkrdhagkjraehgjkrehnjgkhekjghke",search)
        if len(search) == 0:
            data=Users.objects.all().order_by('id')
            page = request.GET.get('page', 1)
            paginator = Paginator(data, 1)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            return render(request, 'admin_view_users.html',{'data':users})
        data=Users.objects.filter(name__icontains=search)
        page = request.GET.get('page', 1)
        paginator = Paginator(data, 1)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(request, 'admin_view_users.html',{'data':users})
    data=Users.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'admin_view_users.html',{'data':users})

def admin_order_management(request):
    data=OrderProduct.objects.filter(ordered=False)
    return render(request,'admin_order_management.html',{'data':data})

def admin_cancel_order(request,id):
    data=OrderProduct.objects.get(id=id)
    data.ordered=True
    data.save()
    return redirect(admin_order_management)

def admin_order_detailed_view(request,id):
    data=OrderProduct.objects.get(id=id)
    if request.method == 'POST':
        status=request.POST.get('status_update_adminside')
        print("status",status)
        data=OrderProduct.objects.get(id=id)
        if status == 'Out for Delivery':
            data.out_for_delivery = datetime.datetime.now()
        data.status=status
        data.save()
    return render(request,'admin_order_detailed_view.html',{'i':data})

def filter_order(request,status):
    data=OrderProduct.objects.filter(ordered=False,status=status)
    return render(request,'admin_order_management.html',{'data':data})

def admin_logout(request):
    return redirect(admin_login)

def coupan_management(request):
    if request.method=='POST':
        coupan_code = request.POST.get('c_code')
        start_date_and_time = request.POST.get('s_date')
        end_date_and_time = request.POST.get('e_date')
        discount_amount = request.POST.get('d_amount')
        maximum_usage = 0
        print(coupan_code,start_date_and_time,type(start_date_and_time),end_date_and_time,type(end_date_and_time),discount_amount,maximum_usage )
        a=Coupan.objects.create(coupan_code=coupan_code,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_amount=discount_amount,maximum_usage=maximum_usage)
        a.save()
        messages.info(request,'Created successfully')
    return render(request,'coupan_management.html')

def category_offer_management(request):
    if request.method=='POST':
        category_id = request.POST.get('c_code')
        category=add_category.objects.get(id=category_id)
        start_date_and_time = datetime.datetime.now()
        end_date_and_time = request.POST.get('e_date')
        discount_percentage = request.POST.get('d_percentage')
        a=Category_offer.objects.create(Category=category,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_percentage=discount_percentage)
        a.save()
        messages.info(request,'Created successfully')       
    category=add_category.objects.all()
    return render(request,'category_offer_management.html',{'category':category})

# # sales per day................
# def sales(request):
#     if request.method=='GET':
#         if 'date' in request.GET:
#             date = request.GET['date']
#             print("datesss",date)
#             Total = 0
#             if date:
#                 excel_products = sales_report.objects.all().delete()
#                 products =OrderProduct.objects.order_by('-created_at').filter(created_at__icontains=date)
                
#                 for product in products:
#                     excel_products = sales_report()
#                     excel_products.date = product.created_at
#                     excel_products.product_name = product.product.product_name
#                     excel_products.quantity = product.quantity
#                     excel_products.amount = product.order.order_total
#                     Total += product.order.order_total
#                     excel_products.save()
#                 context = {
#                 'products':products,
#                 }
#                 return render(request,'sales.html',context)
#             else:
#                 excel_products = sales_report.objects.all().delete()
#                 products =OrderProduct.objects.order_by('-created_at').all()
                
#                 for product in products:
#                     excel_products = sales_report()
#                     excel_products.date = product.created_at
#                     excel_products.product_name = product.product.product_name
#                     excel_products.quantity = product.quantity
#                     excel_products.amount = product.order.order_total
#                     Total += product.order.order_total
#                     excel_products.save()
#                 context = {
#                 'products':products,
#                 }
#                 return render(request,'sales.html',context)
#     return render(request,'sales.html')

# # sales per month.............................
# def monthly_sales(request):
#     if 'month_date' in request.GET:
#         month_date = request.GET['month_date']
#         Total = 0
#         if month_date:
#             excel_products = monthly_sales_report.objects.all().delete()
#             # months = OrderProduct.objects.annotate(month=ExtractMonth('created_at'))
#             months = OrderProduct.objects.filter(created_at__icontains = month_date)
#             print("months",months)
#             for month in months:
#                 excel_products = monthly_sales_report()
#                 excel_products.date = month.created_at
#                 excel_products.product_name = month.product.product_name
#                 excel_products.quantity = month.quantity
#                 excel_products.amount = month.order.order_total
#                 Total += month.order.order_total
#                 excel_products.save()
#             context = {
#                 'month_products': months,
#                 'Total':Total
#             }
#             return render(request, 'sales.html', context)
#     return redirect(sales)

# # sales per day excel download................
# def export_to_excel(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['content-Disposition'] = 'attachment; filename="sales.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     # this will generate a file named as sales Report
#     ws = wb.add_sheet('Sales Report')

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = ['Date','Product Name', 'Quantity', 'Amount', ]

#     for col_num in range(len(columns)):
#     # at 0 row 0 column
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()
#     total = 0
#     rows = sales_report.objects.all().values_list('date','product_name', 'quantity', 'amount')

#     print("row", rows)
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)
#     return response


# def export_to_pdf(request):
    
#     rows = sales_report.objects.all()
    
    
#     template_path = 'sales_pdf.html'
#     context = {
#         'report':rows
#     }
    
#     # csv file can also be generated using content_type='application/csv
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

#     template = get_template(template_path)
#     html = template.render(context)

#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')

#     return response

#     #########################################################################################

# def export_to_excel1(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['content-Disposition'] = 'attachment; filename="sales.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')
#     # this will generate a file named as sales Report
#     ws = wb.add_sheet('Sales Report')

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = ['Date','Product Name', 'Quantity', 'Amount', ]

#     for col_num in range(len(columns)):
#     # at 0 row 0 column
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     font_style = xlwt.XFStyle()
#     total = 0
#     rows = monthly_sales_report.objects.all().values_list('date','product_name', 'quantity', 'amount')

#     print("row", rows)
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)
#     return response


# def export_to_pdf1(request):
#     Date = []
#     product_name= []
#     quantity =[]
#     amount=[]
#     rows = monthly_sales_report.objects.all()
#     for i in rows:
#         Date.append(i.date)
#         product_name.append(i.product_name)
#         quantity.append(i.quantity)
#         amount.append(i.amount)
    
#     template_path = 'sales_pdf.html'
#     context = {
#         'brand_name':Date,
#         'order_count':product_name,
#         'total_amount':quantity,
#         'amount':amount,
#     }
    
    # # csv file can also be generated using content_type='application/csv
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    # template = get_template(template_path)
    # html = template.render(context)

    # # create a pdf
    # pisa_status = pisa.CreatePDF(
    #     html, dest=response)
    # # if error then show some funny view
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')

    # return response

def view_categories(request):
    categories = add_category.objects.all()
    return render(request,'view_categories.html',{'cat':categories})

def delete_category(request,id):
    print(id)
    add_category.objects.get(id=id).delete()
    return redirect(view_categories)

def product_offer_management(request):
    if request.method=='POST':
        product_id = request.POST.get('c_code')
        print('idhajkhbfkjd',product_id)
        product1=product.objects.get(id=product_id)
        start_date_and_time = datetime.datetime.now()
        end_date_and_time = request.POST.get('e_date')
        discount_percentage = request.POST.get('d_percentage')
        a=Product_offer.objects.create(product=product1,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_percentage=discount_percentage)
        a.save()
        messages.info(request,'Created successfully')
    category=product.objects.all()
    return render(request,'product_offer_management.html',{'category':category})

def view_offers(request):
    product_offer = Product_offer.objects.all()
    category_offer=Category_offer.objects.all()
    return render(request,'offers.html',{'product':product_offer,'category':category_offer})

def delete_category_offer(request,id):
    print(id)
    Category_offer.objects.get(id=id).delete()
    return redirect(view_offers)

def delete_product_offer(request,id):
    print(id)
    Product_offer.objects.get(id=id).delete()
    return redirect(view_offers)

def view_coupan(request):
    categories = Coupan.objects.all()
    return render(request,'view_coupan.html',{'coupan':categories})

def delete_coupan_offer(request,id):
    print(id)
    Coupan.objects.get(id=id).delete()
    return redirect(view_coupan)

####################################################################################################
def sales_report_date(request):
    data = OrderProduct.objects.all()
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProduct.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProduct.objects.filter(created_at__icontains=date)
            print(date_check)
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProduct.objects.filter(created_at__gte=date1,created_at__lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.cat_id.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.cat_id.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
    
    return render(request,'sales_report_.html')

def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response


def export_to_pdf(request):
    prod = product.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'sales_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

def sales(request):
    pass