from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Evento
from .forms import EventoForm, SignUpForm, LoginForm

# Create your views here.

def evento_list(request):
    eventos = Evento.objects.all().order_by('data')
    paginator = Paginator(eventos, 10)

    page = request.GET.get('page')
    eventos_page = paginator.get_page(page)

    return render(request, 'sistemareservas/evento_list.html', {
        'eventos': eventos_page
    })

@login_required
def evento_create(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user
            evento.save()
            return redirect('evento_list')
    else:
        form = EventoForm()

    return render(request, 'sistemareservas/evento_form.html', {'form': form})

@login_required
def evento_update(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if evento.organizador != request.user:
        return HttpResponse('Você não pode editar este evento.')

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('evento_list')
    else:
        form = EventoForm(instance=evento)

    return render(request, 'sistemareservas/evento_form.html', {'form': form})

@login_required
def evento_delete(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if evento.organizador != request.user:
        return HttpResponse('Você não pode excluir este evento.')

    evento.delete()
    return redirect('evento_list')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f'Bem-vindo, {user.username}! Cadastro realizado com sucesso.'
            )
            return redirect('evento_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()

    return render(request, 'sistemareservas/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {user.username}!')

                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)

                return redirect('evento_list')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()

    return render(request, 'sistemareservas/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema.')
    return redirect('login')

