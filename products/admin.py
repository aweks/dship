from django.contrib import admin
from dropship.products.models import Category, Product, Photo

class PhotoInline(admin.TabularInline):
    model = Photo

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
