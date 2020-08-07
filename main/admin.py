from django.contrib import admin
from django.utils.html import format_html

from .models import ProductTag, ProductImage, Product

admin.AdminSite.site_title = 'BookTime'
admin.AdminSite.site_header = 'BookTime administration'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_stock', 'price', )
    list_filter = ('active', 'in_stock', 'date_updated', )
    list_editable = ('in_stock', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}
    autocomplete_fields = ('tags', )


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    list_filter = ('active', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'product_name', )
    readonly_fields = ('thumbnail', )
    search_fields = ('product__name', )
    autocomplete_fields = ('product', )

    def thumbnail_tag(self, obj):
        return format_html(
            '<img src="%s"/>' % obj.thumbnail.url) if obj.thumbnail else '-'

    thumbnail_tag.short_description = 'Thumbnail'

    def product_name(self, obj):
        return obj.product.name
