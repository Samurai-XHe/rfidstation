import datetime
from django import forms
from django.contrib.auth.models import User
from .models import Department
from .models import Assets

class PlanapplicationsForm(forms.Form):
    department = forms.CharField(
        label='申报部门',
        widget=forms.TextInput(attrs={'class':'form-control','readonly':''}),
        error_messages={
            'required': '申报部门不能为空!(这是forms字段验证)',
        },
    )
    user = forms.IntegerField(
        label='申报人',
        widget=forms.Select(attrs={'class':'form-control custom-select','readonly':''}),
        error_messages={
            'required': '申报人不能为空!(这是forms字段验证)',
        },
    )
    year = forms.CharField(
        label='年度',
        widget=forms.DateTimeInput(attrs={'class':'form-control','id':'date_input','readonly':''}),
        error_messages={
            'required': '年度不能为空!(这是forms字段验证)',
        },
    )
    date_of_application = forms.CharField(
        label='申请日期',
        widget=forms.DateInput(attrs={'class':'form-control','id':'date_time_input','readonly':''}),
        error_messages={
            'required': '申请日期不能为空!(这是forms字段验证)',
        },
    )
    assets = forms.IntegerField(
        label='资产',
        widget=forms.Select(attrs={'class':'form-control custom-select','readonly':''}),
        error_messages={
            'required': '申请日期不能为空!(这是forms字段验证)',
        },
    )
    def __init__(self,*args,**kwargs):
        if 'depart' in kwargs:
            self.depart = kwargs.pop('depart')
        super(PlanapplicationsForm, self).__init__(*args,**kwargs)
        self.fields['user'].widget.choices = User.objects.filter(profile__department__department_name=self.depart).values_list('id','username')
        self.fields['assets'].widget.choices = Assets.objects.all().values_list('id','assets_name')

    def clean_department(self):
        department = self.cleaned_data.get('department','')
        if department == '':
            raise forms.ValidationError('部门不存在')
        else:
            if department != self.depart:
                raise forms.ValidationError('部门错误')
            else:
                return department

    def clean_user(self):
        user = self.cleaned_data.get('user','')
        user_true = User.objects.filter(profile__department__department_name=self.depart).filter(pk=user)
        if not user_true:
            raise forms.ValidationError('申报人错误')
        else:
            return user

    def clean_year(self):
        year = self.cleaned_data.get('year','')
        if year == '' or len(year) > 4:
            raise forms.ValidationError('年份错误')
        else:
            return year

    def clean_date_of_application(self):
        date_of_application = self.cleaned_data.get('date_of_application','')
        if date_of_application == '':
            raise forms.ValidationError('日期错误')
        else:
            return date_of_application

    def clean_assets(self):
        assets = self.cleaned_data.get('assets','')
        aassets_true = Assets.objects.filter(pk=assets).exists()
        if assets == '' or not aassets_true:
            raise forms.ValidationError('资产不存在')
        return assets