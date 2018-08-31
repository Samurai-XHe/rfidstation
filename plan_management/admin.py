from django.contrib import admin

from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('department','user','year','date_of_application','application_status')
