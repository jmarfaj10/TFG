import json
from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from vis_go_app.services.robot_client import robot_client
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.http import url_has_allowed_host_and_scheme
from vis_go_app.models import Log, Mission, Goal, Prompt
from datetime import datetime
from .forms import SignUpForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.utils.http import urlencode

def index(request):
    return render(request, 'vis_go_app/index.html')

def about(request):
    return render(request, 'vis_go_app/about.html')

def login_view(request):
    next_url = request.POST.get('next') or request.GET.get('next')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'vis_go_app/login.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('index')

def singup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'vis_go_app/singup.html', {'form': form})

@login_required
def controlPanel_view(request):
    res_raw = json.loads(
        async_to_sync(robot_client.connect_ws)(settings.ROBOT_USER, settings.ROBOT_PASS, request.user.id, request.META.get("REMOTE_ADDR", ""))
    )

    return render(request, 'vis_go_app/controlPanel.html', {
        "b_ws_name": settings.B_WS_NAME,
        "robot_status": res_raw.get("status"),
        "robot_message": res_raw.get("message"),
    })

@login_required
def logs_view(request):
    logs = Log.objects.filter(user=request.user).select_related('mission__prompt').order_by('-date')
    init_date = request.GET.get('init_date', '')
    final_date = request.GET.get('final_date', '')
    if init_date and final_date:
        try:
            # Formato europeo: es el que escribe el datepicker de la plantilla
            # (date-rangepicker con datepicker-format="dd-mm-yyyy").
            init = datetime.strptime(init_date, '%d-%m-%Y').date()
            final = datetime.strptime(final_date, '%d-%m-%Y').date()
            if init > final:
                init, final = final, init
            logs = logs.filter(date__date__range=(init, final))
        except ValueError:
            init_date = final_date = ''

    paginator = Paginator(logs, 10)
    try:
        n_page = int(request.GET.get('n_page', 1))
    except ValueError:
        n_page = 1
    page = paginator.get_page(n_page)
    n_pages = paginator.num_pages

    context = {
        'logs': page,
        'n_page': n_page,
        'n_pages': n_pages,
        'prev_page': max(n_page - 1, 1),
        'next_page': min(n_page + 1, n_pages),
        'has_prev': n_page > 1,
        'has_next': n_page < n_pages,
        'init_date': init_date,
        'final_date': final_date,
        'filters': urlencode({'init_date': init_date, 'final_date': final_date}) if init_date and final_date else '',
    }
    return render(request, 'vis_go_app/logs.html', context)

@login_required
def logs_remove(request):
    if request.method == "POST" and request.POST.get('id'):
        id = request.POST.get('id')
        log = get_object_or_404(Log, id=id, user=request.user)
        log.delete()
    return redirect('logs')

@login_required
def log_view(request, log_id):
    log = get_object_or_404(
            Log.objects.select_related('mission__prompt', 'mission__goal'),
            pk=log_id,
            user=request.user,
        )
    return render(request, 'vis_go_app/log.html', {'log': log})
