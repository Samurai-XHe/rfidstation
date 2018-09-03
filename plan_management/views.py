from django.shortcuts import render

def plan_applications(request):
    return render(request,'plan_management/plan_applications.html')

def plan_review(request):
    return render(request,'plan_management/plan_review.html')

def plan_summary(request):
    return render(request,'plan_management/plan_summary.html')