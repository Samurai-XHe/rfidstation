from django.urls import path
from . import views

app_name = 'plan_management'
urlpatterns = [
    path('plan_applications/',views.plan_applications,name='plan_applications'),
    path('plan_review/',views.plan_review,name='plan_review'),
    path('plan_summary/',views.plan_summary,name='plan_summary'),
]