from django.shortcuts import render

def index(request):
    return render(request, 'vis_go_app/index.html')

def about(request):
    return render(request, 'vis_go_app/about.html')

def controlPanel(request):
    return render(request, 'vis_go_app/controlPanel.html')
