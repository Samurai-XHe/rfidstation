from django.contrib import admin

from .models import Plan,ApplicationStatus,Plan_Summary,SummaryStatus

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('department','user','year','date_of_application','application_status')

@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ('id','status')

@admin.register(Plan_Summary)
class Plan_SummaryAdmin(admin.ModelAdmin):
    list_display = ('id','project_name','year','summary_status')

@admin.register(SummaryStatus)
class SummaryStatusAdmin(admin.ModelAdmin):
    list_display = ('id','status')