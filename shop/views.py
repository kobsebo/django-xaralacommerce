from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.db.models import Q
from .models import Product, Category
from cart.forms import CartAddProductForm




def index(request):
    products = Product.objects.all()
    context = {"title": "Bienvenue chez vous", "products": products}
    return render(request, "index.html", context)


class ProductList(View):
    # model = Product
    # context_object_name = 'products'
    template_name = 'shop/product_list.html'

    def get(self, request):
        products = Product.objects.all()    # recherche de filtre
        categories = Category.objects.all()    # pour rendre dynamique la liste des categories
        q = request.GET.get("q")     # recherche de filtre
        # print("Query", q)
        if q:    # pour vérifier si q existe
            products = Product.objects.filter(
                Q(name__icontains=q) |        # ici c'est pour recherche par nom description et categorie # | veut dire or
                Q(description__icontains=q) |
                Q(category__name__icontains=q)
                )   # pour le nom exact du produit
        return render(request, self.template_name, {"products": products, "categories": categories})   # recherche de filtre


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_details.html'
    # def get(self, request):
        # return render(request, self.template_name, {"product": product})
    
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context["cart_product_form"] = CartAddProductForm()
        return context
    
