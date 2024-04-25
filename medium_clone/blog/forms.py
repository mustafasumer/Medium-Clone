from django import forms
from django.core import validators
from tinymce.widgets import TinyMCE
from .models import BlogPost

#Our Validator:
from config.validators import min_length_3


class BlogPostModelForm(forms.ModelForm):
    tag = forms.CharField()
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 40, 'rows': 20}))
    # title = forms.CharField(validators=[validators.MinLengthValidator(3, message="En Az 3 Karakter Olmali..")])
    title = forms.CharField(validators=[min_length_3, ])

    class Meta:
        model = BlogPost
        fields = [
            'title',
            'cover_image',
            'content',
            'category',
            'tag',
        ]

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if len(title) < 3:
    #         raise forms.ValidationError('En Az 3 Karakter Olmali..')
    #     return title