// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    initializeAuth();
});

function initializeAuth() {
    setupPasswordToggle();
    setupFormValidation();
    setupPasswordStrength();
    setupFormSubmission();
}

// Configuração do toggle de senha
function setupPasswordToggle() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
}

// Configuração da validação de formulários
function setupFormValidation() {
    const inputs = document.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            clearError(this);
        });
    });
}

// Validação individual de campo
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';
    
    // Validação básica de campo obrigatório
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'Este campo é obrigatório';
    }
    
    // Validações específicas por tipo de campo
    if (value) {
        switch (fieldName) {
            case 'email':
                if (!isValidEmail(value)) {
                    isValid = false;
                    errorMessage = 'Digite um e-mail válido';
                }
                break;
                
            case 'password':
                if (value.length < 8) {
                    isValid = false;
                    errorMessage = 'A senha deve ter pelo menos 8 caracteres';
                }
                break;
                
            case 'confirmPassword':
                const password = document.getElementById('password');
                if (password && value !== password.value) {
                    isValid = false;
                    errorMessage = 'As senhas não coincidem';
                }
                break;
                
            case 'firstName':
            case 'lastName':
                if (value.length < 2) {
                    isValid = false;
                    errorMessage = 'Digite pelo menos 2 caracteres';
                }
                break;
        }
    }
    
    // Validação de checkbox de termos
    if (field.type === 'checkbox' && fieldName === 'terms' && !field.checked) {
        isValid = false;
        errorMessage = 'Você deve aceitar os termos de uso';
    }
    
    showFieldError(field, isValid, errorMessage);
    return isValid;
}

// Limpar erro do campo
function clearError(field) {
    field.classList.remove('error');
    const errorElement = document.getElementById(field.name + '-error');
    if (errorElement) {
        errorElement.textContent = '';
    }
}

// Mostrar erro no campo
function showFieldError(field, isValid, errorMessage) {
    const errorElement = document.getElementById(field.name + '-error');
    
    if (isValid) {
        field.classList.remove('error');
        if (errorElement) {
            errorElement.textContent = '';
        }
    } else {
        field.classList.add('error');
        if (errorElement) {
            errorElement.textContent = errorMessage;
        }
    }
}

// Validação de e-mail
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Configuração do medidor de força da senha
function setupPasswordStrength() {
    const passwordInput = document.getElementById('password');
    const strengthBar = document.querySelector('.strength-fill');
    const strengthText = document.querySelector('.strength-text');
    
    if (passwordInput && strengthBar && strengthText) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            updatePasswordStrength(strengthBar, strengthText, strength);
        });
    }
}

// Calcular força da senha
function calculatePasswordStrength(password) {
    let score = 0;
    let feedback = '';
    
    if (password.length === 0) {
        return { score: 0, feedback: 'Digite uma senha' };
    }
    
    if (password.length >= 8) score += 1;
    if (password.length >= 12) score += 1;
    if (/[a-z]/.test(password)) score += 1;
    if (/[A-Z]/.test(password)) score += 1;
    if (/[0-9]/.test(password)) score += 1;
    if (/[^A-Za-z0-9]/.test(password)) score += 1;
    
    if (score < 3) {
        feedback = 'Senha fraca';
    } else if (score < 5) {
        feedback = 'Senha razoável';
    } else if (score < 6) {
        feedback = 'Senha boa';
    } else {
        feedback = 'Senha forte';
    }
    
    return { score, feedback };
}

// Atualizar indicador visual da força da senha
function updatePasswordStrength(strengthBar, strengthText, strength) {
    // Remover classes anteriores
    strengthBar.className = 'strength-fill';
    
    // Adicionar classe baseada na pontuação
    if (strength.score < 3) {
        strengthBar.classList.add('weak');
    } else if (strength.score < 5) {
        strengthBar.classList.add('fair');
    } else if (strength.score < 6) {
        strengthBar.classList.add('good');
    } else {
        strengthBar.classList.add('strong');
    }
    
    strengthText.textContent = strength.feedback;
}

// Configuração do envio de formulários
function setupFormSubmission() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginSubmit);
    }
    
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignupSubmit);
    }
}

// Manipular envio do formulário de login
function handleLoginSubmit(e) {
    const form = e.target;
    
    // Validar campos
    const emailField = form.querySelector('#email');
    const passwordField = form.querySelector('#password');
    
    let isValid = true;
    
    if (emailField && !validateField(emailField)) isValid = false;
    if (passwordField && !validateField(passwordField)) isValid = false;
    
    if (!isValid) {
        e.preventDefault(); // Só prevenir se houver erro
        showToast('Por favor, corrija os erros no formulário', 'error');
        return;
    }
    
    // Se chegou até aqui, deixa o Django processar o formulário normalmente
}

// Manipular envio do formulário de cadastro
function handleSignupSubmit(e) {
    // Remover preventDefault para permitir que o Django processe o formulário
    // e.preventDefault();
    
    const form = e.target;
    
    // Validar todos os campos antes de enviar
    const requiredFields = form.querySelectorAll('input[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        e.preventDefault(); // Só prevenir se houver erro
        showToast('Por favor, corrija os erros no formulário', 'error');
        return;
    }
    
    // Se chegou até aqui, deixa o Django processar o formulário normalmente
}

// Definir estado de carregamento do botão
function setLoadingState(button, isLoading) {
    const btnText = button.querySelector('.btn-text');
    const btnLoading = button.querySelector('.btn-loading');
    
    if (isLoading) {
        btnText.style.display = 'none';
        btnLoading.style.display = 'flex';
        button.disabled = true;
    } else {
        btnText.style.display = 'block';
        btnLoading.style.display = 'none';
        button.disabled = false;
    }
}

// Mostrar toast de notificação
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}

// Validação em tempo real para confirmação de senha
document.addEventListener('DOMContentLoaded', function() {
    const confirmPasswordField = document.getElementById('confirmPassword');
    const passwordField = document.getElementById('password');
    
    if (confirmPasswordField && passwordField) {
        confirmPasswordField.addEventListener('input', function() {
            if (this.value && passwordField.value) {
                validateField(this);
            }
        });
        
        passwordField.addEventListener('input', function() {
            if (confirmPasswordField.value) {
                validateField(confirmPasswordField);
            }
        });
    }
});

// Melhorar acessibilidade - navegação por teclado
document.addEventListener('keydown', function(e) {
    // Enter para enviar formulário quando focado em um campo
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
        const form = e.target.closest('form');
        if (form) {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                submitButton.click();
            }
        }
    }
});

// Função para integração com Django (exemplo)
function submitToServer(formData, endpoint) {
    return fetch(endpoint, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Erro:', error);
        throw error;
    });
}

// Função auxiliar para obter cookie CSRF (Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}