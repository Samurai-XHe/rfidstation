import datetime
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,FileResponse
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import escape_uri_path
from .forms import PlanapplicationsForm,PlanSummaryForm
from .models import Department,Assets,Plan,ApplicationStatus,SummaryStatus,Plan_Summary
from review.forms import DepartmentForm
from review.models import DepartmentReview
from openpyxl import Workbook

@login_required
def plan_applications(request):
    user = request.user
    department = user.profile.department.department_name
    plan_list = Plan.objects.filter(
        Q(application_status=1)|Q(application_status=3)|Q(application_status=4),
        department__department_name=department).order_by('-date_of_application')
    leader = User.objects.get(profile__department__department_name=department,groups__name='部门领导')
    context = {}
    context['plan_list'] = plan_list
    context['department_leader'] = leader.profile.nickname
    return render(request,'plan_management/plan_applications.html',context)

@login_required
def plan_summary(request):
    summarys = Plan_Summary.objects.all()
    context = {}
    context['summarys'] = summarys
    return render(request,'plan_management/plan_summary.html',context)

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
    if DepartmentReview.objects.filter(plan=plan).exists():
        review = DepartmentReview.objects.filter(plan=plan).order_by('-review_time').first()
        review_content = review.review_content
    else:
        review_content = ''
    context = {}
    context['plan'] = plan
    context['review_content'] = review_content
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
    if DepartmentReview.objects.filter(plan=plan).exists():
        review = DepartmentReview.objects.filter(plan=plan).order_by('-review_time').first()
        review_content = review.review_content
    else:
        review_content = ''
    context = {}
    context['plan'] = plan
    context['form'] = form
    context['review_content'] = review_content
    return render(request,'plan_management/plan_modify.html',context)

@login_required
def plan_submit(request):
    data = {}
    user = request.user
    depart = user.profile.department.department_name
    plan_pk = request.POST.get('plan_pk')
    try:
        plan_pk = int(plan_pk)
        plan = Plan.objects.get(pk=plan_pk)
    except Plan.DoesNotExist as e:
        data['status'] = 'ERROR'
        data['message'] = '计划不存在'
        return JsonResponse(data)
    status = ApplicationStatus.objects.get(pk=2)
    leader = User.objects.get(profile__department__department_name=depart,groups__name='部门领导')
    plan.application_status = status
    plan.operator.add(leader)
    plan.save()
    data['status'] = 'SUCCESS'
    return JsonResponse(data)

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

@login_required
def plan_review(request):
    user = request.user
    department = user.profile.department.department_name
    plan_list = Plan.objects.filter(Q(application_status=2)|Q(application_status=3),
                                    department__department_name=department).order_by('-date_of_application')
    context = {}
    context['plan_list'] = plan_list
    return render(request,'plan_management/plan_review.html',context)

@login_required
def review_page(request,plan_pk):
    try:
        plan_pk = int(plan_pk)
        plan = Plan.objects.get(pk=plan_pk)
    except Plan.DoesNotExist as e:
        return redirect(reverse('index'))
    model_class = ContentType.objects.get_for_model(plan).model
    form = DepartmentForm(
        initial={
            'reviewer':request.user.pk,
            'content_type':model_class,
            'object_id':plan_pk
        },
        user=request.user
    )
    context = {}
    context['plan'] = plan
    context['department_review_form'] = form
    return render(request,'plan_management/review_page.html',context)

@login_required
def view_review(request,plan_pk):
    try:
        plan_pk = int(plan_pk)
        plan = Plan.objects.get(pk=plan_pk)
    except Plan.DoesNotExist as e:
        return redirect(reverse('index'))
    if DepartmentReview.objects.filter(plan=plan).exists():
        review = DepartmentReview.objects.filter(plan=plan).order_by('-review_time').first()
        review_content = review.review_content
    else:
        review_content = ''
    context = {}
    context['plan'] = plan
    context['review_content'] = review_content
    return render(request,'plan_management/view_review.html',context)

@login_required
def department_not_pass(request):
    data = {}
    form = DepartmentForm(request.POST,user=request.user)

    if form.is_valid():
        status = ApplicationStatus.objects.get(pk=4)
        plan_obj = form.cleaned_data['content_object']
        plan_obj.operator.set('')
        plan_obj.application_status = status
        plan_obj.save()

        review_content = form.cleaned_data['review_content']
        reviewerpk = form.cleaned_data['reviewer']
        reviewer = User.objects.get(pk=reviewerpk)
        contenttype = form.cleaned_data['content_type']
        content_type = ContentType.objects.get(model=contenttype)
        object_id = form.cleaned_data['object_id']

        dr = DepartmentReview()
        dr.review_content = review_content
        dr.reviewer = reviewer
        dr.content_type = content_type
        dr.object_id = object_id
        dr.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())
        return JsonResponse(data)

