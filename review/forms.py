from django import forms

class DepartmentForm(forms.Form):
    review_content = forms.CharField(max_length=50)
    #++++++++++++++++++该写form了++++++++++++++++++++++++
