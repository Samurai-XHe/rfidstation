from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname','user','department')
    search_fields = ('nickname','user__username')
