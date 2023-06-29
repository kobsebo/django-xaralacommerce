from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "categories"    # pour regler le probleme d'ortographe

    def __str__(self):
        return self.name    # pour permettre a ce que le nom du produit s'affiche dans l'administration


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to="products/%Y/%m%d")       # %Y/%m%d  permet de formater la date
    description = models.TextField(blank=True)    # blank=True veut dire qu'on n'est pas obliger d'ecrire 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)   # ici la dae s'actualise

    def __str__(self):
        return self.name      # pour permettre a ce que le nom du produit s'affiche dans l'administration

    def get_absolute_url(self):     # pour les details d'un produit
        return reverse("product-details", kwargs={'slug': self.slug})
