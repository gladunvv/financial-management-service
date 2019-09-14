from django.contrib import admin
from wallet.models import Wallet, Transaction


@admin.register(Wallet)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class CourseAdmin(admin.ModelAdmin):
    pass
