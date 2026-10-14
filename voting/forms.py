from django import forms


class UsernamePasswordResetForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Username",
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Enter your username",
            "autofocus": True,
        }),
    )