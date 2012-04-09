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
    
    user_email = forms.EmailField(label=_('Email address'),
            widget=EmailInput(attrs={'placeholder': _('mail@ddress.net')}))
     
    if user_can_hide_web:
        private = forms.BooleanField(required=False,
                label=_("Hide my name on the web"),
                help_text=mark_safe(_("If you check this, your name will still appear in requests to public bodies, but we will do our best to not display it publicly. However, we cannot guarantee your anonymity")))
        
    terms = forms.BooleanField(label=_("Terms and Conditions and Privacy Statement"),
            error_messages={'required':
                _('You need to accept our Terms and Conditions and Priavcy Statement.')},
            widget=AgreeCheckboxInput(
                agree_to=_(u'You agree to our <a href="%(url_terms)s" class="target-new">Terms and Conditions</a> and <a href="%(url_privacy)s" class="target-new">Privacy Statement</a>'),
                url_names={"url_terms": "help-terms", "url_privacy": "help-privacy"}))
    
    def clean_user_email(self):
        email = self.cleaned_data['user_email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.is_active:
                raise forms.ValidationError(mark_safe(
                    _('This email address already has an account. <a href="%s?simple" class="target-small">Please login using that email address.</a>') % reverse("account-login")))
            else:
                raise forms.ValidationError(
                    _('This email address is already registered, but not yet confirmed! Please click on the confirmation link in the mail we send you.'))
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
        cleaned = super(NewUserWithPasswordForm, self).clean()
        if cleaned['password'] != cleaned['password2']:
            raise forms.ValidationError(_("Passwords do not match!"))
        return cleaned
    
    def create_new_user(self):
        self.clean()
        cleaned = super(NewUserWithPasswordForm, self).clean()
        user, password = AccountManager.create_user(**cleaned)
        return user        
        

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=EmailInput(
        attrs={'placeholder': _('mail@ddress.net')}),
        label=_('Email address'))
    password = forms.CharField(widget=forms.PasswordInput,
        label=_('Password'))



