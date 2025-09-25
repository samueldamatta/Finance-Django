from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, ExpenseForm, IncomeForm, CategoryForm
from .models import Transaction, Category
from django.db.models import Sum
from collections import defaultdict

# Create your views here.
@login_required
def index(request):
    #Gastos por categoria
    gastos_por_categoria = defaultdict(float)
    despesas_com_categoria = Transaction.objects.filter(
        user=request.user,
        transaction_type='despesa',
        category__isnull=False
    ).select_related('category')

    for despesa in despesas_com_categoria:
        categoria = despesa.category
        gastos_por_categoria[despesa.category.name] += float(despesa.amount)

    # Preparar dados para o gráfico
    categorias_labels = list(gastos_por_categoria.keys())
    categorias_values = list(gastos_por_categoria.values())

    #Encontrar categoria com maior gasto e menor gasto
    categoria_maior_gasto = None
    categoria_menor_gasto = None
    valor_maior_gasto = 0
    valor_menor_gasto = float('inf')

    for categoria, valor in gastos_por_categoria.items():
        if valor > valor_maior_gasto:
            valor_maior_gasto = valor
            categoria_maior_gasto = categoria
        if valor < valor_menor_gasto:
            valor_menor_gasto = valor
            categoria_menor_gasto = categoria

    #Se não há gastos, definir valores padrão
    if not gastos_por_categoria:
        valor_maior_gasto = 0

    # Buscar receitas do usuário logado
    receitas = Transaction.objects.filter(
        user=request.user, 
        transaction_type='receita'
    )
    
    # Buscar despesas do usuário logado
    despesas = Transaction.objects.filter(
        user=request.user, 
        transaction_type='despesa'
    )
    
    # Calcular totais
    total_receitas = sum(receita.amount for receita in receitas)
    total_despesas = sum(despesa.amount for despesa in despesas)
    saldo_atual = total_receitas - total_despesas
    
    # Buscar transações recentes (últimas 5)
    transacoes_recentes = Transaction.objects.filter(
        user=request.user
    ).order_by('-date', '-id')[:5]
    
    context = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo_atual': saldo_atual,
        'transacoes_recentes': transacoes_recentes,
        'categorias_labels': categorias_labels,
        'categorias_values': categorias_values,
        'categoria_maior_gasto': categoria_maior_gasto,
        'valor_maior_gasto': valor_maior_gasto,
        'categoria_menor_gasto': categoria_menor_gasto,
        'valor_menor_gasto': valor_menor_gasto,
    }
    
    return render(request, 'index.html', context)

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
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Despesa adicionada com sucesso!')
            return redirect('despesas')
        else:
            messages.error(request, 'Erro ao adicionar despesa. Verifique os dados.')
    else:
        form = ExpenseForm(user=request.user)
    
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
        form = IncomeForm(request.POST, user=request.user)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            messages.success(request, 'Receita adicionada com sucesso!')
            return redirect('receitas')
        else:
            messages.error(request, 'Erro ao adicionar receita. Verifique os dados.')
    else:
        form = IncomeForm(user=request.user)
    
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

@login_required
def categorias(request):
    # Criar categorias padrão se o usuário não tiver nenhuma
    if not Category.objects.filter(user=request.user).exists():
        default_categories = [
            {'name': 'Alimentação', 'category_type': 'despesa', 'icon': 'fas fa-utensils', 'color': '#ff6b6b'},
            {'name': 'Transporte', 'category_type': 'despesa', 'icon': 'fas fa-car', 'color': '#4ecdc4'},
            {'name': 'Moradia', 'category_type': 'despesa', 'icon': 'fas fa-home', 'color': '#45b7d1'},
            {'name': 'Saúde', 'category_type': 'despesa', 'icon': 'fas fa-heartbeat', 'color': '#f39c12'},
            {'name': 'Educação', 'category_type': 'despesa', 'icon': 'fas fa-graduation-cap', 'color': '#9b59b6'},
            {'name': 'Salário', 'category_type': 'receita', 'icon': 'fas fa-briefcase', 'color': '#27ae60'},
            {'name': 'Freelance', 'category_type': 'receita', 'icon': 'fas fa-laptop', 'color': '#3498db'},
            {'name': 'Investimentos', 'category_type': 'receita', 'icon': 'fas fa-chart-line', 'color': '#e74c3c'},
        ]
        
        for cat_data in default_categories:
            Category.objects.create(user=request.user, **cat_data)
    
    # Buscar todas as categorias do usuário logado
    categories = Category.objects.filter(user=request.user).order_by('name')
    
    # Formulário para adicionar nova categoria
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Categoria adicionada com sucesso!')
            return redirect('categorias')
        else:
            messages.error(request, 'Erro ao adicionar categoria. Verifique os dados.')
    else:
        form = CategoryForm()
    
    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'categorias.html', context)

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoria excluída com sucesso!')
    return redirect('categorias')