from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User

class DepartmentReview(models.Model):
    review_content = models.CharField(max_length=50,verbose_name='审核内容')
    review_time = models.DateTimeField(auto_now_add=True,verbose_name='审核时间')
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='审核人员')

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    def __str__(self):
        return '<DepartmentReview:%s>' % self.review_content
    class Meta():
        verbose_name_plural = '部门审核表'

class LogisticsReview(models.Model):
    review_content = models.CharField(max_length=50,verbose_name='审核内容')
    review_time = models.DateTimeField(auto_now_add=True,verbose_name='审核时间')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='审核人员')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return '<LogisticsReview:%s>' % self.review_content

    class Meta():
        verbose_name_plural = '后勤审核表'