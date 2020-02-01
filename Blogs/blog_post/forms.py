from django import forms
from .models import Blogpost
from django.contrib.auth.models import User


class Contactform(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise forms.ValidationError("we don't accept this type of mail, please use '.com' extension mail")
        return email


class Blogform(forms.Form):      # this and  Blogmodelform both do same task
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)


class Blogmodelform(forms.ModelForm):
    class Meta:
        model = Blogpost
        fields = ['title', 'slug', 'image', 'content']

    def clean_title(self, *args, **kwargs):          # use only for checking specific thing/ use for validation
        title = self.cleaned_data.get('title')
        instance = self.instance
        qs = Blogpost.objects.filter(title__iexact=title)       # iexact treat small and capital same
        if instance is not None:             # this is used for update blog as it show error for same title
            qs = qs.exclude(id=instance.id)
        if qs.exists():
            raise forms.ValidationError("Title already exist")
        return title


class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

