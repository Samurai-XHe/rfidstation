from django.db import models

class Department(models.Model):
    department_name = models.CharField('部门名称',max_length=20)
    order = models.IntegerField('次序')

    def __str__(self):
        return '<assets:%s>' % self.department_name

    class Meta():
        verbose_name_plural = '部门管理'