from django import forms
from .models import Track, Module, SubDot, Topic

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['name']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'track']

class SubDotForm(forms.ModelForm):
    class Meta:
        model = SubDot
        fields = ['name', 'module']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'content', 'code', 'image', 'audio', 'subdot']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'tinymce'}),  # For TinyMCE
            'code': forms.Textarea(attrs={'class': 'monaco'})  # For Monaco Editor
        }

class ContentForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)
    code = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)
    audio = forms.FileField(required=False)
