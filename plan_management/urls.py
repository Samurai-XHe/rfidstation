from django.urls import path
from . import views

app_name = 'plan_management'
urlpatterns = [
    path('plan_applications/',views.plan_applications,name='plan_applications'),
    path('plan_review/',views.plan_review,name='plan_review'),
    path('plan_summary/',views.plan_summary,name='plan_summary'),
    path('add_plan/',views.add_plan,name='add_plan'),
    path('add_plan_interface/',views.add_plan_interface,name='add_plan_interface'),
    path('view_plan/<int:plan_pk>/',views.view_plan,name='view_plan'),
    path('plan_modify/<int:plan_pk>/',views.plan_modify,name='plan_modify'),
    path('plan_modify_interface/<int:plan_pk>/',views.plan_modify_interface,name='plan_modify_interface'),
    path('plan_delete/',views.plan_delete,name='plan_delete'),
]