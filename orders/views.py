from django.shortcuts import redirect, render
from .forms import OrderCreateForm
from cart.cart import Cart
from orders.models import OrderItem
from django.http import HttpResponse
from send_mail.views import send_new_order_email_with_template
from send_mail.views import send_new_order_email
from django.core.mail import send_mail
from django.template.loader import get_template



def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            email = form.cleaned_data.get("email")    # pour envoie de mail
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            cart.clear()    # pour vider le panier
            request.session["order_id"] = order.id 
            # on envoie un mail au client (faire de meme pour l'administrateur)
            send_new_order_email(email)
            # send_new_order_email_with_template(email)
            return redirect("payment_process")
            # return HttpResponse("<h2>Votre commande est receptionnée </h2>")
    else:
        form = OrderCreateForm()
    return render(request, "orders/create.html", {"order_cart": cart, "form": form})


def order_created(request):
    return render(request, "orders/created.html")