@login_required
def department_pass(request):
    data = {}
    form = DepartmentForm(request.POST, user=request.user)

    if form.is_valid():
        # 把plan的状态改为审核通过
        status = ApplicationStatus.objects.get(pk=3)
        plan_obj = form.cleaned_data['content_object']
        plan_obj.operator.set('')
        plan_obj.application_status = status
        plan_obj.save()

        # 获取审核表需要的各种数据
        review_content = form.cleaned_data['review_content']
        reviewerpk = form.cleaned_data['reviewer']
        reviewer = User.objects.get(pk=reviewerpk)
        contenttype = form.cleaned_data['content_type']
        content_type = ContentType.objects.get(model=contenttype)
        object_id = form.cleaned_data['object_id']

        # 插入审核记录
        dr = DepartmentReview()
        dr.review_content = review_content
        dr.reviewer = reviewer
        dr.content_type = content_type
        dr.object_id = object_id
        dr.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())
        return JsonResponse(data)

@login_required
def add_plan_summary(request):
    form = PlanSummaryForm()
    plan_list = Plan.objects.filter(application_status_id=3,plan_summary=None)
    context = {}
    context['form'] = form
    context['plan_list'] = plan_list
    return render(request, 'plan_management/add_plan_summary.html', context)

@login_required
def add_plan_summary_interface(request):
    form = PlanSummaryForm(request.POST)
    plan_list = request.POST.getlist('plan_pk','')
    data = {}
    if form.is_valid():
        project_name = form.cleaned_data['project_name']
        year = form.cleaned_data['year']
        status = SummaryStatus.objects.get(pk=1)
        summary = Plan_Summary()
        summary.project_name = project_name
        summary.year = year
        summary.summary_status = status
        summary.save()
        for planid in plan_list:
            plan = Plan.objects.get(pk=planid)
            plan.plan_summary = summary
            plan.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())
        return JsonResponse(data)

@login_required
def view_summary(request,summary_pk):       #################从这里做##################
    try:
        summary_pk = int(summary_pk)
        summary = Plan_Summary.objects.get(pk=summary_pk)
        plan_list = Plan.objects.filter(plan_summary=summary)
    except Exception as e:
        return redirect(reverse('index'))
    context = {}
    context['summary'] = summary
    context['plan_list'] = plan_list
    return render(request,'plan_management/view_summary.html',context)

@login_required
def summary_delete(request):
    user = request.user
    try:
        summary_pk = int(request.GET.get('summary_pk'))
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': '该计划不存在'})
    data = {}
    if user.has_perm('plan_management.delete_plan_summary') and Plan_Summary.objects.filter(pk=summary_pk).exists():
        summary = Plan_Summary.objects.get(pk=summary_pk)
        plan_list = Plan.objects.filter(plan_summary=summary)
        plan_list.update(plan_summary='')
        summary.delete()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['message'] = '无权限或无计划书'
        return JsonResponse(data)

@login_required
def summary_modify(request,summary_pk):      #############zhelikaishi############
    try:
        summary_pk = int(summary_pk)
        summary = Plan_Summary.objects.get(pk=summary_pk)
        chirden_plans = list(Plan.objects.filter(plan_summary=summary).values('id'))
        plan_list = Plan.objects.filter(Q(plan_summary=None) | Q(plan_summary=summary), application_status_id=3)
    except Plan.DoesNotExist as e:
        return redirect(reverse('index'))
    form = PlanSummaryForm(
        initial={
            'project_name': summary.project_name,
            'year':summary.year,
        },
    )
    context = {}
    context['summary'] = summary
    context['form'] = form
    context['plan_list'] = plan_list
    return render(request,'plan_management/summary_modify.html',context)

@login_required
def summary_modify_interface(request,summary_pk):
    form = PlanSummaryForm(request.POST)
    data = {}
    if form.is_valid():
        plan_list = request.POST.getlist('plan_pk', '')
        project_name = form.cleaned_data['project_name']
        year = form.cleaned_data['year']
        status = SummaryStatus.objects.get(pk=1)
        summary = Plan_Summary.objects.get(pk=summary_pk)
        summary.year = year
        summary.project_name = project_name
        summary.summary_status = status
        summary.save()
        old_plan_list = Plan.objects.filter(plan_summary=summary)
        old_plan_list.update(plan_summary='')
        for planid in plan_list:
            plan = Plan.objects.get(pk=planid)
            plan.plan_summary = summary
            plan.save()
        data['status'] = 'SUCCESS'
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        data['message'] = list(form.errors.values())
        return JsonResponse(data)

@login_required
def print_summary(request):
    data = {}
    summary_pk = request.GET.get('summary_pk','')
    # 返回summary的所有信息
    summary = Plan_Summary.objects.get(pk=summary_pk)
    plans = Plan.objects.filter(plan_summary=summary)
    data['summary_name'] = summary.project_name
    data['summary_year'] = summary.year
    data['status'] = 'SUCCESS'
    return JsonResponse(data)

@login_required
def summary_download(request,summary_pk):
    #  根据summary_pk得到该汇总的所有计划
    file_name = '计划和汇总.xlsx'
    plans = list(Plan.objects.filter(plan_summary=summary_pk).values_list(
        'department__department_name',
        'user__profile__nickname',
        'year',
        'date_of_application',
    ))
    # 把这些计划导入excel
    wb = Workbook()
    ws = wb.active
    for plan in plans:
        ws.append(plan)
    wb.save('plan_management/static/plan_management/summary_download/%s' % file_name)
    # 返回下载数据
    file = open('plan_management/static/plan_management/summary_download/%s' % file_name,'rb')
    response = FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']="attachment;filename*={}".format(escape_uri_path(file_name))
    return response
