from django.contrib import admin
from .models import Product, InventoryProduct, Inventory, Driver, OrderProduct, Order, Payment, ConstructionSite, ConstructionSiteImage, ResponsiblePerson, Store, PaymentRequest

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'case', 'count')
    search_fields = ('name',)

class InventoryProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'count', 'inventory')
    search_fields = ('product__name',)
    list_filter = ('inventory',)

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('created_date',)
    date_hierarchy = 'created_date'

class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'auto')
    search_fields = ('name', 'phone')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'count', 'order')
    search_fields = ('product__name',)
    list_filter = ('order',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'driver', 'cash')
    date_hierarchy = 'created_date'
    search_fields = ('driver__name',)



# Регистрация моделей
admin.site.register(Product, ProductAdmin)
admin.site.register(InventoryProduct, InventoryProductAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('driver', 'cash', 'created_date')
    list_filter = ('created_date',)

admin.site.register(Payment, PaymentAdmin)

#2 block
class ConstructionSiteImageInline(admin.TabularInline):
    model = ConstructionSiteImage
    extra = 1

class ConstructionSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'responsible_person')
    search_fields = ('name', 'location')
    inlines = [ConstructionSiteImageInline]

class ResponsiblePersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'phone_number')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name', 'address', 'phone_number')

class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = ('construction_site', 'responsible_person', 'store', 'amount', 'status', 'created_at', 'reviewed_by')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('construction_site__name', 'responsible_person__user__username', 'store__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('construction_site', 'responsible_person', 'store', 'amount', 'description', 'status')
        }),
        ('Review Info', {
            'fields': ('reviewed_by',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

admin.site.register(ConstructionSite, ConstructionSiteAdmin)
admin.site.register(ResponsiblePerson, ResponsiblePersonAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(PaymentRequest, PaymentRequestAdmin)
#2 block