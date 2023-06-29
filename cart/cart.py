from django.db import models
from django.conf import settings
from shop.models import Product
from decimal import Decimal 
# from django.http import HttpResponse




class Cart(object):
    def __init__(self, request):

        # Initialiser le panier
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)   # on recupere le panier depuis la session CART_SESSION_ID (l'ajouter dans settings en bas)
        if not cart:     # pour sauvegarder les données de l'utilisateur
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    # ajouter au panier
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity   # si le produit a été initialisé cad la qté, on recupere la qté par defaut
        else:
            self.cart[product_id]["quantity"] += quantity    # on ajoute les qtés de l'utilisateur
        self.save()

    # supprimer du panier

    def remove(self, product):
        product_id = str(product.id)   # on recupere le produit_id dans dans le panier
        if product_id in self.cart:    # ici c'est pour savoir le produit choisi dans le panier
            del self.cart[product_id]
            self.save()

    # recuperer tous les éléments  (ici c'est une itération)

    def __iter__(self):
        product_ids = self.cart.keys()    # on recupere toutes les valeurs dans le cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()    # on va copier le panier

        for product in products:
            cart[str(product.id)]["product"] = product    # ajout de produit dans notre panier

        for item in cart.values():    # on va recuperer les valeurs de notre dictionnaire
            item["price"] = Decimal(item['price'])
            item["total_price"] = item['price'] * item["quantity"]
            yield item    # pour avoir plus de performance

    # compter les éléments sur le panier
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())  # on retourne la somme des items et on recupere la partie item quantité
    
    # calculer la valeur totale du panier
    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())
    
    # vider le panier
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
