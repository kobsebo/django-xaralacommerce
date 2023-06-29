from django.urls import path
from .views import cart_add, cart_detail, cart_remove

urlpatterns = [
    path("", cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", cart_add, name="cart_add"),     # add/<int:product_id>/ (pour préciser le chemin de produit avec son argument)
    path("remove/<int:product_id>/", cart_remove, name="cart_remove"),
]