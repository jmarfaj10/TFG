import json
from django.shortcuts import render, redirect
from vis_go_app.services.robot_client import robot_client
from django.conf import settings
def index(request):
    return render(request, 'vis_go_app/index.html')

def about(request):
    return render(request, 'vis_go_app/about.html')

def home(request):
    return render(request, 'vis_go_app/home.html')

async def login_view(request):

    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('password')
        
        if user == settings.USER and password == settings.PASSWORD:
            res_raw_str = await robot_client.connect_ws(settings.ROBOT_USER, settings.ROBOT_PASS)
            res_raw = json.loads(res_raw_str)
            
            if res_raw.get("status") == "SUCCESS":
                request.session['auth'] = True
                return redirect('controlPanel')
        else:
            res_raw = {"status": "ERROR", "message": "Invalid user or password"}

        return render(request, 'vis_go_app/login.html', {"response": res_raw})
            
    return render(request, 'vis_go_app/login.html')

def controlPanel(request):

    b_ws_name = settings.B_WS_NAME

    if not request.session.get('auth'):
        return redirect('login')
        
    return render(request, 'vis_go_app/controlPanel.html', {"b_ws_name":b_ws_name})
