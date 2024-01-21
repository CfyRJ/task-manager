from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from string import ascii_lowercase, ascii_uppercase, digits


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'password1', 'password2')

    def clean_username(self):
        good_symbols = '@.+-_' + ascii_lowercase + \
                        ascii_uppercase + digits

        username = self.cleaned_data['username']
        for symbol in username:
            if symbol not in good_symbols:
                raise forms.ValidationError(
                    '''The username must contain only letters,
                    numbers and the symbols @/./+/-/_.''')
        return username
