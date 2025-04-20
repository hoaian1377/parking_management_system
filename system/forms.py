from django import forms

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nhập email của bạn'
    }))
