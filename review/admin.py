from django.contrib import admin
from .models import DepartmentReview,LogisticsReview
@admin.register(DepartmentReview)
class DepartmentReviewAdmin(admin.ModelAdmin):
    list_display = ('review_content','review_time','reviewer','content_type','object_id')

@admin.register(LogisticsReview)
class LogisticsReviewAdmin(admin.ModelAdmin):
    list_display = ('review_content', 'review_time', 'reviewer', 'content_type', 'object_id')