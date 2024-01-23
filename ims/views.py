from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, date
from .models import Category, Product, Sale, SalesItem, Inventory, ErrorTicket
from account.models import CustomUser, LoggedIn, Pos
from django.contrib.auth.decorators import login_required
from . forms import *
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
import csv
import json
# import datetime
from account.decorators import for_admin, for_staff, for_sub_admin, is_unsubscribed
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.shortcuts import get_object_or_404
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
# from weasyprint import HTML
# import tempfile



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Create your views here
@login_required(login_url=('login'))
@is_unsubscribed
def dashboard(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    products = Product.objects.all()
    category = Category.objects.all()
    
    total_product = products.count()
    total_category = category.count()
    transaction = len(Sale.objects.filter( completed=True,
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ))
    today_sales = Sale.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    total_sales = sum(today_sales.values_list('final_total_price',flat=True))
    # make graph for highest paid products per day
    today_profit = Sale.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    total_profits = sum(today_profit.values_list('total_profit', flat=True))
    pending = ErrorTicket.objects.filter(status='Pending')
    inventory = Inventory.objects.all()

    sale = Sale.objects.order_by('-total_profit')[:7]
    item = SalesItem.objects.order_by('-quantity')[:7]


    context = {
        'pending':pending,
        'products':products,
        'category':category,
        'total_product':total_product,
        'total_category':total_category,
        'transaction':transaction,
        'total_sales':total_sales,
        'total_profits':total_profits,
        'sale':sale,
        'item':item,
        'inventory':inventory
    }
    return render(request, 'ims/index.html', context)

@login_required
@is_unsubscribed
@for_admin
def report(request):
    now = datetime.now()
    start_date_contains = request.GET.get('start_date')
    end_date_contains = request.GET.get('end_date')
    sale = Sale.objects.all()

    if start_date_contains != '' and start_date_contains is not None:
        sale = sale.filter(date_updated__gte=start_date_contains)

    if end_date_contains != '' and end_date_contains is not None:
        sale = sale.filter(date_updated__lt=end_date_contains)
    
    
    total_profits = sum(sale.values_list('total_profit', flat=True))
    

    context = {
        'sale':sale,
        'total_profits':total_profits,
    }
    return render(request, 'ims/reports.html', context)

@login_required
@is_unsubscribed
@for_staff
def store(request):
    inventory = Inventory.objects.all()
    category = Category.objects.all()
    products = Product.objects.all()
    paginator = Paginator(Inventory.objects.all(), 15)
    page = request.GET.get('page')
    inventory_page = paginator.get_page(page)
    nums = "a" *inventory_page.paginator.num_pages
    product_contains_query = request.GET.get('product')

    category = request.GET.get('category')

    if products is None:
        inventory = Inventory.objects.all()
    # else:
    #     inventory = Inventory.objects.filter(product__category=category)

    if product_contains_query != '' and product_contains_query is not None:
        inventory_page = inventory.filter(product__product_name__icontains=product_contains_query)


    context = {
        'inventory':inventory,
        'inventory_page':inventory_page,
        'nums':nums
    }
    return render(request, 'ims/store.html', context)


@for_staff
@login_required
@is_unsubscribed
def cart(request):
    inventory = Inventory.objects.all()
    pos = Pos.objects.all()
    
    if request.user.is_authenticated:
        staff = request.user
        sale , created = Sale.objects.get_or_create(staff=staff, completed=False)
        items = sale.salesitem_set.all()
        
    context = {
        'items':items,
        'sale':sale,
        'pos':pos,
        'inventory':inventory
    }
    return render(request, 'ims/cart.html', context)


@for_staff
@login_required
@is_unsubscribed
def checkout(request):
    inventory = Inventory.objects.all()
    
    if request.user.is_authenticated:
        staff = request.user
        sale , created = Sale.objects.get_or_create(staff=staff, completed=False)
        items = sale.salesitem_set.all()
        form = PaymentForm()
        if request.method == 'POST':
            form = PaymentForm(request.POST or None, instance=sale)
            if form.is_valid():
                sale = form.save(commit=False)
                sale.save()
                messages.success(request, 'Payment Method Updated')
        
    context = {
        'items':items,
        'sale':sale,
        'inventory':inventory,
    }
    return render(request, 'ims/checkout.html', context)



def updateCart(request):
    data = json.loads(request.body)
    inventoryId = data['inventoryId']
    action = data['action']
    print('inventory:', inventoryId)
    print('Action:', action)

    staff = request.user
    inventory = Inventory.objects.get(id=inventoryId)
    sale, created = Sale.objects.get_or_create(staff=staff, completed=False)
    saleItem, created = SalesItem.objects.get_or_create(sale=sale, inventory=inventory)

    if action == 'add':
        saleItem.quantity = (saleItem.quantity + 1)
    saleItem.save()

    if saleItem.quantity <= 0:
        saleItem.delete()

    context = {
        'qty': sale.get_cart_items,
    }

    return JsonResponse(context, safe=False)


def scanCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('inventory:', productId)
    print('Action:', action)

    staff = request.user
    inventory = Inventory.objects.get(product=productId)
    sale, created = Sale.objects.get_or_create(staff=staff, completed=False)
    saleItem, created = SalesItem.objects.get_or_create(sale=sale, inventory=inventory)

    if action == 'add':
        saleItem.quantity = (saleItem.quantity + 1)
    saleItem.save()

    if saleItem.quantity <= 0:
        saleItem.delete()

    context = {
        'qty': sale.get_cart_items,
    }

    return JsonResponse(context, safe=False)


def updateQuantity(request):
    data = json.loads(request.body)
    input_value = int(data['val'])
    inventory_Id = data['invent_id']
    
    staff = request.user
    inventory = Inventory.objects.get(id=inventory_Id)
    sale, created = Sale.objects.get_or_create(staff=staff, completed=False)
    saleItem, created = SalesItem.objects.get_or_create(sale=sale, inventory=inventory)
    saleItem.quantity = input_value
    saleItem.save()

    if saleItem.quantity <= 0:
        saleItem.delete()

    context = {
        'sub_total':saleItem.get_total,
        'final_total':sale.get_cart_total,
        'total_quantity':sale.get_cart_items,
    }

    return JsonResponse(context, safe=False)


def sale_complete(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    staff = request.user
    sale, created = Sale.objects.get_or_create(staff=staff, completed=False)
    sale.transaction_id = transaction_id
    total = float(data['payment']['total_cart'])
    sale.final_total_price = sale.get_cart_total
    sale.total_profit = sale.get_total_profit
    sale.shop = staff.pos


    if total == sale.get_cart_total:
        sale.completed = True
    sale.save()


    messages.success(request, 'sale completed')

    return JsonResponse('Payment completed', safe=False)

@login_required
@is_unsubscribed
@for_admin    
def sales(request):
    sale = Sale.objects.filter(completed = True).all().order_by('-date_updated')
    paginator = Paginator(Sale.objects.all().order_by('-date_updated'), 10)
    page = request.GET.get('page')
    sale_page = paginator.get_page(page)
    nums = "a" *sale_page.paginator.num_pages
    start_date_contains = request.GET.get('start_date')
    end_date_contains = request.GET.get('end_date')
    shop_contains_query = request.GET.get('shop')


    if start_date_contains != '' and start_date_contains is not None:
        sale_page = sale.filter(date_updated__gte=start_date_contains)

    if end_date_contains != '' and end_date_contains is not None:
        sale_page = sale.filter(date_updated__lt=end_date_contains)

    if shop_contains_query != '' and shop_contains_query is not None:
        sale_page = sale.filter(shop__pos_name__icontains=shop_contains_query)

    context = {
        'sale':sale,
        'sale_page':sale_page,
        'nums':nums
    }
    return render(request, 'ims/sales.html', context)

@for_admin
def sale(request, pk):
    sale = Sale.objects.get(id=pk)

    context = {
        'sale':sale
    }
    return render(request, 'ims/sales_delete.html', context)

@for_admin
def sale_delete(request):
    if request.method == 'POST':
        sale = Sale.objects.get(id = request.POST.get('id'))
        if sale != None:
            sale.delete()
            messages.success(request, "Succesfully deleted")
            return redirect('sales')

@for_admin
def export_sales_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']='attachment; filename = Sales History'+str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Sales Rep', 'Trans Id', 'Date', 'Quantity', 'Total'])
    
    sale = Sale.objects.all()
    
    
    for sale in sale:
       
        writer.writerow([sale.staff, sale.transaction_id, sale.date_updated, sale.get_cart_items, sale.final_total_price])
    
    return response
    


