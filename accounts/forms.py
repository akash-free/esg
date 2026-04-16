# =============================================================================
# FILE    : accounts/forms.py
# APP     : accounts
# PURPOSE : Login form — username + password
# =============================================================================

import logging
from django import forms

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class'       : 'form-control',
            'placeholder' : 'Enter username',
            'autofocus'   : True,
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class'       : 'form-control',
            'placeholder' : 'Enter password',
        })
    )