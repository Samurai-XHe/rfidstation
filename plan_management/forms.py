from django import forms
from django.forms import fields,widgets
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Department,Plan
from .models import Assets

class PlanapplicationsForm(forms.Form):
    department = forms.CharField(
        label='申报部门',
        widget=forms.TextInput(attrs={'class':'form-control','readonly':''}),
        error_messages={
            'required': '<申报部门>不能为空!',
        },
    )
    user = forms.IntegerField(
        label='申报人',
        widget=forms.Select(attrs={'class':'form-control custom-select','readonly':''}),
        error_messages={
            'required': '<申报人>不能为空!',
        },
    )
    year = forms.CharField(
        label='年度',
        widget=forms.DateTimeInput(attrs={'class':'form-control','id':'date_input','readonly':''}),
        error_messages={
            'required': '<年度>不能为空!',
        },
    )
    date_of_application = forms.CharField(
        label='申请日期',
        widget=forms.DateInput(attrs={'class':'form-control','id':'date_time_input','readonly':''}),
        error_messages={
            'required': '<申请日期>不能为空!',
        },
    )
    assets = forms.IntegerField(
        label='资产',
        widget=forms.Select(attrs={'class':'form-control custom-select','readonly':''}),
        error_messages={
            'required': '<资产>不能为空!',
        },
    )
    def __init__(self,*args,**kwargs):
        if 'depart' in kwargs:
            self.depart = kwargs.pop('depart')
        super(PlanapplicationsForm, self).__init__(*args,**kwargs)
        # values_list方法可以获得一个列表形式的QuerySet对象，能直接用list转换成列表,例:[(0, ''), (1, '桌子'), (2, '椅子'), (3, '电视')]
        list1 = list(User.objects.filter(profile__department__department_name=self.depart).values_list('id','profile__nickname'))
        list1.insert(0,(0,'请选择'))  #添加一个空选项
        self.fields['user'].widget.choices = list1
        list2 = list(Assets.objects.all().values_list('id', 'assets_name'))
        list2.insert(0, (0, '请选择'))
        self.fields['assets'].widget.choices = list2


    def clean_department(self):
        department = self.cleaned_data.get('department','')
        if department == '':
            raise forms.ValidationError('<申报部门>不存在')
        else:
            if department != self.depart:
                raise forms.ValidationError('<申报部门>错误')
            else:
                return department

    def clean_user(self):
        user = self.cleaned_data.get('user','')
        user_true = User.objects.filter(profile__department__department_name=self.depart).filter(pk=user).exists()
        if not user_true:
            raise forms.ValidationError('请选择<申报人>')
        else:
            return user

    def clean_year(self):
        year = self.cleaned_data.get('year','')
        if year == '' or len(year) > 4:
            raise forms.ValidationError('<年度>错误')
        else:
            return year

    def clean_date_of_application(self):
        date_of_application = self.cleaned_data.get('date_of_application','')
        if date_of_application == '':
            raise forms.ValidationError('<申请日期>错误')
        else:
            return date_of_application

    def clean_assets(self):
        assets = self.cleaned_data.get('assets','')
        aassets_true = Assets.objects.filter(pk=assets).exists()
        if assets == '' or not aassets_true:
            raise forms.ValidationError('请选择<资产>')
        return assets

class PlanSummaryForm(forms.Form):
    project_name = forms.CharField(
        label='计划书名称',
        max_length= 20,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        error_messages={
            'required':'计划书名称不能为空',
            'max_length':'不得超过20个字符'
        }
    )
    year = forms.CharField(
        label='年度',
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'date_input', 'readonly': ''}),
        error_messages={
            'required': '<年度>不能为空!',
        },
    )

    def clean_year(self):
        year = self.cleaned_data.get('year','')
        if year == '' or len(year) > 4:
            raise forms.ValidationError('<年度>错误')
        else:
            return year

