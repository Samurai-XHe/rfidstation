from django.db import models

class Assets(models.Model):
    assets_name = models.CharField('资产名称',max_length=20)
    price = models.FloatField('价格')
    order = models.IntegerField('次序')

    def __str__(self):
        return '<assets:%s>' % self.assets_name

    class Meta():
        verbose_name_plural = '资产管理'