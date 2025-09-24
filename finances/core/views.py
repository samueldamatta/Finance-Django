from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, ExpenseForm, IncomeForm
from .models import Transaction

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'accounts/login.html')

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Cadastro realizado com sucesso!')
                import logging
                logging.warning('Redirecionando para: /accounts/login/')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Erro ao criar conta: {str(e)}')
        else:
            # Mostrar erros específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def despesas(request):
    # Buscar todas as despesas do usuário logado
    expenses = Transaction.objects.filter(
        user=request.user, 
        transaction_type='despesa'
    ).order_by('-date')
    
    # Formulário para adicionar nova despesa
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Despesa adicionada com sucesso!')
            return redirect('despesas')
        else:
            messages.error(request, 'Erro ao adicionar despesa. Verifique os dados.')
    else:
        form = ExpenseForm()
    
    context = {
        'expenses': expenses,
        'form': form,
        'total_expenses': sum(expense.amount for expense in expenses)
    }
    return render(request, 'despesas.html', context)

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Transaction, id=expense_id, user=request.user, transaction_type='despesa')
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Despesa excluída com sucesso!')
    return redirect('despesas')

@login_required
def receitas(request):
    # Buscar todas as receitas do usuário logado
    incomes = Transaction.objects.filter(
        user=request.user, 
        transaction_type='receita'
    ).order_by('-date')
    
    # Formulário para adicionar nova receita
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Receita adicionada com sucesso!')
            return redirect('receitas')
        else:
            messages.error(request, 'Erro ao adicionar receita. Verifique os dados.')
    else:
        form = IncomeForm()
    
    context = {
        'incomes': incomes,
        'form': form,
        'total_incomes': sum(income.amount for income in incomes)
    }
    return render(request, 'receitas.html', context)

@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Transaction, id=income_id, user=request.user, transaction_type='receita')
    if request.method == 'POST':
        income.delete()
        messages.success(request, 'Receita excluída com sucesso!')
    return redirect('receitas')