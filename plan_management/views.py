import datetime
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PlanapplicationsForm
from .models import Department,Assets,Plan,ApplicationStatus

@login_required
def plan_applications(request):
    user = request.user
    department = user.profile.department.department_name
    context = {}
    plan_list = Plan.objects.filter(application_status=1,department__department_name=department).order_by('-date_of_application')
    context['plan_list'] = plan_list
    return render(request,'plan_management/plan_applications.html',context)

@login_required
def plan_review(request):
    return render(request,'plan_management/plan_review.html')

@login_required
def plan_summary(request):
    return render(request,'plan_management/plan_summary.html')

@login_required
def add_plan(request):
    user = request.user
    depart = user.profile.department.department_name
    form = PlanapplicationsForm(initial={'department':depart},depart=depart)
    context = {}
    context['form'] = form
    return render(request,'plan_management/add_plan.html',context)

@login_required
def add_plan_interface(request):
    user = request.user
    depart = user.profile.department.department_name
    form = PlanapplicationsForm(request.POST, depart=depart)
    data = {}
    if form.is_valid():
        department = form.cleaned_data['department']
        user = form.cleaned_data['user']
        year = form.cleaned_data['year']
        date_of_application = form.cleaned_data['date_of_application']
        assets = form.cleaned_data['assets']
        plan = Plan()
        plan.department = Department.objects.get(department_name=department)
        plan.user = User.objects.get(pk=user)
        plan.year = year
        plan.date_of_application = date_of_application
        plan.application_status = ApplicationStatus.objects.get(status='未提交')
        plan.save()
        asset = Assets.objects.get(pk=assets)
        plan.assets.add(asset)
        plan.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())
        return JsonResponse(data)

@login_required
def plan_modify_interface(request,plan_pk):
    user = request.user
    depart = user.profile.department.department_name
    form = PlanapplicationsForm(request.POST, depart=depart)
    data = {}
    if form.is_valid():
        department = form.cleaned_data['department']
        user = form.cleaned_data['user']
        year = form.cleaned_data['year']
        date_of_application = form.cleaned_data['date_of_application']
        assets = form.cleaned_data['assets']
        plan = Plan.objects.get(pk=plan_pk)
        plan.department = Department.objects.get(department_name=department)
        plan.user = User.objects.get(pk=user)
        plan.year = year
        plan.date_of_application = date_of_application
        plan.application_status = ApplicationStatus.objects.get(status='未提交')
        plan.save()
        asset = Assets.objects.get(pk=assets)
        plan.assets.add(asset)
        plan.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())
        return JsonResponse(data)

@login_required
def view_plan(request,plan_pk):
    try:
        plan_pk = int(plan_pk)
        plan = Plan.objects.get(pk=plan_pk)
    except Plan.DoesNotExist as e:
        return redirect(reverse('index'))
    context = {}
    context['plan'] = plan
    return render(request,'plan_management/view_plan.html',context)

@login_required
def plan_modify(request,plan_pk):
    try:
        plan_pk = int(plan_pk)
        plan = Plan.objects.get(pk=plan_pk)
    except Plan.DoesNotExist as e:
        return redirect(reverse('index'))
    user = request.user
    depart = user.profile.department.department_name
    form = PlanapplicationsForm(
        initial={
            'department': depart,
            'user':plan.user.pk,
            'year':plan.year,
            'date_of_application':plan.date_of_application.strftime('%Y-%m-%d'),
            'assets':plan.assets.first().pk #因为是一个select字段，多对多选第一个物资的pk
        }, depart=depart
    )
    context = {}
    context['plan'] = plan
    context['form'] = form
    return render(request,'plan_management/plan_modify.html',context)

@login_required
def plan_delete(request):
    user = request.user
    try:
        plan_pk = int(request.GET.get('plan_pk'))
    except Exception as e:
        return JsonResponse({'status':'error','message':'该计划不存在'})
    data = {}
    if user.has_perm('plan_management.delete_plan') and Plan.objects.filter(pk=plan_pk).exists():
        plan = Plan.objects.get(pk=plan_pk)
        plan.delete()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        return JsonResponse(data)