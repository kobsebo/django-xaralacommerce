from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from cart.forms import CartAddProductForm
from shop.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)   # le produit que l'utilisateur va ajouter
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():    # verifier si le formulaire est valide
        cleaned_data = form.cleaned_data 
        cart.add(product=product, quantity=cleaned_data["quantity"], override_quantity=cleaned_data["override"])
        return redirect("cart_detail")
    

@require_POST
def cart_remove(request, product_id):       # pour retirer un produit du panier
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")
    

def cart_detail(request):
    cart = Cart(request)   # recuperation de la cart sur le panier
    for item in cart:   # pour mettre à jour les qtés
        item['update_quantity_form'] = CartAddProductForm(initial={"quantity": item["quantity"], "override": True})

    return render(request, "cart/cart_detail.html", {"cart": cart})   # {"cart": cart} qui permet d'afficher l'image dans le panier

