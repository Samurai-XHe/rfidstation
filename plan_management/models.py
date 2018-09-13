from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from assets_management.models import Assets
from department.models import Department
from review.models import DepartmentReview

class ApplicationStatus(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return '<application_status:%s>' % self.status

    class Meta():
        verbose_name_plural = '申请状态'

class SummaryStatus(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return '<summary_status:%s>' % self.status

    class Meta():
        verbose_name_plural = '计划书状态'

class Plan_Summary(models.Model):
    project_name = models.CharField(verbose_name='项目名称', max_length=20)
    year = models.IntegerField(verbose_name='年度')
    summary_status = models.ForeignKey(SummaryStatus,on_delete=models.CASCADE,verbose_name='计划书状态')
    def __str__(self):
        return '<plan_summary:%s>' % self.project_name

    class Meta():
        verbose_name_plural = '计划汇总表'

class Plan(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE,verbose_name='申报部门')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='plan_user',verbose_name='申报人')
    year = models.IntegerField(verbose_name='年度')
    date_of_application = models.DateField(verbose_name='申请日期')
    application_status = models.ForeignKey(ApplicationStatus,on_delete=models.CASCADE,verbose_name='申请状态')
    operator = models.ManyToManyField(User,related_name='plan_operator',verbose_name='操作人',null=True)
    assets = models.ManyToManyField(Assets,verbose_name='资产')
    plan_summary = models.ForeignKey(Plan_Summary,on_delete=models.CASCADE,verbose_name='所属计划书',null=True)

    review_content = GenericRelation(DepartmentReview,related_query_name='plan')

    def __str__(self):
        return '<plan:%s for %s>' % (self.department,self.date_of_application)

    class Meta():
        verbose_name_plural = '计划管理'
        permissions = (
            ('can_see','能看到计划管理模块'),
        )




