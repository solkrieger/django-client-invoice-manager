from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client, Invoice, InvoiceItem
from .forms import ClientForm, InvoiceForm, InvoiceItemForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ClientSerializer, InvoiceSerializer

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "billing/register.html", {"form": form})


def home(request):
    return render(request, 'billing/home.html')


@login_required
def client_list(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, "billing/client_list.html", {"clients": clients})
    


@login_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            messages.success(request, "Client created successfully.")
            return redirect("client_list")
    else:
        form = ClientForm()
    return render(request, "billing/client_form.html", {"form": form})


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk, user = request.user)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully.")
            return redirect("client_list")
    else:
        form = ClientForm(instance=client)
    
    return render(request, "billing/client_form.html", {"form": form})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk= pk, user=request.user)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Client deleted successfully.")
        return redirect("client_list")
    
    return render(request, "billing/client_confirm_delete.html", {"client": client})



@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(user=request.user)
    return render(request, "billing/invoice_list.html", {"invoices": invoices})


@login_required
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST, user=request.user)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            messages.success(request, "Invoice created successfully.")
            return redirect("invoice_list")
    
    else:
        form = InvoiceForm(user=request.user)
    
    return render(request, "billing/invoice_form.html", {"form": form})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    items = invoice.items.all

    return render(request, "billing/invoice_detail.html", {
        "invoice": invoice,
        "items": items,
    })


@login_required
def item_create(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, user=request.user)

    if request.method == "POST":
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.invoice = invoice
            item.save()
            messages.success(request, "Item created successfully.")
            return redirect("invoice_detail", pk=invoice.id)
    
    else:
        form = InvoiceItemForm()

    return render(request, "billing/item_form.html", {"form": form})


@login_required
def dashboard(request):
    invoices = Invoice.objects.filter(user=request.user)
    
    unpaid_total = sum(i.total() for i in invoices if i.status == 'UNPAID')
    paid_total = sum(i.total() for i in invoices if i.status == 'PAID')

    recent_invoices= invoices.order_by("-created_at")[:5]
    
    return render(request, "billing/dashboard.html",{
        "unpaid_total": unpaid_total,
        "paid_total": paid_total,
        "recent_invoices": recent_invoices
    })


@login_required
def invoice_list(request):
    invoices = Invoice.objects.filter(user=request.user)

    status = request.GET.get("status")

    if status:
        invoices = invoices.filter(status=status)

    return render(request, "billing/invoice_list.html", {"invoices": invoices})


@login_required
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice,pk=pk, user = request.user)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice updated successfully.")
            return redirect("invoice_detail", pk=invoice.id)
    
    else:
        form = InvoiceForm(instance=invoice, user=request.user)
    
    return render(request, "billing/invoice_form.html", {"form": form})

    
@login_required
def invoice_delete(request, pk):
    invoice =get_object_or_404(Invoice, pk=pk, user=request.user)

    if request.method == "POST":
        invoice.delete()
        messages.success(request, "Invoice deleted successfully.")
        return redirect("invoice_list")
    
    return render(request, "billing/invoice_confirm_delete.html", {"invoice": invoice})


@login_required
def item_update(request, pk):
    item = get_object_or_404(InvoiceItem, pk=pk, invoice__user=request.user)

    if request.method == "POST":
        form = InvoiceItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect("invoice_detail", pk=item.invoice.id)
    else:
        form = InvoiceItemForm(instance=item)

    return render(request, "billing/item_form.html", {"form": form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(InvoiceItem, pk=pk, invoice__user=request.user)

    if request.method == "POST":
        invoice_id = item.invoice.id
        item.delete()
        messages.success(request, "Item deleted successfully.")
        return redirect("invoice_detail", pk=invoice_id)

    return render(request, "billing/item_confirm_delete.html", {"item": item})


@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    items = invoice.items.all()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{invoice.id}.pdf"'

    p = canvas.Canvas(response)
    
    y = 800
    p.drawString(100, y, f"Invoice #{invoice.id}")
    y -= 30

    p.drawString(100, y, f"Client: {invoice.client.name}")
    y -= 30

    p.drawString(100, y, f"Status: {invoice.status}")
    y -= 40

    for item in items:
        p.drawString(
            100,
            y,
            f"{item.description} - {item.quantity} x {item.price} = {item.total}"
        )
        y -= 20

    y -= 20
    p.drawString(100, y, f"Total: {invoice.total()}")

    p.showPage()
    p.save()

    return response



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_clients(request):
    clients = Client.objects.filter(user=request.user)
    serializer = ClientSerializer(clients, many= True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_invoices(request):
    invoices = Invoice.objects.filter(user=request.user)
    serializer = InvoiceSerializer(invoices, many= True)
    return Response(serializer.data)