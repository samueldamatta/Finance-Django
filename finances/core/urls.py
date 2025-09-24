from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/signup/', user_signup, name='signup'),
    path('accounts/logout/', user_logout, name='logout'),
    path('despesas/', despesas, name='despesas'),
    path('despesas/delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('receitas/', receitas, name='receitas'),
    path('receitas/delete/<int:income_id>/', delete_income, name='delete_income'),
]