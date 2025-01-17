from django import forms
from .models import Track, Dot, SubDot, Topic

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['name']

class DotForm(forms.ModelForm):
    class Meta:
        model = Dot
        fields = ['name', 'track']

class SubDotForm(forms.ModelForm):
    class Meta:
        model = SubDot
        fields = ['name', 'dot']  

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
