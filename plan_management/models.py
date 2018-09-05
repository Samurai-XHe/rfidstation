from django.db import models
from django.contrib.auth.models import User
from assets_management.models import Assets
from department.models import Department

class ApplicationStatus(models.Model):
    status = models.CharField(max_length=20)

    def __str__(self):
        return '<applicationstatus:%s>' % self.status

    class Meta():
        verbose_name_plural = '申请状态'

class Plan(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE,verbose_name='申报部门')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='plan_user',verbose_name='申报人')
    year = models.IntegerField('年度')
    date_of_application = models.DateField('申请日期')
    application_status = models.ForeignKey(ApplicationStatus,on_delete=models.CASCADE,verbose_name='申请状态')
    operator = models.ManyToManyField(User,related_name='plan_operator',verbose_name='操作人',null=True)
    assets = models.ManyToManyField(Assets,verbose_name='资产')

    def __str__(self):
        return '<plan:%s for %s>' % (self.department,self.date_of_application)

    class Meta():
        verbose_name_plural = '计划管理'
        permissions = (
            ('can_see','能看到计划管理模块'),
        )


