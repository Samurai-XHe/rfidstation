from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import PlanapplicationsForm
from .models import Department,Assets,Plan,ApplicationStatus

@login_required
def plan_applications(request):
    context = {}
    plan_list = Plan.objects.filter(application_status=1).order_by('-date_of_application')
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
    context = {}
    user = request.user
    depart = user.profile.department.department_name
    if request.method == 'POST':
        form = PlanapplicationsForm(request.POST,depart=depart)
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
            context['success_message'] = '添加成功'
            plan_list = Plan.objects.filter(application_status=1).order_by('-date_of_application')
            context['plan_list'] = plan_list
            return render(request, 'plan_management/plan_applications.html', context)
    else:
        form = PlanapplicationsForm(initial={'department':depart},depart=depart)
    context['form'] = form
    return render(request,'plan_management/add_plan.html',context)

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