@for_staff
@login_required
@is_unsubscribed
def reciept(request, pk):
    sale = Sale.objects.get(id = pk)
    salesitem = SalesItem.objects.filter(sale_id=sale).all()
    
    context = {
        'salesitem':salesitem,
        'sale':sale
    }
    return render(request, 'ims/reciept.html', context)


def profitData(request, pk):
    profits = []

    sale = Sale.objects.get(id = pk)
    items = sale.salesitem_set.all()

    for i in items:
        profits.append({i.get_profit:i.inventory.product.product_name})

    return JsonResponse(profits, safe=False)



@for_sub_admin
@login_required
@is_unsubscribed
def product_category(request):
    products = Product.objects.all().order_by('-date_created')
    category = Category.objects.filter().all()
    paginator = Paginator(Product.objects.all(), 15)
    page = request.GET.get('page')
    products_page = paginator.get_page(page)
    nums = "a" *products_page.paginator.num_pages
    product_contains = request.GET.get('product_name')
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully created')
            return redirect('products')

    if product_contains != '' and product_contains is not None:
        products_page = products.filter(product_name__icontains=product_contains)
        
    context = {
        'category':category,
        'form':form,
        'products':products,
        'products_page':products_page,
        'nums':nums
    }
    return render(request, 'ims/products.html', context)


