from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} ({self.email})'
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('receita', 'Receita'),
        ('despesa', 'Despesa'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.transaction_type.capitalize()} of {self.amount} on {self.date} for {self.user.username}'
