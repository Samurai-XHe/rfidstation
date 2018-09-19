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
    path('plan_submit/',views.plan_submit,name='plan_submit'),
    path('review_page/<int:plan_pk>/',views.review_page,name='review_page'),
    path('view_review/<int:plan_pk>/',views.view_review,name='view_review'),
    path('department_not_pass/',views.department_not_pass,name='department_not_pass'),
    path('department_pass/',views.department_pass,name='department_pass'),
    path('add_plan_summary/',views.add_plan_summary,name='add_plan_summary'),
    path('add_plan_summary_interface/',views.add_plan_summary_interface,name='add_plan_summary_interface'),
    path('view_summary/<int:summary_pk>/',views.view_summary,name='view_summary'),
    path('summary_delete/',views.summary_delete,name='summary_delete'),
    path('summary_modify/<int:summary_pk>/',views.summary_modify,name='summary_modify'),
    path('summary_modify_interface/<int:summary_pk>/',views.summary_modify_interface,name='summary_modify_interface'),
    path('print_summary/',views.print_summary,name='print_summary'),
    path('summary_download/<int:summary_pk>/',views.summary_download,name='summary_download'),
]