@for_sub_admin
def product(request, pk):
    products = Product.objects.get(id=pk)

    context = {
        'products':products
    } 
    return render(request, 'ims/modal_edit_product.html', context)


@for_sub_admin
def edit_product(request):
    if request.method == 'POST':
        product = Product.objects.get(id = request.POST.get('id'))
        if product != None:
            form = EditProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'successfully updated')
                return redirect('products')


@for_admin
def delete_product(request):
    if request.method == 'POST':
        product = Product.objects.get(id = request.POST.get('id'))
        if product != None:
            product.delete()
            messages.success(request, "Succesfully deleted")
            return redirect('products')


@login_required
@is_unsubscribed
@for_sub_admin
def category_list(request):
    category = Category.objects.all()
    paginator = Paginator(Category.objects.all(), 15)
    page = request.GET.get('page')
    category_page = paginator.get_page(page)
    nums = "a" *category_page.paginator.num_pages
    category_contains = request.GET.get('category_name')
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully created')
            return redirect('category_list')
            
    if category_contains != '' and category_contains is not None:
        category_page = category.filter(category_name__icontains=category_contains)

    context = {
        'category':category,
        'form':form,
        'category_page':category_page,
        'nums':nums
    }
    return render(request, 'ims/category.html', context)


@for_sub_admin
@login_required
@is_unsubscribed
def category(request, pk):
    category = Category.objects.get(id=pk)

    context = {
        'category':category
    }
    return render(request, 'ims/edit_category', context)


@for_sub_admin
def edit_category(request):
    if request.method == 'POST':
        category = Category.objects.get(id = request.POST.get('id'))
        if category != None:
            form = EditCategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, 'successfully updated')
                return redirect('category_list')


@for_admin
def delete_category(request):
    if request.method == 'POST':
        category = Category.objects.get(id = request.POST.get('id'))
        if category != None:
            category.delete()
            messages.success(request, "Succesfully deleted")
            return redirect('category_list')


@for_sub_admin
@login_required
@is_unsubscribed
def inventory_list(request):
    inventory = Inventory.objects.all()
    product = Product.objects.filter().all()
    paginator = Paginator(Inventory.objects.all(), 15)
    page = request.GET.get('page')
    inventory_page = paginator.get_page(page)
    nums = "a" *inventory_page.paginator.num_pages
    product_contains_query = request.GET.get('product')
    form = CreateInventoryForm
    if request.method == "POST":
        form = CreateInventoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully created')
            return redirect('inventorys')
    
    if product_contains_query != '' and product_contains_query is not None:
        inventory_page = inventory.filter(product__product_name__icontains=product_contains_query)

    context = {
        'inventory':inventory,
        'product':product,
        'form':form,
        'inventory_page':inventory_page,
        'nums':nums,
    }
    return render(request, 'ims/inventory.html', context)


