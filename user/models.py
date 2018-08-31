from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    nickname = models.CharField(max_length=20)

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return '<Profile:%s for %s>' % (self.nickname,self.user.username)

def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        pro = Profile.objects.get(user=self)
        return pro.nickname
    else:
        return self.username

User.get_nickname = get_nickname