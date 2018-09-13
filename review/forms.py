from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist

class DepartmentForm(forms.Form):
    review_content = forms.CharField(
        label='审核意见',
        max_length=50,
        widget=forms.Textarea(attrs={'placeholder':'请输入审核意见','class':'form-control','rows':2,'style':'resize:none'}),
        error_messages={
            'required':'请输入<审核意见>'
        }
    )
    reviewer = forms.CharField(
        max_length=10,
        min_length=1,
        widget=forms.HiddenInput
    )
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self,*args,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(DepartmentForm, self).__init__(*args,**kwargs)

    def clean(self):
        content_type = self.cleaned_data.get('content_type','')
        object_id = self.cleaned_data.get('object_id','')
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist as e:
            raise forms.ValidationError('计划不存在')
        return self.cleaned_data


    def clean_review_content(self):
        review_content = self.cleaned_data.get('review_content','')
        if len(review_content) > 50 or review_content == '':
            raise forms.ValidationError('请输入审核意见')
        else:
            return review_content

    def clean_reviewer(self):
        reviewer = self.cleaned_data.get('reviewer','')
        try:
            reviewer_pk = int(reviewer)
        except Exception as e:
            raise forms.ValidationError('审核人员不存在')
        if reviewer_pk != self.user.pk:
            raise forms.ValidationError('审核人员错误')
        else:
            return reviewer