@login_required
@is_unsubscribed
def inventory(request, pk):
    inventory = Inventory.objects.get(id=pk)

    context = {
        'inventory':inventory
    }
    return render(request, 'ims/edit_inventory.html', context)


@for_admin
def edit_inventory(request):
    if request.method == 'POST':
        inventory = Inventory.objects.get(id = request.POST.get('id'))
        if inventory != None:
            form = ReorderForm(request.POST, instance=inventory)
            if form.is_valid():
                form.save()
                messages.success(request, 'successfully updated')
                return redirect('inventorys')


@for_sub_admin
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            source_product_id = form.cleaned_data['transfer_from']
            destination_product_id = form.cleaned_data['transfer_to']
            quantity_transfered = form.cleaned_data['quantity_transfered']

            # Get the source and destination Inventory objects
            source_inventory = get_object_or_404(Inventory, product_id=source_product_id)
            destination_inventory = get_object_or_404(Inventory, product_id=destination_product_id)

            if quantity_transfered > 0:
                # Perform the transfer logic
                source_inventory.quantity -= quantity_transfered
                destination_inventory.quantity += quantity_transfered

                # Save the changes
                source_inventory.save()
                destination_inventory.save()

                return redirect('inventorys')
    else:
        form = TransferForm()

    inventory = Inventory.objects.all()
    return render(request, 'transfer.html', {'form': form, 'inventory': inventory})


@for_sub_admin
def restock(request):
    if request.method == 'POST':
        inventory = Inventory.objects.get(id = request.POST.get('id'))
        if inventory != None:
            form = RestockForm(request.POST, instance=inventory)
            if form.is_valid():
                form.save(commit=False)
                inventory.quantity += inventory.quantity_restocked
                inventory.save()
                messages.success(request, 'successfully updated')
                return redirect('inventorys')
        else:
            form = RestockForm()
        

@for_sub_admin
@login_required
@is_unsubscribed
def inventoryView(request):
    inventory = Inventory.objects.all()
    product = Product.objects.filter().all()
    paginator = Paginator(Inventory.objects.all(), 15)
    page = request.GET.get('page')
    inventory_page = paginator.get_page(page)
    nums = "a" *inventory_page.paginator.num_pages
    product_contains_query = request.GET.get('product')

    if product_contains_query != '' and product_contains_query is not None:
        inventory_page = inventory.filter(product__product_name__icontains=product_contains_query)

    context = {
        'inventory':inventory,
        'product':product,
        'inventory_page':inventory_page,
        'nums':nums,
    }
    return render(request, 'ims/product_list.html', context)

@for_sub_admin
@login_required
@is_unsubscribed
def countView(request):
    inventory = Inventory.objects.all()
    audit = Inventory.history.all()

    context = {
        'inventory':inventory,
        'audit':audit
    }
    return render(request, 'ims/count.html', context)


@for_sub_admin
def addCount(request):
    if request.method == 'POST':
        inventory = Inventory.objects.get(id = request.POST.get('id'))
        if request.method != None:
            form = AddCountForm(request.POST, instance=inventory)
            if form.is_valid():
                form.save(commit=False)
                inventory.variance = inventory.count - inventory.store_quantity
                inventory.save()
                messages.success(request, 'Count Added Successfully')
                return redirect('count')

@for_admin
def delete_inventory(request):
    if request.method == 'POST':
        inventory = Inventory.objects.get(id = request.POST.get('id'))
        if inventory != None:
            inventory.delete()
            messages.success(request, "Succesfully deleted")
            return redirect('inventorys')

@for_admin
@login_required
@is_unsubscribed
def inventoryAudit(request):
    inventory = Inventory.objects.all()
    audit = Inventory.history.all()

    context = {
        'inventory':inventory,
        'audit':audit
    }
    return render(request, 'ims/price_audit.html', context)


@for_admin
def export_audit_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']='attachment; filename = Audit History'+str(datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Staff', 'Product', 'Date Restocked', 'Quantity Restocked', 'New Cost Price', 'New Sale Price'])
    
    audit = Inventory.history.all()
    
    for audit in audit:
        if audit.quantity_restocked > 0:
            writer.writerow([audit.history_user, audit.product.product_name, audit.history_date, audit.quantity_restocked, audit.cost_price, audit.sale_price])
    
    return response


