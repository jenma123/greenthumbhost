from django.contrib import admin
from .models import Payment, Order, OrderedPlant


class OrderedPlantInline(admin.TabularInline):
    model = OrderedPlant
    readonly_fields = ('order', 'payment', 'user', 'plantitem', 'quantity', 'price', 'amount')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status']
    inlines = [OrderedPlantInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedPlant)