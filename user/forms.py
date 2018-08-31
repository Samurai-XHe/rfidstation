import re
from django import forms
from django.core.validators import RegexValidator
from django.contrib import auth
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        label = '账户',
        max_length = 20,
        min_length = 3,
        widget = forms.TextInput(attrs={'class':'form-control','placeholder':'请输入您的账户'}),
        error_messages = {
            'max_length':'账户不能超过20位',
            'min_length':'账户不能少于3位',
            'required':'用户名或密码不能为空',
        },
        #validators = [RegexValidator('^[a-zA-Z][a-zA-Z0-9_]{2,19}$','必须是字母开头的字母数字组合(这是validators)')]
    )
    password = forms.CharField(
        label='密码',
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
        error_messages={
            'max_length': '密码不能超过20位',
            'min_length': '密码不能少于6位',
            'required': '用户名或密码不能为空',
        },
        #validators=[RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,19}$', '必须是字母开头的大小写字母和数字组合(这是validators)')]
    )

    def clean_username(self):
        username = self.cleaned_data.get('username','')
        if not re.search(r'^[a-zA-Z][a-zA-Z0-9_]{2,19}$',username):
            raise ValidationError('账户必须是字母开头的英文或英文数字组合')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if not re.search(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{7,19}$', password):
            raise ValidationError('密码必须是字母开头的大小写字母和数字组合')
        return password

    def clean(self):
        if LoginForm.has_error(self,'username') or LoginForm.has_error(self,'password'):
            return self.cleaned_data
        else:
            username = self.cleaned_data.get('username','')
            password = self.cleaned_data.get('password','')
            user = auth.authenticate(username=username,password=password)
            if user is None:
                raise ValidationError('用户名或密码错误')
            else:
                self.cleaned_data['user'] = user
            return self.cleaned_data
