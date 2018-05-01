from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class DocumentForm(forms.Form):
    doc_file = forms.FileField(label= 'Select a file',
                               help_text= 'max. 42 megabytes')