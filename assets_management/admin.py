from django.contrib import admin
from .models import Assets

@admin.register(Assets)
class AssetsAdmin(admin.ModelAdmin):
    list_display = ('assets_name','price','order')
