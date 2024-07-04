from django.contrib import admin
from .models import Trader, Company, Stock, Buy, Sell


@admin.register(Trader)
class TraderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'balance', 'total_value')
    list_filter = ('status',)
    search_fields = ('user__username',)
    readonly_fields = ('total_value',)
    fieldsets = (
        (None, {
            'fields': ('user', 'status', 'balance', 'total_value')
        }),
    )
    ordering = ('user__username',)
    actions = ['make_pupil', 'make_student']

    def make_pupil(self, request, queryset):
        queryset.update(status='Pupil')

    make_pupil.short_description = "Mark selected traders as Pupils"

    def make_student(self, request, queryset):
        queryset.update(status='Student')

    make_student.short_description = "Mark selected traders as Students"


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'change', 'percentage', 'volume')
    search_fields = ('name', 'symbol')
    ordering = ('name',)
    actions = ['reset_values']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('trader', 'company', 'investment')
    search_fields = ('trader__user__username', 'company__name')
    ordering = ('trader__user__username', 'company__name')


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ('trader', 'company', 'amount')
    search_fields = ('trader__user__username', 'company__name')
    list_filter = ('trader__user__username', 'company__name')


@admin.register(Sell)
class SellAdmin(admin.ModelAdmin):
    list_display = ('trader', 'company', 'amount')
    search_fields = ('trader__user__username', 'company__name')
    list_filter = ('trader__user__username', 'company__name')


