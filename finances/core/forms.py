from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'seu.email@exemplo.com',
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu primeiro nome',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu sobrenome',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nome de usuário',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Digite sua senha',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirme sua senha',
            'class': 'form-control'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': '0,00',
                'class': 'form-control',
                'step': '0.01'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Descrição da transação (opcional)',
                'class': 'form-control',
                'rows': 3
            }),
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': '0,00',
                'class': 'form-control',
                'step': '0.01'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Descrição da despesa (opcional)',
                'class': 'form-control',
                'rows': 3
            }),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.transaction_type = 'despesa'
        if commit:
            instance.save()
        return instance

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': '0,00',
                'class': 'form-control',
                'step': '0.01'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Descrição da receita (opcional)',
                'class': 'form-control',
                'rows': 3
            }),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.transaction_type = 'receita'
        if commit:
            instance.save()
        return instance
        