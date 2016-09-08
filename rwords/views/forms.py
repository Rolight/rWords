from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm

from rwords.models import WordBook, UserProperty

class RegisterForm(UserCreationForm):

    error_css_class = 'has-error'

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].help_text = _(
            '少于150个字符，只支持字母数字以及@/./+/-/_ '
        )

    def save(self, commit=True):
        super(RegisterForm, self).save()
        UserProperty.objects.create(user=self.instance)

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


# 创建单词书表单
class CreateWordBookForm(ModelForm):

    words_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='单词本数据包')

    class Meta:
        model = WordBook
        fields = ('name', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
