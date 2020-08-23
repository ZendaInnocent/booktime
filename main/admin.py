from django.contrib import admin
from django.utils.html import format_html

from .models import (ProductTag, ProductImage, Product,
                     Basket, BasketLine, Order, OrderLine)

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


class BasketLineInline(admin.TabularInline):
    model = BasketLine
    raw_id_fields = ('product', )


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'count', )
    list_editable = ('status', )
    list_filter = ('status', )
    inlines = (BasketLineInline, )


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    raw_id_fields = ('product', )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', )
    list_editable = ('status', )
    list_filter = ('status', 'shipping_country', 'date_added', )
    list_display_links = ('user', )
    inlines = (OrderLineInline, )
    fieldsets = (
        (None, {'fields': ('user', 'status', )}),
        ('Billing Info', {
            'fields': (
                'billing_name',
                'billing_address1',
                'billing_address2',
                'billing_zip_code',
                'billing_city',
                'billing_country',
            )
        }),
        ('Shipping Info', {
            'fields': (
                'shipping_name',
                'shipping_address1',
                'shipping_address2',
                'shipping_zip_code',
                'shipping_city',
                'shipping_country',
            )
        }),
    )
