from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings

from jophiel.utils.helper.widgets import EmailInput, AgreeCheckboxInput
from .models import AccountManager

user_can_hide_web = settings.FROIDE_CONFIG.get("user_can_hide_web", True)

class NewUserForm(forms.Form):
    
    email = forms.EmailField(label=_('Email address'),
            widget=EmailInput(attrs={'placeholder': _('mail@ddress.net')}))
         
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.is_active:
                raise forms.ValidationError(_('This email address already has an accounte'))
            else:
                raise forms.ValidationError(_('please confirm your account'))
        return email

    def create_new_user(self):
        cleaned = super(NewUserWithPasswordForm, self).clean()
        user, password = AccountManager.create_user(**cleaned)
        AccountManager(user).send_confirmation_mail(password=password) 
        return user       
    
class NewUserWithPasswordForm(NewUserForm):
    password = forms.CharField(widget=forms.PasswordInput,
            label=_('Password'))
    password2 = forms.CharField(widget=forms.PasswordInput,
            label=_('Password (repeat)'))
    
    def clean(self):
        cleaned = super(NewUserWithPasswordForm,self).clean()
        if any(self.errors):
            return
        ps1 = cleaned["password"]
        ps2 = cleaned["password2"]
        if not ps1 == ps2:
            raise forms.ValidationError(_("the two passwords should be same"))
        return cleaned
    
    def create_new_user(self):
        cleaned = super(NewUserWithPasswordForm, self).clean()
        user, password = AccountManager.create_user(**cleaned)
        return user        
 

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(
        attrs={'placeholder': _('mail@ddress.net')}),
        label=_('Email address'))
    password = forms.CharField(widget=forms.PasswordInput,
        label=_('Password'))



