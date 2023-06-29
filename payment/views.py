import paydunya
from paydunya import InvoiceItem, Store, Invoice
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings
from orders.models import Order
from send_mail.views import payment_successful_email
from django.http import HttpResponse

    
# Activer le mode 'test'. Le debug est à False par défaut
paydunya.debug = True

# Configurer les clés d'API
paydunya.api_keys = settings.PAYDUNYA_ACCESS_TOKENS

store = Store(name='Magasin Chez Xaralacommerce')

def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, pk=order_id)
    order_items = order.items.all()
    items = [InvoiceItem(
        name=item.product.name,
        quantity=item.quantity,
        unit_price=str(item.price),
        total_price=str(item.price * item.quantity),
        description=item.product.name
    ) for item in order_items]
    invoice = paydunya.Invoice(store)
    # host = request.get_host()
    # invoice.callback_url = f"http://{host}/payment-done/"
    # invoice.cancel_url = f"http://{host}/payment-canceled/"
    # invoice.return_url = f"http://{host}/payment-done/" 
    invoice.add_items(items)
    successful, response = invoice.create()        # création de commande
    if successful:
        return redirect(response.get("response_text"))  # pour rediriger sur la page de paiement de paydunya
        

def payment_done(request):
    token = request.GET.get("token")
    invoice = Invoice(Store)
    successful = invoice.confirm(token)       # on recupere invoice
    if successful:
    # envoi un mail, nous avons recu votre commande
        # payment_successful_email(order.email)
        return HttpResponse("<h2>Merci pour le paiement</h2>")
    

def payment_canceled(request):         # pour annuler un paiement
    return HttpResponse("<h2>Vous avez annulé le paiement</h2>")