@login_required
@is_unsubscribed
@for_admin
def staffs(request): 
    staff = CustomUser.objects.filter(is_active = True).all()
    staff_contains = request.GET.get('username')
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account successfully created for ' + username)

    if staff_contains != '' and staff_contains is not None:
        staff = staff.filter(username__icontains=staff_contains)
   
    context = {
        'staff':staff,
        'form':form
    }
    return render(request, 'ims/staff.html', context)


@login_required
@is_unsubscribed
@for_admin
def staff(request, pk):
    staff = CustomUser.objects.get(id=pk)

    context = {
        'staff':staff,
    }
    return render(request, 'ims/staff.html', context)


@login_required
@is_unsubscribed
@for_admin
def edit_staff(request):
    if request.method == 'POST':
        staff = get_object_or_404(CustomUser, id=request.POST.get('id'))
        form = UserForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated')
            return redirect('staff')
        else:
            messages.error(request, 'Form is not valid. Please check the entered data.')
  



@for_admin
def delete_staff(request):
    if request.method == 'POST':
        staff = CustomUser.objects.get(id = request.POST.get('id')) 
        if staff != None and staff.is_active == True:
            staff.is_active = False
            staff.save()
            messages.success(request, "Succesfully deleted")
            return redirect('staff')


@for_admin
@login_required
@is_unsubscribed
def record(request):
    login_trail = LoggedIn.objects.all().order_by('-timestamp')
    staff_contains = request.GET.get('username')

    if staff_contains != '' and staff_contains is not None:
        login_trail = login_trail.filter(staff__username__icontains=staff_contains)

    context = {
        'login_trail':login_trail,
    }
    return render(request, 'ims/records.html', context)

@login_required
@is_unsubscribed
def errorTicket(request):
    ticket = ErrorTicket.objects.all()
    pending = ErrorTicket.objects.filter(status='Pending')

    context = {
        'ticket':ticket,
        'pending':pending
    }

    return render(request, 'ims/ticket.html', context)

@login_required
@is_unsubscribed
def Ticket(request, pk):
    ticket = ErrorTicket.objects.get(id=pk)
    form = UpdateTicketForm(instance=ticket)
    if request.method == 'POST':
        form = UpdateTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ticket viewed')
            return redirect('ticket')

    context = {
        'ticket':ticket
    }
    return render(request, 'ims/view_ticket.html', context)

@login_required
@is_unsubscribed
def createTicket(request):
    staff = CustomUser.objects.all()
    form = CreateTicketForm()
    if request.method == 'POST':
        form = CreateTicketForm(request.POST or None)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.staff = request.user
            ticket.pos_area = ticket.staff.pos
            ticket.save()
            messages.success(request, 'Ticket Created Successfully')
            return redirect('index')

    context = {
        'staff':staff
    }
    
    return render(request, 'ims/create_ticket.html', context)


def export_profit(request):
    
    # create buffer
    buf = io.BytesIO()
    #  create canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #  create a text object
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 10)
    # Add lines of text
    

    sale = Sale.objects.all()
    total_profits = sum(sale.values_list('total_profit', flat=True))
    lines = []

    for sale in sale:
        lines.append(str(sale.staff))
        lines.append(sale.transaction_id)
        lines.append(sale.method)
        lines.append(str(sale.date_updated))
        lines.append(str(sale.get_cart_items))
        lines.append(str(sale.final_total_price))
        lines.append(" ")

    lines.append(str(total_profits))


    for line in lines:
        textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    #  return
    return FileResponse(buf, as_attachment=True, filename='profits.pdf')


# def inventoryReport(request):
#     report = Inventory.objects.all()

#     context = {
#         'report': report
#     }
#     return render(request, 'ims/inv_report.html', context)

def downloadProductDetails(request):
    report = Inventory.objects.all()

    data = {
        'report': report
    }

    pdf = render_to_pdf('ims/inv_report.html', data)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"Product_{timestamp}.pdf"
        content = f"attachment; filename={filename}"
        response["Content-Disposition"] = content

        return response
    return HttpResponse("No pdf file found")




    
