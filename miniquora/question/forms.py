from django import forms
from .models import Question

class QuestionCreateForm(forms.ModelForm):
    #blah=forms.CharField(max_length=8)
    #field_order=['blah','title','text']
    class Meta:
        model=Question
        fields=['title','text']


